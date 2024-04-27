import encodings
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cryptography.fernet import Fernet
from join import juntar_planilhas


# Cria uma chave aleatória através do método da biblioteca Fernet
def criar_chave() -> bytes:
    chave = Fernet.generate_key()
    print('Chave de criptografia criada.')
    return chave


# Cria arquivo para armazenar a chave
def criar_arquivo_chave():
    with open(os.path.join(sys.path[0], "chave.key"), "wb") as f:
        f.write(criar_chave())
    print('Arquivo chave.key criado na pasta.')


# Acessa a chave que estará contida no arquivo chave.key
def obter_chave() -> bytes:
    return open('chave.key', 'rb').read()


# Programa
def criptografar_coluna(df: pd.DataFrame, coluna: str, f: Fernet) -> list:
    coluna_cript = []
    for valor in df[coluna]:
        valor_codificado = str(valor).encode()
        valor_cripto = f.encrypt(valor_codificado)
        coluna_cript.append(valor_cripto)
    return coluna_cript


def criar_planilha_criptografada(df: pd.DataFrame):
    criar_arquivo_chave()
    f = Fernet(obter_chave())

    colunas_para_criptografar = ['ID_PESSOA', 'NOME_PESSOA', 'MATR_ALUNO', 'CPF_MASCARA']
    for coluna in colunas_para_criptografar:
        df[coluna] = criptografar_coluna(df, coluna, f)

    df.to_excel('planilhaJoinCriptografada.xlsx', index=True, header=True)
    print('Planilha Criptografada criada e adicionada na pasta.')


def main():
    print("Algoritmo de criptografia")
    nome_planilha1, nome_planilha2 = input(
        "Digite o nomes das duas planilhas separado por vírgula ('ex: alunos_bsi, endereco_cra_bsi') :").split(',')
    # Juntar as duas planilhas em um DataFrame
    df = juntar_planilhas(nome_planilha1, nome_planilha2)
    # Crie a planilha criptografada a partir do DataFrame
    criar_planilha_criptografada(df)


if __name__ == "__main__":
    main()
