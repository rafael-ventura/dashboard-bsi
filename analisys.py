import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#pip install cryptography
from cryptography.fernet import Fernet
import re


#le o arquivo com planilha 
tabelaPrinc = pd.read_excel("planilhaCriptografada.xlsx")

#faz limpeza nas colunas
colunas = ['SEXO', 'DT_NASCIMENTO', 'FORMA_INGRESSO',
       'FORMA_EVASAO', 'COD_CURSO', 'NOME_UNIDADE', 'NUM_VERSAO',
       'PERIODO_INGRESSO', 'DT_EVASAO', 'PERIODO_EVASAO']
tabelaPrinc = tabelaPrinc.filter(colunas)


#divide o campo de evasao em ano e periodo
tabelaPrinc[['ANO_EVASAO', 'PERIODO_EVASAO']] = tabelaPrinc['PERIODO_EVASAO'].str.split('/', expand=True)
tabelaPrinc = tabelaPrinc[['SEXO', 'DT_NASCIMENTO', 'FORMA_INGRESSO',
       'FORMA_EVASAO', 'COD_CURSO', 'NOME_UNIDADE', 'NUM_VERSAO',
       'PERIODO_INGRESSO', 'DT_EVASAO', 'ANO_EVASAO','PERIODO_EVASAO']]
#formatando o campo periodo
linhasPeriodoEvasao = tabelaPrinc['PERIODO_EVASAO']
colunaSemestre = []
for linha in linhasPeriodoEvasao:
  colunaSemestre.append(re.sub('\D', '', str(linha)))
tabelaPrinc['PERIODO_EVASAO'] = colunaSemestre

#transforma coluna em valor numerico
colSem = tabelaPrinc['PERIODO_EVASAO'] 
tabelaPrinc['PERIODO_EVASAO'] = pd.to_numeric(colSem)



#divide o campo de ingresso em ano e periodo
tabelaPrinc[['ANO_INGRESSO', 'PERIODO_INGRESSO']] = tabelaPrinc['PERIODO_INGRESSO'].str.split('/', expand=True)
tabelaPrinc = tabelaPrinc[['SEXO', 'DT_NASCIMENTO', 'FORMA_INGRESSO',
       'FORMA_EVASAO', 'COD_CURSO', 'NOME_UNIDADE', 'NUM_VERSAO',
       'ANO_INGRESSO',  'PERIODO_INGRESSO', 'DT_EVASAO', 
       'ANO_EVASAO','PERIODO_EVASAO']]

#formatando o campo periodo
linhasPeriodoIngresso = tabelaPrinc['PERIODO_INGRESSO']
colunaSemestre = []
for linha in linhasPeriodoIngresso:
  colunaSemestre.append(re.sub('\D', '', str(linha)))
tabelaPrinc['PERIODO_INGRESSO'] = colunaSemestre

#transforma coluna em valor numerico
colSem = tabelaPrinc['PERIODO_INGRESSO'] 
tabelaPrinc['PERIODO_INGRESSO'] = pd.to_numeric(colSem)

#group by por ano e período
ocorrencias = tabelaPrinc.groupby(['ANO_INGRESSO','PERIODO_INGRESSO']).size().reset_index(name='ALUNOS')


#Numero de Alunos por ano de 2001 até 2021
cases = [1000, 2000, 5000, 8000, 15000, 6000]
plt.figure( figsize=(16, 10)) # alterar tamanho
plt.bar(ocorrencias['ANO_INGRESSO'], ocorrencias['ALUNOS'])
plt.ylabel('Numero de Alunos')
plt.xlabel('Anos')

plt.show()


X = ['Group A','Group B','Group C','Group D']
Ygirls = [10,20,20,40]
Zboys = [20,30,25,30]
  
X_axis = np.arange(len(X))
 
plt.bar(X_axis -  0.2 , Ygirls, 0.4, label = '1 Semestre')
plt.bar(X_axis +  0.2, Zboys, 0.4, label = '2 Semestre')
  
plt.xticks(X_axis, X)
plt.xlabel("Groups")
plt.ylabel("Number of Students")
plt.title("Number of Students in each group")
plt.legend()

plt.show()



