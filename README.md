
![addtext_com_MDM0NDMyNDg1Mw](https://user-images.githubusercontent.com/87882680/147547214-cfe53580-ff7c-4312-bf2b-ae2feecd0697.png)

 [![jigmi - PyCryptRAT-MultiClientEncryptedRAT](https://img.shields.io/static/v1?label=jigmi&message=PyCryptRAT-MultiClientEncryptedRAT&color=black&logo=github)](https://github.com/jigmi/PyCryptRAT-MultiClientEncryptedRAT "Go to GitHub repo")
[![stars - PyCryptRAT-MultiClientEncryptedRAT](https://img.shields.io/github/stars/jigmi/PyCryptRAT-MultiClientEncryptedRAT?style=social)](https://github.com/jigmi/PyCryptRAT-MultiClientEncryptedRAT)   [![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT) [![Python 3.9.9](https://img.shields.io/badge/python-3.9.9-black.svg)](https://www.python.org/downloads/release/python-399/)

# Secure Penetration Testing
![Capture](https://user-images.githubusercontent.com/87882680/147556303-10b22a09-8694-4e61-b3e0-16314f66e960.PNG)


The Multiple Client Remote Access Tool was created in order to target the linux and windows operating system and perform reconnaissance with its main purpose of serving as a staging ground for further payloads and the extraction of notable files which are essential in information gathering. The **Diffie Hellman** key exchanged is performed between the server and the client in order to securely transfer keys, where then commands and data from files are encrypted with **AES 256 bit symmetric encryption** in order to protect sensitive data. 



 __Features__
- **Diffie Hellman key exchange and the AES 256 bit encryption of all data and commands sent between the server and client** This includes the encryption of file data along with the decryption of it, all commands are also encrypted to prevent MITM attacks.
- **Access to the target's terminal** and thus, the execution of an array of shell commands, most notably displaying directories and files, opening files such as further payloads, altering file structure, displaying network configurations and connections.
- **Multiple clients** are also supported, allowing for an array of target machines to be monitored and exploited.
- **Send any file** to the target machine which allows for further tools and paylods to be present on the victim's machine, which can be executed through issuing system commands. 
- **Download files** which can contain valuable information vital to the operation.
- **Persistence** on windows which allows for continuous acces to the machine.

__Commands__
| Command for Greater Console | Description |
| --- | --- |
| list | List all active connections to the server along with their selection number, ip address and portnumber |
| select number | select 0 will select the first active connection to the server.py |
| total | displays the total number of connections |
| quit | closes all connections to the server and exits
| help | displays all available commands |

| Commands for selection clients | Description |
| --- | --- |
| all terminal commands are available as access is given to the client's terminal, so cd, del, ipconfig and more are available |
| download_file | downloads file from given path from the client machine |
| send_file | sends a file from the control machine to the client |
| quit | closes the connection with the client and exits to the greater console | 
| help | displays available commands |


__Usage__

The server.py can be hosted on your machine however, I have tested this on servers provideed by external providers and have thus far, encounted no errors and bugs that hinder the operational capabilities of the RAT. Most importantly, client.py will always try to establish connection with the server without prompting errors that delay successive commands, enabling the hosting servers to be turned off when not in use which can decrease operational costs.

__Dependancies__

Pycryptodomex
```
pip install pycryptodomex
```
__Disclaimer__

This project should only be used for authorised testing or educational purposes only.
