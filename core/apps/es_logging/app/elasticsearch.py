import jsonmerge
import requests
import functools
import base64

from core.apps.config import AppNames, AppConfigLoader
from core.apps.es_logging.models.document import DtoFunctionLogger, update_interval_map
from core.config.env_variables import ENV_ENABLE_PROXY
from core.utilities.data.qlist import QList

from datetime import datetime
from http import HTTPStatus
from urllib.parse import urljoin


from hamcrest import assert_that, any_of, equal_to

APP_NAME = AppNames.ELASTIC_LOGGING

config = AppConfigLoader(AppNames.ELASTIC_LOGGING).config
app_data = config.app_data

LOGGING_INDEX = app_data.get('default_index', "harqis-elastic-logging")
ELASTIC_TIME_FORMAT = app_data.get('time_format', "%Y-%m-%dT%H:%M")


def log_result(logging_index=LOGGING_INDEX):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            path = "{0}.{1}".format(func.__module__, func.__qualname__)
            try:
                logs = QList(get_index_data(logging_index, type_hook=DtoFunctionLogger))

                target = logs.where(lambda x: x.name == path).first() if len(logs) > 0 else None
            except Exception:
                target = None
            args_str = ''.join(['"{0}" '.format(str(arg)) for arg in args])
            index_dto = DtoFunctionLogger(name=path,
                                          passed=0,
                                          failed=0,
                                          last_failed='2000-01-01T00:00',
                                          pass_fail_percent=0,
                                          exception_message='None',
                                          args=args_str) \
                if not target else target

            f = error = None
            now = datetime.now().strftime(ELASTIC_TIME_FORMAT)
            try:
                f = func(*args, **kwargs)
                index_dto.passed += 1
                # reset the initial date
                index_dto.last_failed = '2000-01-01T00:00'
            except Exception as e:
                error = e
                index_dto.failed += 1
                index_dto.last_failed = now
                index_dto.exception_message = error.__class__.__name__
                index_dto.args = args_str
            finally:
                index_dto.date = now
                index_dto.compute_stat()

                post(json_dump=index_dto.get_dict(),
                     index_name=logging_index,
                     use_interval_map=False,
                     location_key=path)
                if error:
                    raise error

            return f

        return wrapper

    return decorator


def _looks_base64(s: str) -> bool:
    try:
        # tolerate padding variations
        base64.b64decode(s + "==", validate=True)
        return True
    except Exception:
        return False


def _es_session():
    """
    Build a configured requests.Session for Elasticsearch.
    Relies on globals: app_data, ENV_ENABLE_PROXY, config.parameters['url'].
    """
    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json"})
    auth_type = (app_data.get("auth_type") or "").lower()

    if auth_type == "basic":
        sess.auth = (app_data["username"], app_data["password"])
    elif auth_type == "api_key":
        api_key = app_data.get("api_key", "")
        if ":" in api_key and not _looks_base64(api_key):
            api_key = base64.b64encode(api_key.encode("utf-8")).decode("ascii")
        sess.headers["Authorization"] = f"ApiKey {api_key}"
    elif auth_type == "bearer":
        sess.headers["Authorization"] = f"Bearer {app_data['token']}"

    if str(ENV_ENABLE_PROXY).lower() == "true":
        sess.proxies.update(app_data.get("proxies") or {})

    sess.verify = app_data.get("verify_ssl", True)
    return sess, (config.parameters["url"].rstrip("/") + "/")


def _map_hits(hits, type_hook):
    if type_hook is None:
        return hits
    mapped = []
    for h in hits:
        src = h.get("_source", {})
        mapped.append(type_hook(**src))
    return mapped


def post(json_dump, index_name: str, location_key: str, use_interval_map=True, identifier=''):
    """
    Index a JSON doc into Elasticsearch with robust auth handling.

    Expects globals:
      - app_data: {
          'update_interval': '5m' | '1h' | ...,
          'auth_type': 'basic' | 'api_key' | 'bearer' | None,
          # for basic:
          'username': 'elastic',
          'password': '*******',
          # for api_key: base64(id:key) OR raw "id:key" (both supported)
          'api_key': 'base64_or_id_colon_key',
          # for bearer:
          'token': 'eyJhbGciOi...',
          'use_basic_auth': False,  # legacy flag not needed anymore
          'proxies': {'http': 'http://...', 'https': 'http://...'},
          'verify_ssl': True
        }
      - update_interval_map: dict mapping update_interval to a suffix key
      - config.parameters['url']: base ES URL like "https://localhost:9200/"
      - ENV_ENABLE_PROXY: "true"/"false"
    """

    update_interval_config = str(app_data['update_interval']).upper()
    if use_interval_map:
        id_ = '_' + update_interval_map[update_interval_config]
    else:
        id_ = '' if not identifier else '_' + identifier

    loc = f"{location_key}{id_}"
    print(f"Using {update_interval_config} interval with generated location key {loc}")

    # Merge timestamp into payload
    result = jsonmerge.merge(
        {"date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')},
        json_dump
    )

    # Build URL safely
    base = config.parameters['url'].rstrip('/') + '/'
    url = urljoin(base, f"{index_name}/_doc/{loc}")

    # Headers and auth
    headers = {'Content-Type': 'application/json'}
    auth = None

    auth_type = (app_data.get('auth_type') or '').lower()

    if auth_type == 'basic':
        # Best practice: let requests add the header
        auth = (app_data['username'], app_data['password'])
    elif auth_type == 'api_key':
        api_key = app_data.get('api_key', '')
        # Accept either already-base64 or raw "id:key"
        if ':' in api_key and not _looks_base64(api_key):
            api_key = base64.b64encode(api_key.encode('utf-8')).decode('ascii')
        headers['Authorization'] = f"ApiKey {api_key}"
    elif auth_type == 'bearer':
        headers['Authorization'] = f"Bearer {app_data['token']}"
    else:
        # No auth configured
        pass

    proxies = app_data['proxies'] if str(ENV_ENABLE_PROXY).lower() == "true" else None
    verify = app_data.get('verify_ssl', True)

    # Send JSON properly; requests sets Content-Length and encoding
    response = requests.post(
        url=url,
        json=result,
        headers=headers,
        auth=auth,
        proxies=proxies,
        verify=verify,
        timeout=20
    )

    # Helpful logging on failures
    if response.status_code == 401:
        wa = response.headers.get('WWW-Authenticate', '<none>')
        print(f"[401 Unauthorized] Check credentials/permissions. WWW-Authenticate: {wa}")
        print(f"Response body: {response.text}")
    elif response.status_code >= 400:
        print(f"[{response.status_code}] Error indexing doc id={loc}")
        print(f"Response body: {response.text}")

    print(f"Sending data from item {location_key} got response: {response.status_code}")

    assert_that(
        response.status_code,
        any_of(equal_to(HTTPStatus.CREATED), equal_to(HTTPStatus.OK))
    )


def get_index_data(
    index_name: str,
    type_hook=None,
    search_string: str | None = None,
    fetch_docs: int = 10_000,
    *,
    query: dict | None = None,
    use_scroll: bool | None = None,
    timeout: int = 20,
):
    """
    Fetch documents from an Elasticsearch index.

    Args:
      index_name: target index.
      type_hook: callable to map each _source -> object (e.g., dataclass(**_source)).
      search_string: Lucene q=... string (e.g., 'status:active AND tag:foo').
      fetch_docs: number of docs to return (defaults to 10,000).
      query: full Query DSL body (dict). If provided, POST is used.
      use_scroll: if True, use the Scroll API (useful when fetch_docs > 10k).
                  If None, it auto-enables when fetch_docs > 10k.
      timeout: request timeout in seconds.

    Returns:
      List of docs (either raw hits or type_hook(_source)).
    """
    sess, base = _es_session()
    url = urljoin(base, f"{index_name}/_search")

    # Decide whether to use scroll
    if use_scroll is None:
        use_scroll = fetch_docs > 10_000

    out = []
    try:
        if not use_scroll:
            # Simple one-shot search: either GET with q= or POST with body.
            params = {
                "size": fetch_docs,
                "track_total_hits": "true",  # reliable totals on ES 7/8
            }
            if query is not None:
                body = dict(query=query, size=fetch_docs, track_total_hits=True)
                resp = sess.post(url, json=body, timeout=timeout)
            else:
                params["q"] = search_string if search_string is not None else "*:*"
                resp = sess.get(url, params=params, timeout=timeout)

            if resp.status_code == 401:
                wa = resp.headers.get("WWW-Authenticate", "<none>")
                print(f"[401 Unauthorized] WWW-Authenticate: {wa}")
                print(f"Response body: {resp.text}")

            if resp.status_code not in (HTTPStatus.OK, HTTPStatus.CREATED):
                raise RuntimeError(f"Search failed ({resp.status_code}): {resp.text}")

            payload = resp.json()
            hits = payload.get("hits", {}).get("hits", [])
            out = _map_hits(hits, type_hook)
            return out

        # Scroll path for >10k or deep pagination
        # Note: Scroll keeps a search context open; use short TTLs.
        scroll_ttl = "1m"
        init_body = {
            "size": min(10_000, fetch_docs),
            "sort": ["_doc"],  # efficient, order not guaranteed
            "track_total_hits": True,
        }
        if query is not None:
            init_body["query"] = query
        elif search_string is not None:
            init_body["query"] = {"query_string": {"query": search_string}}
        else:
            init_body["query"] = {"match_all": {}}

        init_resp = sess.post(
            url,
            params={"scroll": scroll_ttl},
            json=init_body,
            timeout=timeout,
        )

        data = init_resp.json()
        scroll_id = data.get("_scroll_id")
        hits = data.get("hits", {}).get("hits", [])
        out.extend(_map_hits(hits, type_hook))

        remaining = max(0, fetch_docs - len(out))

        while remaining > 0 and hits:
            sc_resp = sess.post(
                urljoin(base, "_search/scroll"),
                json={"scroll": scroll_ttl, "scroll_id": scroll_id},
                timeout=timeout,
            )
            if sc_resp.status_code not in (HTTPStatus.OK, HTTPStatus.CREATED):
                raise RuntimeError(f"Scroll page failed ({sc_resp.status_code}): {sc_resp.text}")

            sc = sc_resp.json()
            scroll_id = sc.get("_scroll_id")
            hits = sc.get("hits", {}).get("hits", [])
            if not hits:
                break

            batch = _map_hits(hits, type_hook)
            if remaining < len(batch):
                batch = batch[:remaining]
            out.extend(batch)
            remaining = fetch_docs - len(out)

        if scroll_id:
            try:
                sess.delete(urljoin(base, "_search/scroll"), json={"scroll_id": [scroll_id]}, timeout=timeout)
            except Exception:
                pass

        return out

    except requests.RequestException as e:
        raise RuntimeError(f"Network error talking to Elasticsearch: {e}") from e



