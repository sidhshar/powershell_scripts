import paramiko

# === Configuration ===
firewall_ip = ""   # Replace with your Sophos XG IP
username = ""            # Replace with your username
password = ""    # Replace with your password

commands = {
    "Firmware version": "show version",
    "Pattern update interval": "show update schedule",
    "Admin timeout": "show advanced-firewall",
    "NTP servers": "show ntp",
    "WAN access": "show network-settings",
    "SNMP settings": "show snmp",
    "Syslog config": "show syslog",
    "IPS policies": "show ips-settings",
    "ATP settings": "show atp",
    "Heartbeat status": "show central-management",
}

def run_ssh_commands():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connecting to Sophos XG Firewall...")
    try:
        ssh.connect(firewall_ip, username=username, password=password, timeout=10)

        for label, command in commands.items():
            print(f"\n== {label} ==")
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode().strip())

        ssh.close()
    except Exception as e:
        print(f"[!] Connection failed: {e}")

if __name__ == "__main__":
    run_ssh_commands()
