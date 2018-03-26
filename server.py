import socket
import os
import sys
import time
import random

def processar_arquivo (file_name):
	print "\tProcessing ...\n"
	time.sleep(2)
	dados = ["cadeira", "caneca", "barco", "mesa", "jurema"]
	return random.choice (dados)



HOST = '127.0.0.1'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(4)

while True:
	print "-----------------\n\tWainting for connections\n"
	con, addr = tcp.accept()
	fname = "arquivo_recebido" + str(addr)+".jpg"
	arq = open(fname, "wb")
	dados = None


	print "\tOnline with "+ str (addr)

	while dados <> "\x18" :
		dados = con.recv(1024)
		if dados.count("EndOF"):
			dados = dados.replace("EndOF", "")
			if len(dados)> 0:
				arq.write(dados)
			arq.close()
			print "\tProcessando Arquivo\n"
			con.send(processar_arquivo(fname))
			break
		if not dados:
			break
		arq.write(dados)
	con.close()
	print "\nFinished\n\n"
