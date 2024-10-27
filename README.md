
# FirewallX

A simple Python-based firewall that automatically detects and blocks suspicious IPs based on failed login attempts, using iptables.

## Features 

* Real-time Monitoring: Tracks /var/log/auth.log for failed login attempts.

* Automatic Blocking: Blocks IPs with repeated failed attempts within a set time window.


## Usage

To run this tool. write open terminal and type :- 

```bash
    git clone https://github.com/FunkyAditya/FirewallX.git
    
    sudo python3 main.py
```

#### Your Firewall is ready to protect your network!!