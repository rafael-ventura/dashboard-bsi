import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import plotar_grafico_linha, criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_temporal(dataframe):
    """
    Realiza análise temporal sobre a evolução do CRA, a variação média acumulada do CRA,
    a tendência de ingresso ao longo dos anos e a variação da média do CRA por tipo de ingresso.
    """
    print("\nIniciando Análise Temporal...")

    evolucao_media_cra(dataframe)
    variacao_media_cra_acumulada(dataframe)
    plot_tendencia_ingresso(dataframe)
    variacao_media_cra_por_tipo_ingresso(dataframe)

    print("\nAnálise Temporal Concluída!")


def evolucao_media_cra(dataframe):
    """
    Analisa a evolução da média do CRA ao longo dos períodos de ingresso.
    """
    media_cra_por_periodo = dataframe.groupby('PERIODO_INGRESSO_FORMATADO')['CRA'].mean().reset_index()
    plotar_grafico_linha(x='PERIODO_INGRESSO_FORMATADO', y='CRA', data=media_cra_por_periodo,
                         titulo='Evolução da Média do CRA por Período', xlabel='Período de Ingresso', ylabel='Média do CRA')
    salvar_grafico('evolucao_media_cra')


def variacao_media_cra_acumulada(dataframe):
    """
    Mostra a variação acumulada da média do CRA por período de ingresso.
    """
    df_sorted = dataframe.sort_values('PERIODO_INGRESSO_FORMATADO')
    df_acumulada = df_sorted.groupby('PERIODO_INGRESSO_FORMATADO')['CRA'].expanding().mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_acumulada, x='PERIODO_INGRESSO_FORMATADO', y='CRA')
    plt.title('Variação da Média do CRA Acumulada por Período')
    plt.xlabel('Período de Ingresso')
    plt.ylabel('Média do CRA Acumulada')
    plt.xticks(rotation=45)
    salvar_grafico('variacao_media_cra_acumulada')


def plot_tendencia_ingresso(dataframe):
    """
    Analisa a tendência de ingresso no curso ao longo dos anos, separada por forma de ingresso.
    """

    tendencia_ingresso = dataframe.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(
        name='Quantidade')

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=tendencia_ingresso, x='ANO_PERIODO_INGRESSO', y='Quantidade', hue='FORMA_INGRESSO_SIMPLES',
                 marker='o')
    plt.title('Tendência de Ingresso no Curso ao Longo dos Anos por Forma de Ingresso')
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Número de Alunos Ingressantes')
    plt.xticks(rotation=45)  # Rotação dos labels no eixo X para melhor visualização
    plt.legend(title='Forma de Ingresso')
    salvar_grafico('tendencia_ingresso_por_forma')


def variacao_media_cra_por_tipo_ingresso(dataframe):
    """
    Mostra a variação da média do CRA por tipo de ingresso ao longo dos períodos.
    """
    df_por_tipo = dataframe.groupby(['FORMA_INGRESSO_SIMPLES', 'PERIODO_INGRESSO_FORMATADO'])[
        'CRA'].mean().reset_index()
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_por_tipo, x='PERIODO_INGRESSO_FORMATADO', y='CRA', hue='FORMA_INGRESSO_SIMPLES')
    plt.title('Variação da Média do CRA por Tipo de Ingresso ao Longo dos Períodos')
    plt.xlabel('Período de Ingresso')
    plt.ylabel('Média do CRA')
    plt.xticks(rotation=45)
    salvar_grafico('variacao_media_cra_tipo_ingresso')


if __name__ == "__main__":
    df = carregar_dados()
    analise_temporal(df)
