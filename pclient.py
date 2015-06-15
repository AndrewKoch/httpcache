import socket
import logging


def main():
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8080))
    outmsg = "Hello?"
    logger.info("Sending message: %s", outmsg)
    s.send(outmsg)
    msg = s.recv(1024)
    logger.info("Received message: %s", msg)
    s.shutdown(1)
    logger.info("Socket is shutdown but listening")
    s.close()
    logger.info("Socket is closed")

if __name__ == '__main__':
    logger = logging.getLogger()
    log_fmt = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    level = logging.INFO

    logging.basicConfig(level=level, format=log_fmt)
    logger = logging.getLogger()

    main()
