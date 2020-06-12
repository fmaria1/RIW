import http.client
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import socket
import datetime
import os
#initializations
coada = ["http://riweb.tibeica.com/crawl/"]
my_var = 0
#functions
def isabsolute(url):
    return bool(urlparse(url).netloc)

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

def read(client):
    CHUNK_SIZE = 36
    buffer = bytearray()
    buffer.extend(client.recv(CHUNK_SIZE))
    firstline = buffer[:buffer.find(b'\n')]
    firstline = buffer.decode()
    data = b''
    # print(target_host)
    # print(buffer)
    if '200 OK' in firstline:
        data = receive_data(client)
        data = data.decode()
        data_lower = data.lower()
        # print(data_lower.find('<!doctype'))
        if data_lower.find('<!doctype') > -1:
            data_to_store = data[data_lower.find('<!doctype'):data_lower.find('</html>') + 8]
        else:
            data_to_store = data[data_lower.find('<html'):data_lower.find('</html>') + 8]
        # client.close()
        with open('index.html','w') as file:
            print(data_to_store)
            file.write(data_to_store)
        return data_to_store
    else:
        data = data + buffer
        data += receive_data(client)
        with open('error_page.txt', 'w') as file:
            file.write(data.decode())
        pass

def extract_html_page(target_host):
    global my_var
    target_host2 = urlparse(target_host).netloc
    if not (os.path.isdir(os.path.join('work_directory',target_host2))):
        os.mkdir(os.path.join('work_directory',target_host2))
    client = "RIWEB_CRAWLER"
    target_port = 80
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host2, target_port))

    request = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\n\r\n".format(target_host, target_host2, client)

    client.send(request.encode())
    read(client)

def crawler():
    counter = 0
    for L in coada:
        #print(L)
        P = extract_html_page(L)
        if P is not None:
            getpage_soup = BeautifulSoup(P, 'html.parser')
            metas = getpage_soup.find_all('meta')
            permission1 = False
            permission2 = False
            for meta in metas:
                if meta.get('name') == 'robots':
                    if meta.get('content') == 'all' or meta.get('content') == 'index':
                        permission1 = True

                    if meta.get('content') == 'all' or meta.get('content') == 'follow':
                        permission2 = True
            if not any(meta.get('name') == 'robots' for meta in metas):
                permission1, permission2 = True, True
            if permission1 == True:
                path = L.split('http://')[1]
                path = path.split('/')
                current_path = os.path.join(os.getcwd(),'work_directory')
                for var in path[:-1]:
                    if (os.path.isdir(os.path.join(current_path,var))):
                        current_path = os.path.join(current_path,var)
                    else:
                        current_path = os.path.join(current_path,var)
                        os.mkdir(current_path)
                if path[-1] == '':
                    nume_fisier = 'index.html'
                else:
                    nume_fisier = path[-1]
                with open('{}\{}.html'.format(current_path,nume_fisier.split('.')[0]), 'w') as file:
                    file.write(P)
                    if counter > 99:
                        break
                    else:
                        counter += 1
            if permission2 == True:
                a_tags = getpage_soup.find_all('a',href = True)
                for a_tag in a_tags:
                    link = a_tag['href']
                    if isabsolute(link):
                        if link[:link.find(':')] == 'http' or link[:link.find(':')] == 'https':
                            link = link.split('#')[0]
                            if link not in coada:
                                coada.append(link)
                    else:
                        link = link.split('#')[0]
                        if '.' in L.split('/')[-1]:
                            #print('Da')
                            L = L.replace(L.split('/')[-1],'')
                        if L[-1] != '/':
                            L += '/'
                        #print(L)
                        link = L + link
                        if link not in coada:
                            coada.append(link)
    print(len(coada))
    print(coada)

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    crawler()
    print('A durat:', str(datetime.datetime.now() - start_time))