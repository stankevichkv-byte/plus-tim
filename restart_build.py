import paramiko
import time

HOST = "194.67.127.153"
PORT = 22
USERNAME = "root"
PASSWORD = "eBd3Et72O880BHx0"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD, timeout=30)

    # Kill old docker-compose processes
    print("Killing old docker-compose processes...")
    stdin, stdout, stderr = client.exec_command("pkill -f docker-compose || true")
    time.sleep(2)

    # Kill any running pip install processes
    print("Killing pip install processes...")
    stdin, stdout, stderr = client.exec_command("pkill -f 'pip install' || true")
    time.sleep(2)

    # Clean up docker containers
    print("Cleaning up docker containers...")
    stdin, stdout, stderr = client.exec_command("docker-compose down --remove-orphans 2>/dev/null || true")

    # Navigate to project directory and pull latest code
    print("Pulling latest code...")
    stdin, stdout, stderr = client.exec_command("cd /root/plus-tim && git pull origin main")
    print("Git output:", stdout.read().decode())
    print("Git errors:", stderr.read().decode())

    # Start new build
    print("Starting new docker-compose build...")
    stdin, stdout, stderr = client.exec_command("cd /root/plus-tim && nohup docker-compose build --no-cache > /tmp/docker_build4.log 2>&1 & echo 'Build started'")
    print(stdout.read().decode())

    print("\nBuild started with log at /tmp/docker_build4.log")

finally:
    client.close()