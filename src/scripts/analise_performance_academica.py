import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from src.utils.utils import criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_performance_academica(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise de Performance Acadêmica...")

    plot_distribuicao_cra_arredondado(dataframe)
    plot_comparacao_cra(dataframe)
    plot_media_ponderada_cra_distancia_forma_ingresso(dataframe)
    plot_evasao_cra(dataframe)
    plot_comparacao_distribuicao_cra_violin(dataframe)

    print("\nAnálise de Performance Acadêmica Concluída!")


def plot_distribuicao_cra_arredondado(dataframe):
    """
    Plota a distribuição do CRA arredondado
    :param dataframe: DataFrame com os dados
    :return: None
    """
    plt.figure(figsize=(12, 6))

    sns.histplot(dataframe['CRA'].round(1), bins=40, kde=True, color="crimson")
    plt.title('Distribuição do CRA Arredondado')
    plt.xlabel('CRA Arredondado')
    plt.ylabel('Quantidade de Alunos')

    plt.xticks(ticks=np.arange(0, 11, 1))
    plt.grid(True)
    plt.tight_layout()

    salvar_grafico('distribuicao_cra_arredondado')


def plot_comparacao_cra(dataframe):
    sns.boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe)
    plt.title('Distribuição do CRA por Forma de Ingresso')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('comparacao_cra')


def plot_media_cra_por_idade(dataframe):
    plt.figure(figsize=(12, 6))

    ordenado = dataframe.groupby('IDADE_INGRESSO')['CRA_ARREDONDADO'].mean().reset_index().sort_values('IDADE_INGRESSO')
    sns.barplot(x='IDADE_INGRESSO', y='CRA_ARREDONDADO', data=ordenado, palette='inferno')  # 'viridis'
    plt.title('Média de CRA por Idade de Ingresso')
    plt.xlabel('Idade de Ingresso')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()

    salvar_grafico('media_cra_por_idade')


def plot_media_ponderada_cra_distancia_forma_ingresso(dataframe):
    # Definir os intervalos de distância
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    labels = [f'{int(left)}-{int(right)}' for left, right in zip(bins[:-1], bins[1:])]

    # Categorizar 'DISTANCIA_URCA' em intervalos
    dataframe['DISTANCIA_INTERVALO'] = pd.cut(dataframe['DISTANCIA_URCA'], bins=bins, labels=labels, right=False)

    # Função para calcular a média ponderada
    def ponderada(x):
        d = {'CRA_PONDERADO': (x['CRA_ARREDONDADO'] * x['QUANTIDADE']).sum() / x['QUANTIDADE'].sum()}
        return pd.Series(d, index=['CRA_PONDERADO'])

    # Adicionar uma coluna 'QUANTIDADE' para representar o número de alunos em cada entrada
    dataframe['QUANTIDADE'] = 1

    # Calcular média ponderada de CRA por intervalo de distância e forma de ingresso
    media_cra_ponderada = dataframe.groupby(['DISTANCIA_INTERVALO', 'FORMA_INGRESSO_SIMPLES']).apply(
        ponderada).unstack()

    # Cria o gráfico de barras agrupadas
    media_cra_ponderada.plot(kind='bar', figsize=(12, 6), y='CRA_PONDERADO')
    plt.title('Média de CRA Arredondado Ponderado por Intervalo de Distância e Forma de Ingresso')
    plt.xlabel('Intervalo de Distância até a Urca (km)')
    plt.ylabel('Média de CRA Arredondado Ponderado')
    plt.legend(title='Forma de Ingresso Simples', labels=[col[1] for col in media_cra_ponderada.columns])
    plt.xticks(rotation=45)
    plt.tight_layout()

    salvar_grafico('media_cra_distancia_forma_ingresso_ponderado')


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


def plot_media_cra_por_distancia(dataframe):
    plt.figure(figsize=(12, 6))

    ordenado = dataframe.groupby('DISTANCIA')[
        'CRA_ARREDONDADO'].mean().reset_index().sort_values('DISTANCIA')
    sns.barplot(x='DISTANCIA', y='CRA_ARREDONDADO', data=ordenado, color="darkgreen")
    plt.title('Média de CRA por Distância')
    plt.xlabel('Distância')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()

    salvar_grafico('media_cra_por_distancia')


if __name__ == "__main__":
    df = carregar_dados()
    analise_performance_academica(df)
