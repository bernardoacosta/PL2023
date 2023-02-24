def percorreTexto():
	flag=True
	soma=0
	recebido=""

	while (recebido != "="):
		recebido=input("")

		if recebido.upper()=="ON" and flag==False:
			flag=True

		elif recebido.upper()=="OFF" and flag==True:
			flag=False


		elif recebido.isnumeric() and flag==True:
			soma += int(recebido)

		elif recebido.isalpha() and flag==False:
			flag=True

		elif recebido.isalpha() and flag==True:
			flag=True 

		else:
			if recebido != "=":
				print("Insira o sinal = para observar o resultado da soma caso a leitura esteja ou tenha estado ativada. Caso contrário, esta será 0.")

	return soma


def main():
	print(percorreTexto())

main()
