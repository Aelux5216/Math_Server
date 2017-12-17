import asyncore
import socket
import copy
import cx_Oracle

#Test data
testsym = "Bob"
testcomp = "Bobbers"
testprice = 120.33
testquant = 100

connection = cx_Oracle.connect('SYSTEM/12345@xe') #Connect to the database
cursor = connection.cursor() #Create instance that allows me to enter commands
'''
query = str.format("INSERT INTO DATABASE (SYMBOL, COMPANY, PRICE, QUANTITY) VALUES ('{0}', '{1}', '{2}', '{3}')", testsym,testcomp,testprice,testquant) #How to run a sql command
cursor.execute(query) #Run the query
connection.commit() #Save changes to the database
'''

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)

        data2 = data.decode('ascii')

        if data2:
            if data2 == "RequestDB":
                query = "SELECT * FROM DATABASE"
                cursor.execute(query)
                for row in cursor:
                    for cell in row:
                        cellF = str.format("{0}$",cell)
                        self.send(cellF.encode())
            else:
                self.send(data2)
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

server = EchoServer('localhost', 8000)
asyncore.loop()
