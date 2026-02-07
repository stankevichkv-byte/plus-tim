#!/usr/bin/env python3
"""Restart docker build with fixed requirements"""
import paramiko

SERVER = "194.67.127.153"
PORT = 22
USERNAME = "root"
PASSWORD = "eBd3Et72O880BHx0"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SERVER, PORT, USERNAME, PASSWORD, timeout=30)

# Kill old processes
print("[*] Killing old docker-compose processes...")
stdin, stdout, stderr = client.exec_command("pkill -9 -f 'docker-compose' 2>/dev/null; pkill -9 -f 'pip install' 2>/dev/null; sleep 2")
print(stdout.read().decode('utf-8')[:200])

# Pull latest code
print("\n[*] Pulling latest code...")
stdin, stdout, stderr = client.exec_command("cd /root/plus-tim && git pull origin main 2>&1")
print("Git:", stdout.read().decode('utf-8')[:500])

# Clean Docker cache and restart build
print("\n[*] Cleaning Docker build cache...")
client.exec_command("docker builder prune -af 2>&1")

print("\n[*] Restarting docker-compose build with no cache...")
cmd = "cd /root/plus-tim && nohup docker-compose build --no-cache > /tmp/docker_build3.log 2>&1 & echo 'Build started'"
stdin, stdout, stderr = client.exec_command(cmd)
print("Result:", stdout.read().decode('utf-8'))

client.close()
print("\n[+] Build restarted! Check /tmp/docker_build2.log")