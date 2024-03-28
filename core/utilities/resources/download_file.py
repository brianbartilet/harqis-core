import os
from core.web.services.core.constants.http_methods import HttpMethod
from core.web.services.fixtures.rest import BaseFixtureServiceRest
from core.web.services.core.config.webservice import AppConfigWSClient


class ServiceDownloadFile(BaseFixtureServiceRest):
    def __init__(self, url: str, headers: dict[str, str] = None, **kwargs):
        config = AppConfigWSClient(
            client="rest",
            parameters={
                "base_url": url,
                "response_encoding": "binary",
                "verify": False,
                "timeout": 10,
                "stream": True,
            },
            headers=headers
        )
        super(ServiceDownloadFile, self).__init__(config=config, **kwargs)

    def download_file(self, file_name: str, path=os.getcwd(), resource="", ):
        self.request.set_method(HttpMethod.GET)\
            .add_uri_parameter(resource)\
            .strip_right_url(True)

        response = self.client.execute_request(self.request.build())

        file_path = os.path.join(path, file_name)
        with open(file_path, 'wb') as file:
            # Write the content of the response to the file in chunks
            file.write(response.raw_bytes)

        return response
