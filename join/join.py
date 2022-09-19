import pandas as pd

print("Algoritmo para Joins das Planilhas")
file_1, file_2 = input("Digite o nomes das duas planilhas separado por vírgula (ex: alunos_bsi, endereco_cra_bsi) :").split(',')
#file_2 = input("Digite o nome da planilha 2: //exemplo: 'endereco_cra'  :")
df_1 = pd.read_excel(f'{file_1.strip()}.xlsx')
df_2 = pd.read_excel(f'{file_2.strip()}.xlsx')


# print(df_1.head())
# print(df_2.head())

df_join = pd.merge( df_1, df_2, left_on='MATR_ALUNO', right_on='MATRICULA')

# Tratamento dos dados da planilha

columns = ['ID_PESSOA','NOME_PESSOA','SEXO',
    'DT_NASCIMENTO','FORMA_INGRESSO','FORMA_EVASAO',
    'MATR_ALUNO','NUM_VERSAO','PERIODO_INGRESSO',
    'DT_EVASAO','PERIODO_EVASAO','CPF_MASCARA',
    'CRA','BAIRRO','CIDADE','ESTADO']
df_join = df_join.filter(items=columns)

print(df_join.head())