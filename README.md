# filesend

Este é o repositório de duas aplicações cliente servidor. Abaixo está a descrição de cada aplicação.

server.py: o lado servidor da aplicação é responsável por receber um arquivo e realizar algum tipo de processamento (que neste caso é abstrato, a ser substituído no método processar_arquivo).

client.py: A aplicação cliente deve indicar qual arquivo será enviado ao servidor e esperar a resposta do servidor contendo o resultado do processamento por meio de uma string.
