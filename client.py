import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

arquivo = raw_input ("Digite o arquivo a ser enviado, para teste aperte enter \n")
#Utiliza arquivo de teste
if arquivo == '':
	arquivo = "./arquivo_teste.jpg"
	fp = open(arquivo, "rb")

	for line in fp.readlines():
		tcp.send(line)
	tcp.send("EndOF")
	print "------------\n+++++  Recebendo Resposta ++++\n------------"
	x = tcp.recv(512)
	print ("\n\t => Resultado = " + str (x))
	tcp.close()
	print "\nConection Closed."
	

#utiliza arquivo existente
else:
	fp = open(arquivo, "rb")

	for line in fp.readlines():
		tcp.send(line)
	tcp.send("EndOF")
	print "------------\n+++++  Recebendo Resposta ++++\n------------"
	x = tcp.recv(512)
	print ("\n\t => Resultado = " + str (x))
	tcp.close()
	print "\nConection Closed."

	pass
