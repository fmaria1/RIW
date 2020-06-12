import socket
from my_queue import coada,Q
#din Laboratorul 6
def extract_html_page(url,domain,ip,adress):
    client = "RIWEB_CRAWLER"
    port = 80
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, port))
    client.settimeout(1)
    request = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\n\r\n".format(url, domain, client)
    client.send(request.encode())

    firstline_size = 16
    buffer = bytearray()
    buffer.extend(client.recv(firstline_size))
    if len(buffer) == 0:
        return
    buffer = bytes(buffer)
    firstline = buffer.decode('utf-8', errors="ignore")

    data = b''
    if '200 OK' in firstline:
        buffer_size = 4096
        data1 = b''
        while True:
            part = client.recv(buffer_size)
            data1 += part
            if b'</html>' in part.lower() or len(part) == 0:
                break
        data = data1
        data = buffer + data
        data = data.decode('utf-8')
        data_to_store = data[data.find('\r\n\r\n'):]
        coada[adress]['explorat'] = True
        return data_to_store
    else:
        data = data + buffer
        buffer_size = 4096
        data1 = b''
        while True:
            part = client.recv(buffer_size)
            data1 += part
            if b'</html>' in part.lower() or len(part) == 0:
                break
        data += data1
        data = data.decode('utf-8')
        if '301' in firstline:
            for header in data.split('\r\n'):
                if 'Location' in header:
                    new_location = header.split(': ')[1]
                    if coada[adress]['retry'] <= 5:
                        coada[adress]['retry'] += 1
                        coada[adress]['explorat'] = True
                        coada[new_location] = {'explorat': False, 'retry': coada[adress]['retry']}
                        Q.append(new_location)
        if '307' in firstline:
            for header in data.split('\r\n'):
                if 'Location' in header:
                    new_location = header.split(': ')[1]
                    if coada[adress]['retry'] <= 5:
                        coada[adress]['retry'] += 1
                        coada[adress]['explorat'] = True
                        coada[new_location] = {'explorat': False, 'retry': coada[adress]['retry']}
                        Q.append(new_location)
        if '302' in firstline:
            for header in data.split('\r\n'):
                if 'Location' in header:
                    new_location = header.split(': ')[1]
                    if coada[adress]['retry'] <= 5:
                        coada[adress]['retry'] += 1
                        coada[adress]['explorat'] = True
                        coada[new_location] = {'explorat': False, 'retry': coada[adress]['retry']}
                        Q.append(new_location)
        if ('500' in firstline) or ('501' in firstline) or ('502' in firstline) or ('503' in firstline) or ('504' in firstline) or ('505' in firstline) or('506' in firstline) or ('507' in firstline) or ('509' in firstline) or ('510' in firstline) or ('511' in firstline):
            if coada[adress]['retry'] < 5:
                Q.append(adress)
                coada[adress]['retry'] += 1
            else:
                coada[adress]['explorat'] = True

