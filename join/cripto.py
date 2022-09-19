import encodings
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#pip install cryptography
from cryptography.fernet import Fernet

from join import df_join

# Cria uma chave aleatória através do método da biblioteca Fernet
def criarChave():
    key = Fernet.generate_key()
    print(f'Chave de criptografia criada.')
    return key
# Cria arquivo para armazenar a chave
def criarArquivo():
    with open(os.path.join(sys.path[0], "chave.key"), "wb") as f:
        f.write(criarChave())
        f.close()
    print('Arquivo chave.key criado na pasta.')
# Acessa a chave que estará contida no arquivo chave.key
def getChave():
    return open('chave.key', 'rb').read()

#Programa
print("Algoritmo de criptografia")
criarArquivo()
f = Fernet(getChave())

idCol = df_join['ID_PESSOA']
nomeCol = df_join['NOME_PESSOA']
matriculaCol = df_join['MATR_ALUNO']
cpfCol = df_join['CPF_MASCARA']

idCriptCol = []
nomeCriptCol = []
matriculaCriptCol = []
cpfCriptCol = []

    #ID
for id in idCol:
    idCodificado = str(id).encode()
    idCripto = f.encrypt(idCodificado) 
    #cripto = f.encrypt(idCodificado)
    #criptoString = cripto.decode('utf-8')
    idCriptCol.append(idCripto)
#NOME
for nome in nomeCol:
    nomeCodificado = nome.encode()
    nomeCripto = f.encrypt(nomeCodificado)
    #cripto = f.encrypt(nomeCodificado)
    #criptoString = cripto.decode('utf-8')
    nomeCriptCol.append(nomeCripto)
#MATRICULA
for matricula in matriculaCol:
    matriculaCodificado = str(matricula).encode()
    matriculaCripto = f.encrypt(matriculaCodificado)
    #cripto = f.encrypt(matriculaCodificado)
    #criptoString = cripto.decode('utf-8')
    matriculaCriptCol.append(matriculaCripto)
#CPF
for cpf in cpfCol:
    cpfCodificado = cpf.encode()
    cpfCripto = f.encrypt(cpfCodificado)
    #cripto = f.encrypt(cpfCodificado)
    #criptoString = cripto.decode('utf-8')
    cpfCriptCol.append(cpfCripto) 

tabelaCriptografada = df_join

#insere colunas criptografadas
tabelaCriptografada['ID_PESSOA'] = idCriptCol
tabelaCriptografada['NOME_PESSOA'] = nomeCriptCol
tabelaCriptografada['MATR_ALUNO'] = matriculaCriptCol
tabelaCriptografada['CPF_MASCARA'] = cpfCriptCol

tabelaCriptografada

temp = tabelaCriptografada  
temp.to_excel('planilhaJoinCriptografada.xlsx', index = True, header=True)
print('Planilha Criptografada criada e adicionada na pasta!')


# cria array para receber as colunas criptografadas
idCol = tabelaCriptografada['ID_PESSOA']
nomeCol = tabelaCriptografada['NOME_PESSOA']
matriculaCol = tabelaCriptografada['MATR_ALUNO']
cpfCol = tabelaCriptografada['CPF_MASCARA']

idDescriptCol = []
nomeDescriptCol = []
matriculaDescriptCol = []
cpfCriptDescCol = []

for id in idCol:
    aux = f.decrypt(id)
    print(aux)
    idDescriptCol.append(int((aux).decode('utf-8')))

for nome in nomeCol:
    aux = f.decrypt(nome)
    nomeDescriptCol.append(aux.decode('utf-8'))

for matricula in matriculaCol:
    aux = f.decrypt(matricula)
    matriculaDescriptCol.append(aux.decode('utf-8'))

for cpf in cpfCol:
    aux = f.decrypt(cpf)
    cpfCriptDescCol.append(aux.decode('utf-8')) 

tabelaDescriptografada = tabelaCriptografada

tabelaDescriptografada['ID_PESSOA'] = idDescriptCol
tabelaDescriptografada['NOME_PESSOA'] = nomeDescriptCol
tabelaDescriptografada['MATR_ALUNO'] = matriculaDescriptCol
tabelaDescriptografada['CPF_MASCARA'] = cpfCriptDescCol

temp = tabelaDescriptografada  
temp.to_excel('planilhaJoinDescriptografada.xlsx', index = True, header=True)
print('Planilha Descriptografada criada e adicionada na pasta!')
