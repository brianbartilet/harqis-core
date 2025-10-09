#!/usr/bin/env bash
set -euo pipefail

PORT="${HOST_PORT_ELASTICSEARCH_HTTP:-9200}"
REPO="${SNAP_REPO:-local_fs}"
SNAP_DIR="${SNAP_DIR:-./es_snapshots}"
ES="http://localhost:${PORT}"

usage() {
  cat <<USAGE
Usage: $0 <command> [args]

Commands:
  register
  backup
  list
  restore <SNAPSHOT>
  restore-prefix <SNAPSHOT> [PREFIX]
  archive

Env (optional):
  HOST_PORT_ELASTICSEARCH_HTTP (default: 9200)
  SNAP_REPO (default: local_fs)
  SNAP_DIR  (default: ./es_snapshots)
USAGE
}

require_curl() { command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }; }
require_tar()  { command -v tar  >/dev/null 2>&1 || { echo "tar is required"; exit 1; }; }

register_repo() {
  mkdir -p "${SNAP_DIR}"
  echo "Registering snapshot repo '${REPO}' at ${ES} -> ${SNAP_DIR}"
  curl -sS -X PUT "${ES}/_snapshot/${REPO}" \
    -H 'Content-Type: application/json' \
    -d '{"type":"fs","settings":{"location":"/usr/share/elasticsearch/snapshots","compress":true}}' | sed 's/{"acknowledged":true}/Repo OK/'
}

backup_snapshot() {
  ts="$(date +%Y%m%d-%H%M%S)"
  snap="snap-${ts}"
  echo "Creating snapshot ${snap}..."
  curl -sS -X PUT "${ES}/_snapshot/${REPO}/${snap}?wait_for_completion=true" \
    -H 'Content-Type: application/json' \
    -d '{"indices":"*","ignore_unavailable":true,"include_global_state":true}' | jq -r '.snapshot.state // .accepted // .error' || true
  echo "Done. Snapshot name: ${snap}"
}

list_snapshots() {
  curl -sS "${ES}/_snapshot/${REPO}/_all?pretty"
}

restore_snapshot() {
  snap="${1:-}"; [[ -z "${snap}" ]] && { echo "Missing <SNAPSHOT>"; usage; exit 1; }
  echo "Restoring snapshot ${snap} (includes global state)..."
  curl -sS -X POST "${ES}/_snapshot/${REPO}/${snap}/restore" \
    -H 'Content-Type: application/json' \
    -d '{"indices":"*","ignore_unavailable":true,"include_global_state":true}'
  echo
}

restore_prefix() {
  snap="${1:-}"; prefix="${2:-restored_}"
  [[ -z "${snap}" ]] && { echo "Missing <SNAPSHOT>"; usage; exit 1; }
  echo "Restoring snapshot ${snap} with prefix '${prefix}' (no global state)..."
  curl -sS -X POST "${ES}/_snapshot/${REPO}/${snap}/restore" \
    -H 'Content-Type: application/json' \
    -d "{\"indices\":\"*\",\"ignore_unavailable\":true,\"include_global_state\":false,\"rename_pattern\":\"(.+)\",\"rename_replacement\":\"${prefix}\\1\",\"indices_options\":{\"expand_wildcards\":\"open,closed\"}}"
  echo
}

archive_snapshots() {
  require_tar
  mkdir -p "${SNAP_DIR}"
  out="es_snapshots_$(date +%Y%m%d_%H%M%S).tgz"
  echo "Archiving ${SNAP_DIR} -> ${out}"
  tar -czf "${out}" -C "${SNAP_DIR}" .
  echo "Created ${out}"
}

main() {
  require_curl
  cmd="${1:-}"; shift || true
  case "${cmd}" in
    register)        register_repo ;;
    backup)          backup_snapshot ;;
    list)            list_snapshots ;;
    restore)         restore_snapshot "${1:-}";;
    restore-prefix)  restore_prefix "${1:-}" "${2:-restored_}";;
    archive)         archive_snapshots ;;
    *)               usage; exit 1 ;;
  esac
}

main "$@"
