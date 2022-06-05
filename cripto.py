import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#pip install cryptography
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f'ESSA É A CHAVE DE CRIPTOGRAFIA:    {key}    !!!!!!!!!!!!!!!!')

#file = open('../encrypt/chave.txt', 'wb') #write/bytes
#file.write(key)  
#file.close()c

with open(os.path.join(sys.path[0], "chave.txt"), "wb") as f:
    f.write(key)
    f.close()


# Leitura da planilha
## INSIRA A PLANILHA NA PASTA E ALTERE O CAMINHO ABAIXO
tabelaPrinc = pd.read_csv("Listagem alunos por curso - atual.csv", sep=',')
tabelaPrinc

idCol = tabelaPrinc['ID_PESSOA']
nomeCol = tabelaPrinc['NOME_PESSOA']
matriculaCol = tabelaPrinc['MATR_ALUNO']
cpfCol = tabelaPrinc['CPF_MASCARA']

#adicionando na  variavel f a chave que será usada para criptografar
f = Fernet(key)

# cria array para receber as colunas criptografadas
idCriptCol = []
nomeCriptCol = []
matriculaCriptCol = []
cpfCriptCol = []

# criptografa as colunas linha por linha
# todas as linhas estão preenchidas, portanto, mesmo tamanho para todos.

#ID
for id in idCol:
    idCodificado = str(id).encode()
    cripto = f.encrypt(idCodificado)
     #criptoString = cripto.decode('utf-8')
    idCriptCol.append(cripto)
#NOME
for nome in nomeCol:
    nomeCodificado = nome.encode()
    cripto = f.encrypt(nomeCodificado)
    #criptoString = cripto.decode('utf-8')
    nomeCriptCol.append(cripto)
#MATRICULA
for matricula in matriculaCol:
    matriculaCodificado = str(matricula).encode()
    cripto = f.encrypt(matriculaCodificado)
    #criptoString = cripto.decode('utf-8')
    matriculaCriptCol.append(cripto)
#CPF
for cpf in cpfCol:
    cpfCodificado = cpf.encode()
    cripto = f.encrypt(cpfCodificado)
    #criptoString = cripto.decode('utf-8')
    cpfCriptCol.append(cripto)   


#limpa a tabela para inserir novamente
tabelaCriptografada = tabelaPrinc

#insere colunas criptografadas
tabelaCriptografada['ID_PESSOA'] = idCriptCol
tabelaCriptografada['NOME_PESSOA'] = nomeCriptCol
tabelaCriptografada['MATR_ALUNO'] = matriculaCriptCol
tabelaCriptografada['CPF_MASCARA'] = cpfCriptCol

tabelaCriptografada

temp = tabelaCriptografada  
temp.to_excel('planilhaCriptografada.xlsx', index = False, header=True)
