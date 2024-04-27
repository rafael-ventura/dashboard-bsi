import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_performance_academica(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise de Performance Acadêmica...")

    plot_comparacao_cra(dataframe)
    plot_correlacao_cra_distancia(dataframe)
    plot_evasao_cra(dataframe)
    plot_comparacao_distribuicao_cra_violin(dataframe)

    print("\nAnálise de Performance Acadêmica Concluída!")


def plot_comparacao_cra(dataframe):
    sns.boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe)
    plt.title('Distribuição do CRA por Forma de Ingresso')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('comparacao_cra')


def plot_correlacao_cra_distancia(dataframe):
    df_filtrado = dataframe.dropna(subset=['DISTANCIA_URCA'])

    plt.figure(figsize=(6, 4))

    sns.heatmap(df_filtrado[['CRA', 'DISTANCIA_URCA']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlação entre CRA e Distância até a Urca')
    salvar_grafico('correlacao_cra_distancia_urca')


def plot_evasao_cra(dataframe):
    sns.boxplot(x='STATUS_EVASAO', y='CRA', data=dataframe)
    plt.title('CRA por Status de Evasão')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('evasao_cra')


def plot_comparacao_distribuicao_cra_violin(dataframe):
    sns.violinplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe)
    plt.title('Distribuição do CRA entre Diferentes Formas de Ingresso')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('distribuicao_cra_violin')


if __name__ == "__main__":
    df = carregar_dados()
    analise_performance_academica(df)
