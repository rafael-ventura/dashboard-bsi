import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribuicao_ingresso(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='FORMA_INGRESSO_SIMPLES', data=df)
    plt.title('Distribuição de Cotistas e Não-Cotistas')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('Quantidade')
    plt.show()

def plot_evasao_sexo(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='FORMA_EVASAO_SIMPLES', hue='SEXO', data=df)
    plt.title('Distribuição de Evasões por Sexo')
    plt.xlabel('Forma de Evasão')
    plt.ylabel('Quantidade')
    plt.show()

def plot_evasao_idade(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[df['STATUS_EVASAO'] == 'Evasão']['IDADE'], kde=True)
    plt.title('Distribuição de Idades dos Alunos com Evasão')
    plt.xlabel('Idade')
    plt.ylabel('Quantidade')
    plt.show()

def analise_ingresso_evasao(df):
    print("\nIniciando Análise de Ingresso e Evasão...")
    plot_distribuicao_ingresso(df)
    plot_evasao_sexo(df)
    plot_evasao_idade(df)

if __name__ == "__main__":
    df = pd.read_csv('../dados/processado/dfPrincipal.csv')
    analise_ingresso_evasao(df)
