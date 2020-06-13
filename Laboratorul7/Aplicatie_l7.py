import http.client
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import socket
import datetime
import os
#initializations
coada = ["http://riweb.tibeica.com/crawl/"]
my_var = 0
dstPath = 'output'
#functions
def isabsolute(url):
    return bool(urlparse(url).netloc)

def extract_html_page(target_host):
    global my_var
    target_host2 = urlparse(target_host).netloc
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)
    if not (os.path.isdir(os.path.join(dstPath,target_host2))):
        os.mkdir(os.path.join(dstPath,target_host2))
    client = "RIWEB_CRAWLER"
    target_port = 80
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host2, target_port))

    request = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\n\r\n".format(target_host, target_host2, client)

    client.send(request.encode())
    #din lab6
    CHUNK_SIZE = 16
    buffer = bytearray()
    buffer.extend(client.recv(CHUNK_SIZE))
    firstline = buffer.decode()
    data = b''
    # verificarea codului de stare (daca acesta este cod de eroare, se va deschide un fisier text în care se va
    # scrie cererea initiala si raspunsul  serverului);
    if '200 OK' in firstline:
        buffer_size = 4096
        data1 = b''
        while True:
            part = client.recv(buffer_size)
            data1 += part
            if b'</html>' in part.lower() or len(part) == 0:
                break
        data = data1
        data = data.decode()
        data_lower = data.lower()
        if data_lower.find('<!doctype') > -1:
            data_to_store = data[data_lower.find('<!doctype'):data_lower.find('</html>') + 8]
        else:
            data_to_store = data[data_lower.find('<html'):data_lower.find('</html>') + 8]
            # salvarea continutului raspunsului (corpul mesajului – pagina html) într-un fisier html
        with open('my_page.html', 'w') as file:
            file.write(data_to_store)
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
        with open('error_page.txt', 'w') as file:
            file.write(data.decode())
        pass

def crawler(start_time):
    counter = 0
    for L in coada:
        page = extract_html_page(L)
        if page is not None:
            getpage_soup = BeautifulSoup(page, 'html.parser')
            metas = getpage_soup.find_all('meta')
            page_flag = False
            link_flag = False
            #rep local
            for meta in metas:
                if meta.get('name') == 'robots':
                    if 'all' in meta.get('content') or 'index' in meta.get('content'):
                        page_flag = True
                    if 'all' in meta.get('content') or 'follow' in meta.get('content'):
                        link_flag = True

            if not any(meta.get('name') == 'robots' for meta in metas):
                page_flag, link_flag = True, True
            if page_flag == True:
                path = L.split('http://')[1]
                path = path.split('/')
                current_path = os.path.join(os.getcwd(), dstPath)
                for var in path[:-1]:
                    if (os.path.isdir(os.path.join(current_path, var))):
                        current_path = os.path.join(current_path,var)
                    else:
                        current_path = os.path.join(current_path,var)
                        os.mkdir(current_path)
                if path[-1] == '':
                    nume_fisier = 'index.html'
                else:
                    nume_fisier = path[-1]
                with open('{}\{}.html'.format(current_path,nume_fisier.split('.')[0]), 'w') as file:
                    file.write(page)
            if link_flag == True:
                a_tags = getpage_soup.find_all('a',href = True)
                for a_tag in a_tags:
                    link = a_tag['href']
                    if bool(urlparse(link).netloc) == True:
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
        timeb = datetime.datetime.now()
        cycle = (timeb - start_time).seconds

        if counter == 100:
            break
        else:
            counter += 1
        print("Got: ", counter, " pages in ", cycle, "sec")
        
if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print('Start')
    crawler(start_time)
    print('Stop')
