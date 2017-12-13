import asyncore
import socket
import copy
import cx_Oracle as cx_Oracle

command = ""
commandSize = 0
dataSize = 0

commandSizeArray = 7
dataSizeArray = 50

testsym = "Bob"
testcomp = "Bobbers"
testprice = 120.33
testquant = 100

connection = cx_Oracle.connect('SYSTEM/12345@xe')
cursor = connection.cursor()
query = str.format("INSERT INTO DATABASE (SYMBOL, COMPANY, PRICE, QUANTITY) VALUES ({0}, {1}, {2}, {3}",testsym,testcomp,testprice,testquant)
cursor.execute(query)

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)
        else:
            pass

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("listening..")

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print ("Incoming connection from {0}",repr(addr))
            handler = EchoHandler(sock)

server = EchoServer('localhost', 8080)
asyncore.loop()