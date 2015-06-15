import socket
import sys
from urlparse import urlparse
import logging


class ProxyServer(object):

    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port
        self.s_sock = None
        self.logger = logging.getLogger()

    def start(self):
        self.s_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.s_sock.bind(("127.0.0.1", 8080))
        self.s_sock.listen(5)
        self.logger.info("Starting proxy server")

    def run(self):
        while True:
            c_sock, addr = self.s_sock.accept()
            c_sock = ClientSocket(c_sock, addr)
            c_sock.run()

    def shutdown(self):
        self.s_sock.close()
        self.logger.info("Closed sever socket")


class ClientSocket(object):

    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.read_bytes = ""
        self.logger = logging.getLogger()

    def run(self):
        self.logger.info("New socket created at %s:%s", self.sock, self.addr)

        while True:
            bytes = self.sock.recv(1024)
            self.read_bytes += bytes
            if self.discovered_dest_server():
                break

    def shutdown(self):
        self.sock.close()
        self.logger.info("Closed sever socket")

    def extract_dest_server(self):
        chunks = self.read_bytes.split("\r\n")
        print chunks
        # split_request_line = chunks[0].split()
        # domain = split_request_line[1]
        for chunk in chunks:
            if chunk.startswith("Host:"):
                host_head = chunk.split()
                domain = host_head[1]
                self.logger.info("Received domain. It is %s", domain)

    def discovered_dest_server(self):
        return self.extract_dest_server() is not None

def run_proxy():
    logger = logging.getLogger()

    proxy_server = ProxyServer("127.0.0.1", 8080)
    try:
        proxy_server.start()
        proxy_server.run()
    except Exception as e:
        logger.exception(e)

        proxy_server.shutdown()
        sys.exit(-1)


    # raw_request = clientsocket.recv(1024)
    # logger.info("Received message: %s", raw_request)

    # clientsocket.send("Received: " + raw_request)
    # logger.info("Message echoed to client")

    # method, url, protocol = request_parser(raw_request)

    # reply = fwd_connection(raw_request, url)
    # logger.info("Reply is: \n%s", reply)

    # clientsocket.send(reply)
    # logger.info("Reply sent to client")

    # kill_socket(clientsocket)


def main():
    logger = logging.getLogger()
    log_fmt = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    level = logging.INFO

    logging.basicConfig(level=level, format=log_fmt)
    logger = logging.getLogger()

    run_proxy()



def fwd_connection(raw_request, url):
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    ex_ip = socket.gethostbyname(url)
    s.connect((ex_ip, 80))
    s.send(raw_request)
    reply = s.recv(2048)
    logger.info("Received reply of length %s", len(reply))
    kill_socket(s)
    return reply


# def request_parser(raw_request):
#     split_request_line = raw_request.split()
#     fmt_url = urlparse(split_request_line[1])
#     split_request_line[1] = fmt_url[1]
#     return split_request_line[0:3]


# def kill_socket(sock_name):
#     sock_name.shutdown(1)
#     logger.info("Socket is shutdown but listening")
#     sock_name.close()
#     logger.info("Socket is closed")

if __name__ == '__main__':
    main()
