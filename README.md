
# Objective - Penetration Testing
![image](https://user-images.githubusercontent.com/87882680/127826958-e6fe0b07-2ea1-4244-980b-30dbde22b486.png)


The Multiple Client Remote Access Tool was created in order to target the linux and windows operating system and perform reconnaissance with its main purpose of serving as a staging ground for further payloads and the extraction of notable files which are essential in information gathering.  


# Features 
- **Access to the target's terminal** and thus, the execution of an array of shell commands, most notably displaying directories and files, opening files such as further payloads, altering file structure, displaying network configurations and connections.
- **Send any file** to the target machine which allows for further tools and paylods to be present on the victim's machine, which can be executed through issuing system commands. 
- **Download files** which can contain valuable information vital to the operation.
- **Persistence** on windows which allows for continuous acces to the machine.
- **Multiple clients** are also supported, allowing for an array of target machines to be monitored and exploited.
# Usage
The server.py can be hosted on your machine however, I have tested this on servers provideed by external providers and have thus far, encounted no errors and bugs that hinder the operational capabilities of the RAT. Most importantly, client.py will always try to establish connection with the server without prompting errors that delay successive commands, enabling the hosting servers to be turned off when not in use which can decrease operational costs.
