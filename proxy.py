import signal
import asyncio 
import os
class ProxyProtocol(asyncio.DatagramProtocol):
    def __init__(self, proxy):
        self.proxy = proxy

    def connection_made(self, transport):
        self.proxy.transport = transport

    def datagram_received(self, data, addr):
        if addr == (self.proxy.dest_host, self.proxy.dest_port):
            # Message from server
            self.proxy.handle_server_message(data, self.proxy.client_addr)
        else:
            # Message from client
            self.proxy.client_addr = addr
            self.proxy.handle_client_message(addr, data)

class Proxy:
    def __init__(self, dest, r_port=9999):
        self.dest_host, self.dest_port = dest.split(':')
        self.dest_port = int(self.dest_port)
        print(f"Proxying {self.dest_host}:{self.dest_port} to port {r_port}")
        self.r_port = r_port
        self.transport = None
        self.client_addr = None

    def handle_client_message(self, client_addr, data):
        data = self.parse_d(data, 'client', sys.stdout)
        # Forward the message to the destination server
        self.transport.sendto(data, (self.dest_host, self.dest_port))

    def handle_server_message(self, data, client_addr):
        data = self.parse_d(data, 'server', sys.stdout)
        # Send the response back to the client
        self.transport.sendto(data, client_addr)


    def modify(self,data, src):
        if src == 'server':
            pass #
        else :
            pass
        return data
    max_string=100
    def parse_d(self,data, src, fd):
        d = self.modify(data, src)
        spaces = self.max_string - len(d)
        if spaces < 0:
            spaces = 0
        # print(f"[{src}] {str(d.hex()).ljust(70)} | {d.decode('utf-8', 'ignore').rstrip('\n')}")
        fd.write(f"[{src}] {str(d.hex()).ljust(70)} | {d.decode('utf-8', 'ignore').rstrip('\n')} \n")
        return d


    async def listen_client(self):
        print(f"Listening on port {self.r_port}")
        loop = asyncio.get_running_loop()
        await loop.create_datagram_endpoint(
            lambda: ProxyProtocol(self),
            local_addr=("0.0.0.0", self.r_port)
        )
        on_close = asyncio.Future()
        await on_close

    async def start(self):
        self.set_ip_tables_rules()
        await self.listen_client()

    def set_ip_tables_rules(self):
        print("Setup Ip table rules")
        # uid of user proxyuser 
        proxy_user_uid =  os.getuid()
        print(f" UID {proxy_user_uid}")
        # redirect client packets to proxy server
        os.system(f"sudo iptables -t nat -A OUTPUT -m owner  ! --uid-owner {proxy_user_uid} -p udp --dport {self.dest_port} -d {self.dest_host} -j REDIRECT --to-ports {self.r_port}")
        # redirect server packets to proxy server
        os.system(f"sudo iptables -t nat -A PREROUTING -p udp -s {self.dest_host} --sport {self.dest_port} -j  DNAT --to-destination {self.dest_host}:{self.dest_port}")

        # allow forwarding 
        os.system(f"sudo iptables -A FORWARD -p udp --dport {self.r_port} -j ACCEPT")
        os.system(f"sudo sysctl -w net.ipv4.ip_forward=1")
        
    def flush_ip_tables_rules(self):
        print("Cleaning Iptables rules")
        os.system("sudo iptables -t nat -F")
        os.system("sudo iptables -t nat -X")
        os.system("sudo iptables -F")
        os.system("sudo iptables -X")
        os.system("sudo iptables -P INPUT ACCEPT")
        os.system("sudo iptables -P FORWARD ACCEPT")
        os.system("sudo iptables -P OUTPUT ACCEPT")
        os.system("sudo iptables -t mangle -F")  
        os.system("sudo iptables -t mangle -X")
        exit(0)


import sys 
def main():
    
    if len(sys.argv)  < 2:
        print("Usage: python proxy.py <server_host:server_port>")
        sys.exit(1)
    

    proxy = Proxy(sys.argv[1], 9999)
    signal.signal(signal.SIGINT, lambda s, f: proxy.flush_ip_tables_rules())
    asyncio.run(proxy.start())


if __name__ == "__main__":
    main()
    