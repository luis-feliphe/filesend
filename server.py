import socket
import os
import sys
import time
import random
import subprocess

def processar_arquivo (file_name):
	answer_file = file_name.replace(".jpg",".txt")
	os.system("./darknet detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights " + str (file_name) + " >> "+ str (answer_file))
	#subprocess.check_output(["./darknet", "detector", "test", "cfg/coco.data","cfg/yolov3.cfg", "yolov3.weights", file_name,">>", answer_file])
	resultado = open (answer_file, "r")
	retorno = ""	
	for linha in resultado.readlines():
		retorno += str(linha)
	return retorno



HOST = '150.165.138.39'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(4)

while True:
	print "-----------------\n\tWainting for connections\n"
	con, addr = tcp.accept()
	fname = "arquivo_recebido" + str(addr)+".jpg"
	fname = fname.replace("(","").replace(")","").replace("'","").replace(",","").replace(".","").replace("jpg",".jpg").replace(" ","")
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
			print ("O NOME DO ARQUIVO \n\n" + fname + "\n\n")
			con.send(processar_arquivo(fname))
			break
		if not dados:
			break
		arq.write(dados)
	con.close()
	print "\nFinished\n\n"
