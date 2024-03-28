import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_comparacao_cra(df):
    sns.boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=df)
    plt.title('Distribuição do CRA entre Cotistas e Não-Cotistas')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')


def plot_correlacao_cra(df):
    correlacoes = df[['CRA', 'IDADE']].corr()
    print("\nCorrelações entre CRA e Idade:")


def plot_evasao_cra(df):
    sns.boxplot(x='STATUS_EVASAO', y='CRA', data=df)
    plt.title('CRA por Status de Evasão')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA')


def analise_performance_academica(df, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    print("\nIniciando Análise de Performance Acadêmica...")
    plot_comparacao_cra(df)
    plot_correlacao_cra(df)
    plot_evasao_cra(df)

if __name__ == "__main__":
    df = pd.read_csv('../dados/processado/dfPrincipal.csv')
    analise_performance_academica(df)

