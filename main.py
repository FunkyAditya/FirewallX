import subprocess
import time
import re
from collections import defaultdict

class AutoFirewall:
    def __init__(self, max_attempts=5, time_window=60, log_file="/var/log/auth.log"):
        self.max_attempts = max_attempts
        self.time_window = time_window
        self.log_file = log_file
        self.connection_attempts = defaultdict(list)

    def reset_rules(self):
        subprocess.run(["iptables", "-F"])
        subprocess.run(["iptables", "-X"])
        print("Firewall rules reset.")

    def block_ip(self, ip):
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        print(f"Automatically blocked IP: {ip}")

    def monitor_log(self):
        with subprocess.Popen(["tail", "-F", self.log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            try:
                for line in proc.stdout:
                    ip = self.extract_ip(line)
                    if ip:
                        self.log_connection_attempt(ip)
                        if len(self.connection_attempts[ip]) > self.max_attempts:
                            self.block_ip(ip)
                            del self.connection_attempts[ip]
            except KeyboardInterrupt:
                print("Stopping firewall monitoring.")

    def extract_ip(self, log_entry):
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', log_entry)
        return match.group(0) if match else None

    def log_connection_attempt(self, ip):
        current_time = time.time()
        self.connection_attempts[ip].append(current_time)
        self.connection_attempts[ip] = [
            t for t in self.connection_attempts[ip] if current_time - t <= self.time_window
        ]

firewall = AutoFirewall(max_attempts=5, time_window=60)
firewall.reset_rules()
firewall.monitor_log()