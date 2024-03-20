import abc
from telnetlib import Telnet
from core.utilities.logging.custom_logger import create_logger


class ReflectionClientBase(object):
    """
    This is the class responsible fr calling our Pro*C commands via python.
    """

    # timeout used when reading from telnet. this has been assigned arbitrarily and
    # appears to work fine
    TIMEOUT_DEFAULT_SECONDS = 10

    # this is our marker when trying to wait for a response we're not entirely sure of
    # or if the response does not matter during the course of runners
    EOF = '^]'

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__timeout = ReflectionClientBase.TIMEOUT_DEFAULT_SECONDS
        self.__session_exists = False
        self.__encoding = "ascii"
        self.__log = create_logger()
        self._client = None

    def initialize_client(self):
        self._client = Telnet(self.__host, self.__port, self.__timeout)
        self.session_exists = True

    @abc.abstractmethod
    def close_session(self):
        pass

    @property
    def session_exists(self):
        return self.__session_exists

    @session_exists.setter
    def session_exists(self, session_exists):
        self.__session_exists = session_exists

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int):
        self.__timeout = timeout

    def set_encoding(self, encoding: str):
        """
            Sets the encoding when sending via telnet.
            Currently using ascii
        :param encoding:
        :return:
        """
        self.__encoding = encoding

    def set_timeout(self, timeout: int):
        # helper method in case our run becomes too lengthy
        self.__timeout = timeout

    def get_any_response(self):
        """
            Method for reading any response and returning result
            once timeout expires, or EOF found.
        :param self:
        :return: str value of the response
        """
        self.__log.info("get_any_response")
        return self.__read_any__()

    def get_expected_response(self, expect: str):
        """
            Method for waiting for an expected response. Returns once expect is found
        :param self:
        :param expect: the expected response from our previous call.
        :return: str value of the response
        """
        self.__log.info(f"get_expected_response - expected: {expect}")

        return self.__send_read_request__(expect)

    def _send_and_receive_with_path_and_expected_(self, path, request, expected_response: str, *args):
        self._send_request_and_path_(path, request, *args)
        return self.get_expected_response(expected_response)

    def _send_and_receive_with_expected_(self, request: str, expected_response: str, *args):
        self._send_request_(request, *args)
        return self.get_expected_response(expected_response)

    def _send_and_receive_with_path_(self, path, request, *args):
        self._send_request_and_path_(path, request, *args)
        return self.get_any_response()

    def send_and_receive(self, request: str, *args):
        self._send_request_(request, *args)
        return self.get_any_response()

    def _send_request_and_path_(self, path, request, *args):
        full_cmd = "/".join([path, request])
        self._send_request_(full_cmd, *args)

    # request consists of the full command, then arguments to the command
    def _send_request_(self, request: str, *args):
        clean_args = [item.strip() for item in args if len(item) > 0]
        joined_args = " ".join(clean_args)
        full_request = " ".join([request.strip(), joined_args.strip()])
        self.__send_write_request__(full_request)

    def __send_write_request__(self, request: str):
        self.__log.info(f"send_write_request - request: {request}")

        if "\n" not in request:
            request = f"{request}\n"
        self._client.write(request.encode(self.__encoding))

    def __send_read_request__(self, request: str):
        self.__log.info(f"send_read_request - request: {request}")

        return str(self._client.read_until(request.encode(self.__encoding), self.__timeout)).encode(self.__encoding)\
            .decode(self.__encoding)

    def __read_any__(self):
        self.__log.info("read any...")
        return str(self._client.read_until(ReflectionClientBase.EOF.encode(self.__encoding), self.__timeout))

