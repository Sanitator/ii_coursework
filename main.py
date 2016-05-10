import sys
import socket
import encryption
import struct
from questions import answer

def main():

    sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    UDP_port = 10000
    
    while True:
        try: 
            sUDP.bind(('', UDP_port))
            break
            
        except socket.error, msg:
            if (UDP_port < 10101):
                UDP_port = UDP_port + 1
            else:
                print("Socket error with UDP bind", msg)
                break
    
    host = socket.gethostbyname('ii.virtues.fi')
    my_ip = socket.gethostbyname(socket.gethostname())

    key_table = []
    for i in range(20):
        key_table.append(encryption.generateKey(64))
            
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sTCP.connect((host, 10000))
    helo_msg = "HELO " + str(UDP_port)
    #for i in range(len(key_table)):
    #    helo_msg = helo_msg + key_table[i] + "\r\n"
    #helo_msg = helo_msg + ".\r\n"
    
    #print helo_msg
    
    helo_msg = helo_msg +"\r\n"
    
    sTCP.sendall(helo_msg)
    

    reply = sTCP.recv(1024)
    #key_list = sTCP.recv(4096)
    port = int(reply.split()[1])
    print(reply, "port", port)
    #print "key list before modification"
    #print key_list
    #key_list = key_list.split()[:-1]
    #print "server send:"
    #print key_list
    
    #Apparently we can't use two sockets here for UDP
    #sUDP_tosend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ini_msg = "Ekki-ekki-ekki-ekki-PTANG.\r\n"
    data = struct.pack("!??HH64s", False, True, len(ini_msg), 0, ini_msg)
    
    sUDP.sendto(data, ((host, port)))
    print("udp message should be sent now")
    
    EOM = False
    while not EOM:
        reply2, addr = sUDP.recvfrom(4096)

        #print reply2
        uncoded = struct.unpack("!??HH64s", reply2)
        #print "uncoded"
        #print uncoded

        EOM = uncoded[0]
        print "EOM is: "
        print EOM

        question = uncoded[4].lstrip('/x00')
        
        
        print "question"
        print question

        #decrypted = encryption.decrypt(question, key_list[0])
        
        #print decrypted
        
        answ = answer(question)

        print "answ"
        print answ
        
        data = struct.pack("!??HH64s", False, True, len(answ), 0, answ)
        sUDP.sendto(data, ((host, port)))
        
        #EOM = True

    sUDP.close()
    sTCP.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting down"
        sys.exit(1)
