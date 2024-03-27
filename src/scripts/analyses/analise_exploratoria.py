import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def estatisticas_descritivas(df):
    print("\nEstatísticas Descritivas:")
    print(df.describe(include='all'))

def plot_distribuicao_CRA(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['CRA'], kde=True)
    plt.title('Distribuição do CRA')
    plt.xlabel('CRA')
    plt.ylabel('Frequência')
    plt.show()

def plot_distribuicao_sexo(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='SEXO', data=df)
    plt.title('Distribuição por Sexo')
    plt.xlabel('Sexo')
    plt.ylabel('Quantidade')
    plt.show()

def plot_distribuicao_idade(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['IDADE'], kde=True)
    plt.title('Distribuição por Idade')
    plt.xlabel('Idade')
    plt.ylabel('Quantidade')
    plt.show()

def plot_distribuicao_evasao(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='FORMA_EVASAO_SIMPLES', data=df)
    plt.title('Distribuição de Evasões')
    plt.xlabel('Forma de Evasão')
    plt.ylabel('Quantidade')
    plt.show()

def analise_exploratoria(df):
    print("\nIniciando Análise Exploratória...")
    estatisticas_descritivas(df)
    plot_distribuicao_CRA(df)
    plot_distribuicao_sexo(df)
    plot_distribuicao_idade(df)
    plot_distribuicao_evasao(df)

if __name__ == "__main__":
    df = pd.read_csv('../dados/processado/dfPrincipal.csv')
    analise_exploratoria(df)
