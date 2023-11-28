import paramiko
import subprocess
import pytest

server_ip = '192.168.56.101'
password = '12345'
username = 'andrii'


@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, password=password)

    start_server_command = "iperf3 -s -p 5201 -1"
    _, stdout, stderr = ssh.exec_command(start_server_command)

    ssh.close()

    error_message = stderr.read().decode("utf-8")
    if error_message:
        pytest.fail(f"Error starting iperf server: {error_message}")

    return error_message


@pytest.fixture(scope='function')
def client(server):
    client_command = f"iperf3 -c {server_ip}"
    process = subprocess.Popen(client_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()

    if "connection failed" in error.decode("utf-8").lower():
        pytest.fail("Failed to connect to the iperf server")

    return output.decode("utf-8"), error.decode("utf-8")
