
import socket

#initializations
port = 80
address_1 = "http://riweb.tibeica.com/crawl/"
address_2 = "riweb.tibeica.com"
client = "CLIENT RIW"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#1 linia de cerere (metoda, resurs ˘ a, versiune protocol);
request = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\n\r\n".format(address_1,address_2,client)

#2 Deschiderea unei conexiuni TCP, port 80, catre hostul dorit
client.connect((address_2, port))

#3 Transmiterea cererii catre server, utilizând conexiunea stabilit ˘ a anterior
client.send(request.encode())

#functions

def receive_data(socket):
    buffer_size = 4096
    data = b''
    while True:
        part = socket.recv(buffer_size)
        print(len(part))
        data += part
        if  b'</html>' in part.lower() or len(part) == 0:
            break
    return data

# 4 Preluarea raspunsului HTTP oferit de catre server
def read():
    CHUNK_SIZE = 32  # you can set it larger or smaller
    buffer = bytearray()
    buffer.extend(client.recv(CHUNK_SIZE))
    firstline = buffer[:buffer.find(b'\n')]
    firstline = buffer.decode()
    data = b''
    #verificarea codului de stare (daca acesta este cod de eroare, se va deschide un fisier text în care se va
    # scrie cererea initiala si raspunsul  serverului);
    if '200 OK' in firstline:
        data = receive_data(client)
        data=data.decode()
        data_lower = data.lower()
        #print(data_lower.find('<!doctype'))
        if data_lower.find('<!doctype') > -1:
            data_to_store = data[data_lower.find('<!doctype'):data_lower.find('</html>') + 8]
        else:
            data_to_store = data[data_lower.find('<html'):data_lower.find('</html>') + 8]
            #salvarea continutului raspunsului (corpul mesajului – pagina html) într-un fisier html
        with open('my_page.html','w') as file:
            print(data_to_store)
            file.write(data_to_store)
    else:
        data = data + buffer
        data +=receive_data(client)
        with open('error_page.txt','w') as file:
            file.write(data.decode())
        pass

if __name__ == "__main__":
    read()
    #unde inchizi conexiunea?
