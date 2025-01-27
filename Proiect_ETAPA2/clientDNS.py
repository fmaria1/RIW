#imports
import codecs
import socket
import bitstring, struct # For constructing and destructing the DNS packet.
import datetime
#functions

def int_string_to_hex(val):
  result = "0"
  if val.__class__.__name__ == "int" and val >= 0:
    result = hex(val)
    if val < 16:
      result = "0" + result[2:]
  elif val.__class__.__name__ == "str":
    result = "".join([hex(ord(y))[2:] for y in val])
  return "0x" + result

def resolve_host_name(host_name_to):

  host_name_to = host_name_to.split(".")

  DNS_QUERY_FORMAT = [
      "hex=id"
    , "bin=flags"
    , "uintbe:16=qdcount"
    , "uintbe:16=ancount"
    , "uintbe:16=nscount"
    , "uintbe:16=arcount"
  ]

  DNS_QUERY = {
      "id": "0x1a2b"
    , "flags": "0b0000000100000000"
    , "qdcount": 1
    , "ancount": 0
    , "nscount": 0
    , "arcount": 0
  }

  j = 0

  for i, _ in enumerate(host_name_to):

    host_name_to[i] = host_name_to[i].strip()

    DNS_QUERY_FORMAT.append("hex=" + "qname" + str(j))

    DNS_QUERY["qname" + str(j)] = int_string_to_hex(len(host_name_to[i]))

    j += 1

    DNS_QUERY_FORMAT.append("hex=" + "qname" + str(j))

    DNS_QUERY["qname" + str(j)] = int_string_to_hex(host_name_to[i])

    j += 1

  # Add a terminating byte.

  DNS_QUERY_FORMAT.append("hex=qname" + str(j))

  DNS_QUERY["qname" + str(j)] = int_string_to_hex(0)

  # End QNAME.

  # Set the type and class now.

  DNS_QUERY_FORMAT.append("uintbe:16=qtype")

  DNS_QUERY["qtype"] = 1 # For the A record.

  DNS_QUERY_FORMAT.append("hex=qclass")

  DNS_QUERY["qclass"] = "0x0001" # For IN or Internet.

  # Convert the struct to a bit string.

  data = bitstring.pack(",".join(DNS_QUERY_FORMAT), **DNS_QUERY)

  # Send the packet off to the server.

  DNS_IP = "8.8.8.8" # Google public DNS server IP.
  DNS_PORT = 53 # DNS server port for queries.

  READ_BUFFER = 1024 # The size of the buffer to read in the received UDP packet.

  address = (DNS_IP, DNS_PORT) # Tuple needed by sendto.

  client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP.

  client.sendto(data.tobytes(), address) # Send the DNS packet to the server using the port.

  # Get the response DNS packet back, decode, and print out the IP.

  # Get the response and put it in data. Get the responding server address and put it in address.

  data, address = client.recvfrom(READ_BUFFER)

  # Convert data to bit string.
  data2 = data
  data = bitstring.BitArray(bytes=data)

  # Unpack the receive DNS packet and extract the IP the host name resolved to.

  # Get the host name from the QNAME located just past the received header.

  host_name_from = []

  # First size of the QNAME labels starts at bit 96 and goes up to bit 104.
  # size|label|size|label|size|...|label|0x00

  x = 96
  y = x + 8

  for i, _ in enumerate(host_name_to):

    # Based on the size of the very next label indicated by
    # the 1 octet/byte before the label, read in that many
    # bits past the octet/byte indicating the very next
    # label size.

    # Get the label size in hex. Convert to an integer and times it
    # by 8 to get the number of bits.

    increment = (int(str(data[x:y].hex), 16) * 8)

    x = y
    y = x + increment

    # Read in the label, converting to ASCII.

    host_name_from.append(codecs.decode(data[x:y].hex, "hex_codec").decode())

    # Set up the next iteration to get the next label size.
    # Assuming here that any label size is no bigger than
    # one byte.

    x = y
    y = x + 8 # Eight bits to a byte.

  # Get the response code.
  # This is located in the received DNS packet header at
  # bit 28 ending at bit 32.

  response_code = str(data[28:32].hex)

  result = {'host_name': None, 'ip_address': None,'expire':None}

  # Check for errors.

  if (response_code == "0"):
    #print(data2)
    result['host_name'] = ".".join(host_name_from)


    result['ip_address'] = ".".join([
        str(data[-32:-24].uintbe)
      , str(data[-24:-16].uintbe)
      , str(data[-16:-8].uintbe)
      , str(data[-8:].uintbe)
    ])

    # Assemble the IP address the host name resolved to.
    # It is usually the last four octets of the DNS
    # packet--at least for A records.



    result['expire'] = (data[-80:-48]).uintbe
  elif (response_code == "1"):

    print("\nFormat error. Unable to interpret query.\n")
    return None

  elif (response_code == "2"):

    print("\nServer failure. Unable to process query.\n")
    return None

  elif (response_code == "3"):
    print(host_name_to)
    print("\nName error. Domain name does not exist.\n")
    return None

  elif (response_code == "4"):

    print("\nQuery request type not supported.\n")
    return None

  elif (response_code == "5"):

    print("\nServer refused query.\n")
    return None

  timp_curent = datetime.datetime.now()
  if result['expire'] is not None:
    timp_extras = datetime.timedelta(seconds=result['expire'])
    timp_curent = timp_curent + timp_extras
    result['expire'] = timp_curent
  return result

def DNSServer(HOST_NAME):
  result = resolve_host_name(HOST_NAME)
  return result

def Cache_DNS(HOST_NAME,adresses):
  adress_size = len(adresses)
  if (adress_size == 0):
    adresses = DNSServer(HOST_NAME)
    if adresses is None:
      return None

  else:
    if adresses['expire'] is not None:
      if adresses['expire'] < datetime.datetime.now():
        adresses = DNSServer(HOST_NAME)
  return adresses


