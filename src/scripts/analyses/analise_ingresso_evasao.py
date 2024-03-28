import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_distribuicao_ingresso(df):
    sns.countplot(x='FORMA_INGRESSO_SIMPLES', data=df)
    plt.title('Distribuição de Cotistas e Não-Cotistas')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('Quantidade')


def plot_evasao_sexo(df):
    sns.countplot(x='FORMA_EVASAO', hue='SEXO', data=df)
    plt.title('Distribuição de Evasões por Sexo')
    plt.xlabel('Forma de Evasão')
    plt.ylabel('Quantidade')


def plot_evasao_idade(df):
    sns.histplot(df[df['STATUS_EVASAO'] == 'Evasão']['IDADE'], kde=True)
    plt.title('Distribuição de Idades dos Alunos com Evasão')
    plt.xlabel('Idade')
    plt.ylabel('Quantidade')


def analise_ingresso_evasao(df, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    print("\nIniciando Análise de Ingresso e Evasão...")
    plot_distribuicao_ingresso(df)
    plot_evasao_sexo(df)
    plot_evasao_idade(df)


if __name__ == "__main__":
    df = pd.read_csv('../dados/processado/dfPrincipal.csv')
    analise_ingresso_evasao(df)
