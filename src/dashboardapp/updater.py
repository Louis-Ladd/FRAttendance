import socket
import psutil
import threading

from threading import Thread

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
server_info = {"ip" : socket.gethostbyname(hostname), "hostname" : hostname, "cpu_usage" : [], "ram_usage" : []}
server_info["cpu_usage"].append(psutil.cpu_percent(4))
server_info["ram_usage"].append(psutil.virtual_memory().percent)

class updateThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = threading.Event()
        self.daemon = True

    def run(self):
        while not self.stopped.wait(0.25):
            #print(f"Thread {self.native_id}: Updating server_info...")
            server_info["cpu_usage"].append(psutil.cpu_percent(0))
            server_info["ram_usage"].append(psutil.virtual_memory().percent)