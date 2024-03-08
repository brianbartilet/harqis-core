import paramiko
from utilities.logging.custom_logger import custom_logger
import sys
import time


class SSHClient:

    def __init__(self, host, port, ssh_user, ssh_pwd):
        self._host = host
        self._port = port
        self._log = custom_logger()
        self._encoding = "UTF-8"
        self._remote_path = None
        self._local_path = None
        self._input_commands = None
        self.__ssh_client = None

        if self._host is None:
            sys.exit("SSH Host is mandatory")
        if self._port is None:
            sys.exit("SSH Port is mandatory")
        if ssh_user is None:
            sys.exit("User is mandatory to establish SSH connection")
        if ssh_pwd is None:
            sys.exit("Password is mandatory to establish SSH connection")

        try:
            self.__ssh_client = paramiko.SSHClient()
            self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh_client.connect(self._host, self._port, ssh_user, ssh_pwd)
        except paramiko.AuthenticationException:
            self._log.error("Unable to establish SSH client connection to the Host %s" % self._host)

    '''
    Starts new session on SSH server and returns a Channel object. 
    '''
    def get_channel_for_new_session(self):
        if self.__ssh_client is None:
            self._log.error("No Active SSH Client connection")
        return self.__ssh_client.invoke_shell()

    def open_sftp_connection(self):
        if self.__ssh_client is None:
            self._log.error("No Active SSH connection")
        return self.__ssh_client.open_sftp()

    def sftp_file_exists_to_remote(self, sftp_client, remote_path, file_name):
        if sftp_client is None:
            sftp_client = self.open_sftp_connection()
        if remote_path is None:
            self._log.error(" Remote location on server is mandatory to transfer the file")

        sftp_client.chdir(remote_path)
        is_file_exists = False

        for file_attr in sftp_client.listdir_attr():
            if file_attr.filename.startswith(file_name):
                is_file_exists = True
                break

        return is_file_exists

    def sftp_file_remote_to_local(self, sftp_client, remote_path, file_name, local_path):
        if sftp_client is None:
            sftp_client = self.open_sftp_connection()
        if remote_path is None:
            self._log.error(" Remote location on server is mandatory to transfer the file")
        if local_path is None:
            self._log.error(" Local path is mandatory to transfer the file from remote server")

        sftp_client.chdir(remote_path)
        latest = 0
        latest_file = None
        for file_attr in sftp_client.listdir_attr():
            if file_attr.filename.startswith(file_name) and file_attr.st_mtime > latest:
                latest = file_attr.st_mtime
                latest_file = file_attr.filename
            else:
                pass
        if latest_file is not None:
            sftp_client.get(remote_path + latest_file, local_path + latest_file)
        else:
            self._log.error("File does not exist or Not matched")
        return latest_file

    def execute_commands_on_shell(self, channel, inputcommands):
        if channel is None:
            channel = self.get_channel_for_new_session()
        stdin = channel.makefile("wb")
        stdout = channel.makefile("rb")
        stdin.write(inputcommands)
        time.sleep(30)
        stdout.close()
        stdin.close()

    def release_resources(self):
        self.__ssh_client.close()

    def sftp_remove_file(self, sftp_client, remote_path, file_name):
        if sftp_client is None:
            sftp_client = self.open_sftp_connection()
        if remote_path is None:
            self._log.error(" Remote location on server is mandatory to transfer the file")
        try:
            sftp_client.chdir(remote_path)
            for file_attr in sftp_client.listdir_attr():
                if file_attr.filename == file_name:
                    sftp_client.remove(remote_path+file_name)
        except:
            pass #  Remote path does not exitst to delete old files
