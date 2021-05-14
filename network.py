import time
import uuid
import socket
import pickle
import threading

NAME = socket.gethostname()
sleep_timeout = 0.1

class Message:
    def __init__(self, content, args, id):
        self.content = content
        self.args = args
        self.id = id
        self.mode = 0

    def __str__(self):
        return str(self.content)

    def reply(self, content, socket):
        msg = Message(content, self.id)
        msg.mode = 1
        time.sleep(sleep_timeout)
        socket.socket.send(pickle.dumps(Bytes(msg)))
        time.sleep(sleep_timeout)
        socket.socket.send(pickle.dumps(msg))
        time.sleep(sleep_timeout)

class Bytes:
    def __init__(self, message):
        self.bytes = len(pickle.dumps(message))

    def __str__(self):
        return str(self.bytes)

    def __int__(self):
        return self.bytes

class Connection:
    def __init__(self, conn, addr):
        self.socket = conn
        self.addr = addr
        self.close = conn.close
        self.messages = {}
        self.bytes = 5000
        self.data = bytearray()
        self.socket.setblocking(0)
        self.looking_for = []

    def send(self, content, *args, id=None):
        if not id:
            id = str(uuid.uuid4())

        msg = Message(content, args, id)
        time.sleep(sleep_timeout)
        self.socket.send(pickle.dumps(Bytes(msg)))
        time.sleep(sleep_timeout)
        self.socket.send(pickle.dumps(msg))
        time.sleep(sleep_timeout)
        return msg

    def recv(self, id=None):
        if id:
            self.looking_for.append(id)

        while 1:
            try:
                packet = self.socket.recv(self.bytes)
            except socket.error as e:
                if "blocking" in str(e):
                    packet = bytearray()
                else:
                    raise e

            self.data.extend(packet)

            if id and id in self.messages:
                obj = self.messages[id]
                self.messages.pop(id)
                return obj

            try:
                msg = pickle.loads(self.data)
                self.data = bytearray()

                if type(msg) == Bytes:
                    self.bytes += msg.bytes

                elif type(msg) == Message:
                    if not id:
                        if msg.id not in self.looking_for:
                            return msg
                    else:
                        if msg.id == id:
                            self.looking_for.remove(id)
                            return msg
                        else:
                            self.messages[msg.id] = msg

            except:
                pass

    def sendrecv(self, content, id=None):
        msg = self.send(content, id=id)
        msg = self.recv(msg.id)
        return msg.content, msg.args

class Server:
    def __init__(self, port, host=''):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.clients = []

    def run(self, handle_client):
        self.socket.listen()

        while 1:
            try:
                conn, addr = self.socket.accept()
            except:
                continue

            client = Connection(conn, addr)
            self.clients.append(client)
            threading.Thread(target=handle_client, args=(client,)).start()

    def kick(self, conn):
        if conn in self.clients:
            self.clients.remove(conn)

        try:
            conn.close()
        except:
            pass

class Client:
    def __init__(self, port, host=''):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostbyname(host), port))
        self.close = self.socket.close
        self.messages = {}
        self.bytes = 5000
        self.data = bytearray()
        self.socket.setblocking(0)
        self.looking_for = []

    def send(self, content, *args, id=None):
        if not id:
            id = str(uuid.uuid4())

        msg = Message(content, args, id)
        time.sleep(sleep_timeout)
        self.socket.send(pickle.dumps(Bytes(msg)))
        time.sleep(sleep_timeout)
        self.socket.send(pickle.dumps(msg))
        time.sleep(sleep_timeout)
        return msg

    def recv(self, id=None):
        if id:
            self.looking_for.append(id)

        while 1:
            try:
                packet = self.socket.recv(self.bytes)
            except socket.error as e:
                if "blocking" in str(e):
                    packet = bytearray()
                else:
                    raise e

            self.data.extend(packet)

            if id and id in self.messages:
                obj = self.messages[id]
                self.messages.pop(id)
                return obj

            try:
                msg = pickle.loads(self.data)
                self.data = bytearray()

                if type(msg) == Bytes:
                    self.bytes += msg.bytes

                elif type(msg) == Message:
                    if not id:
                        if msg.id not in self.looking_for:
                            return msg
                    else:
                        if msg.id == id:
                            self.looking_for.remove(id)
                            return msg
                        else:
                            self.messages[msg.id] = msg

            except:
                pass

    def sendrecv(self, content, *args, id=None):
        msg = self.send(content, *args, id=id)
        msg = self.recv(msg.id)
        return msg.content, msg.args
