import socket
from abc import abstractmethod

from web.services.core.clients.ssh import SSHClient


class IProCClient:
    @abstractmethod
    def send_raw(self, input_cmd: str):
        ...

    @abstractmethod
    def send_and_receive_with_expected_raw(self, input_cmd: str, expected_str: str) -> str:
        ...

    @abstractmethod
    def read_until(self, expected_result, custom_timeout: int = None) -> str:
        ...

    @abstractmethod
    def read_any(self, custom_timeout: int = None) -> str:
        ...


class SSHTelnetClient(IProCClient, SSHClient):

    def __init__(self, host, port, ssh_user, ssh_pwd, read_block=1024, read_timeout=60):
        super(SSHTelnetClient, self).__init__(host, port, ssh_user, ssh_pwd)
        self.__read_block = read_block
        self.__read_timeout = read_timeout
        self.__channel = self.get_channel_for_new_session()
        self.__channel.setblocking(True)
        # preserve our channel

    def set_read_timeout(self, timeout: int):
        self.__read_timeout = timeout

    def set_block_size(self, block_size: int):
        self.__read_block = block_size

    def send_raw(self, inputcommands: str):
        # ensure we have a newline
        inputcommands = inputcommands.strip("\n") + "\n"
        stdin = self.__channel.makefile("wb")
        stdout = self.__channel.makefile("rb")
        stdin.write(inputcommands)
        stdout.close()
        stdin.close()

    def send_and_receive(self,  inputcommands: str):
        self.send_raw(inputcommands)
        return self.read_any()

    def send_and_receive_with_expected_raw(self, inputcommands: str, expected_str: str) -> str:
        self.send_raw(inputcommands)
        return self.read_until(expected_str)

    def read_until(self, expected_result, custom_timeout: int = None) -> str:

        if custom_timeout is not None:
            self.__channel.settimeout(custom_timeout)
        else:
            self.__channel.settimeout(self.__read_timeout)
        result = ""
        while not (expected_result is not None and expected_result in result):
            try:
                chunk = self.__channel.recv(self.__read_block)
                self._log.info(f"read: {str(chunk)}")

                result = str.format("{}{}", result, chunk.decode(self._encoding))

            except socket.timeout:
                break
        #channel.close()
        return result

    def read_any(self, custom_timeout: int = None) -> str:
        return self.read_until(None, custom_timeout)
