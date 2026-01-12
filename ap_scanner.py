import os
import subprocess
import time
import re
import signal

class AP_Scanner:
	def __init__(self):
		self.blocked_domain = []
		self.network_interface = ""
		self.ap_interface = ""
		self.hostapd_process = None
		self.dnsmasq_process = None
		self.ap_name = "Test"
		self.ap_password = "12345678"

	def write_hostapd_conf(self):
		hostapd_conf = f"interface={self.ap_interface}\nhw_mode=g\nchannel=7\nwmm_enabled=0\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP\nssid={self.ap_name}\nwpa_passphrase={self.ap_password}\nctrl_interface=/var/run/hostapd\nctrl_interface_group=0\n"
		with open("hostapd.conf", "w") as file:
			file.write(hostapd_conf)

	def start_ap(self):
		os.system(f"sudo nmcli dev set {self.ap_interface} managed no")
		os.system("sudo systemctl stop hostapd")
		os.system("sudo systemctl disable hostapd")
		os.system("sudo systemctl mask hostapd")
		os.system("sudo pkill -9 dnsmasq")
		os.system("sudo pkill -9 hostapd")
		os.system(f"sudo ip link set {self.ap_interface} down")
		os.system(f"sudo ip link set {self.ap_interface} up")
		time.sleep(1)

		# Reset wireless interface and release dnsmasq leases
		os.system("sudo rm -f /var/lib/misc/dnsmasq.leases")
		os.system(f"sudo ip link set {self.ap_interface} down")
		os.system("sudo ip addr flush dev " + self.ap_interface)
		os.system(f"sudo ip link set {self.ap_interface} up")
		time.sleep(1)
		self.write_hostapd_conf()
		os.system("sudo ip addr add 192.168.50.1/24 dev " + self.ap_interface)
		os.system("sudo ip link set " + str(self.ap_interface) + " up")
		self.hostapd_process = subprocess.Popen(["sudo", "hostapd", "-B", "./hostapd.conf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		time.sleep(3)

		dnsmasq_command = ["sudo", "dnsmasq", "--interface=" + self.ap_interface, "--bind-interfaces", "--dhcp-range=192.168.50.10,192.168.50.200,1h"]
		print("BLOCKED DOMAINS: " + str(self.blocked_domain))
		for domain in self.blocked_domain:
			if(self.blocked_domain != [""]):
				dnsmasq_command.append("--address=/" + str(domain) + "/0.0.0.0")
		print("dnsmasq_command: " + str(dnsmasq_command))
		self.dnsmasq_process = subprocess.Popen(dnsmasq_command)

		time.sleep(2)

		os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null")

		os.system("sudo iptables -t nat -A POSTROUTING -o " + self.network_interface + " -j MASQUERADE")
		os.system("sudo iptables -A FORWARD -i " + self.ap_interface + " -o " + self.network_interface + " -j ACCEPT")
		os.system("sudo iptables -A FORWARD -i " + self.network_interface + " -o " + self.ap_interface + " -m state --state RELATED,ESTABLISHED -j ACCEPT")

	def monitor_client(self):
		mac_list = []
		result = subprocess.run(["sudo", "hostapd_cli", "-i", self.ap_interface, "all_sta"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
		macs = re.findall(r"([0-9a-f]{2}(:[0-9a-f]{2}){5})", result.stdout, re.I)
		if macs:
			for mac in macs:
				mac_list.append(mac[0].lower())
		return mac_list

	def stop_ap(self):
		#self.hostapd_process.terminate()
		#self.dnsmasq_process.terminate()
		os.system("sudo pkill -9 dnsmasq")
		os.system("sudo pkill -9 hostapd")
		os.system("sudo iptables -t nat -D POSTROUTING -o " + self.network_interface + " -j MASQUERADE")
		os.system("sudo iptables -D FORWARD -i " + self.ap_interface + " -o " + self.network_interface + " -j ACCEPT")
		os.system("sudo iptables -D FORWARD -i " + self.network_interface + " -o " + self.ap_interface + " -m state --state RELATED,ESTABLISHED -j ACCEPT")

		os.system("sudo ip addr flush dev " + self.ap_interface)
		print("[+] Cleanup done")



"""scanner = AP_Scanner(["facebook.com", "youtube.com"], "wlan0", "wlan2")
scanner.start_ap()
time.sleep(10)
result = scanner.monitor_client()
print(result)
time.sleep(10)
result = scanner.monitor_client()
print(result)
scanner.stop_ap()"""