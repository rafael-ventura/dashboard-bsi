import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.plots import salvar_grafico, plotar_grafico_linha, plotar_grafico_linha_ponderada
from src.utils.utils import carregar_dados


def analise_temporal(dataframe):
    """
    Realiza análise temporal sobre a evolução do CRA, a variação média acumulada do CRA,
    a tendência de ingresso ao longo dos anos e a variação da média do CRA por tipo de ingresso.
    """
    print("\nIniciando Análise Temporal...")

    plot_variacao_media_cra(dataframe)
    plot_variacao_media_acumulada_cra_periodo_ingresso(dataframe)
    plot_tendencia_ingresso(dataframe)
    plot_tendencia_evasao(dataframe)
    plot_variacao_media_cra_acumulada(dataframe)
    plot_variacao_media_cra_forma_ingresso(dataframe)
    plot_variacao_media_cra_forma_evasao(dataframe)
    plot_variacao_media_ponderada_cra_forma_ingresso(dataframe)
    plot_variacao_media_ponderada_cra_forma_evasao(dataframe)

    print("\nAnálise Temporal Concluída!")


def plot_variacao_media_cra(dataframe):
    """
    Analisa a variação da média do CRA ao longo dos períodos de ingresso.
    """
    media_cra_por_periodo = dataframe.groupby('PERIODO_INGRESSO_FORMATADO')['CRA'].mean().reset_index()
    plotar_grafico_linha(x='PERIODO_INGRESSO_FORMATADO', y='CRA', data=media_cra_por_periodo,
                         titulo='Variação da Média do CRA por Período',
                         xlabel='Período de Ingresso', ylabel='Média do CRA')
    salvar_grafico('variacao_media_cra')


def plot_variacao_media_cra_acumulada(dataframe):
    """
    Mostra a variação acumulada da média do CRA por período de ingresso.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    dataframe['CRA_ACUMULADA'] = dataframe.sort_values('PERIODO_INGRESSO_FORMATADO') \
        .groupby('PERIODO_INGRESSO_FORMATADO')['CRA'] \
        .expanding().mean().values
    plotar_grafico_linha(x='PERIODO_INGRESSO_FORMATADO', y='CRA_ACUMULADA', data=dataframe,
                         titulo='Variação Acumulada da Média do CRA por Período',
                         xlabel='Período de Ingresso', ylabel='Média do CRA Acumulada')
    salvar_grafico('variacao_media_cra_acumulada')


def plot_variacao_media_cra_forma_ingresso(dataframe):
    """
    Mostra a variação da média do CRA por tipo de ingresso ao longo dos períodos.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    df_por_tipo = dataframe.groupby(['FORMA_INGRESSO_SIMPLES', 'PERIODO_INGRESSO_FORMATADO'])[
        'CRA'].mean().reset_index()
    plotar_grafico_linha(x='PERIODO_INGRESSO_FORMATADO', y='CRA', data=df_por_tipo,
                         titulo='Variação da Média do CRA por Forma de Ingresso',
                         xlabel='Período de Ingresso', ylabel='Média do CRA')
    salvar_grafico('variacao_media_cra_forma_ingresso')


def plot_variacao_media_cra_forma_evasao(dataframe):
    """
    Analisa a variação da média do CRA por forma de evasão ao longo dos períodos.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    df_por_evasao = dataframe.groupby(['STATUS_EVASAO', 'PERIODO_INGRESSO_FORMATADO'])['CRA'].mean().reset_index()
    sns.lineplot(data=df_por_evasao, x='PERIODO_INGRESSO_FORMATADO', y='CRA', hue='STATUS_EVASAO')
    plt.title('Variação da Média do CRA por Forma de Evasão')
    plt.xlabel('Período de Ingresso')
    plt.ylabel('Média do CRA')
    salvar_grafico('variacao_media_cra_forma_evasao')


def plot_variacao_media_ponderada_cra_forma_ingresso(dataframe):
    """
    Mostra a variação da média ponderada do CRA por tipo de ingresso ao longo dos períodos.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    dataframe['QUANTIDADE'] = 1
    dataframe['CRA_PONDERADO'] = dataframe['CRA'] * dataframe['QUANTIDADE']

    # Especificar as colunas numéricas para realizar a soma
    numeric_columns = ['QUANTIDADE', 'CRA_PONDERADO']
    df_ponderado = dataframe.groupby(['FORMA_INGRESSO_SIMPLES', 'PERIODO_INGRESSO_FORMATADO'])[numeric_columns].sum()

    df_ponderado['CRA_PONDERADO'] /= df_ponderado['QUANTIDADE']
    df_ponderado.reset_index(inplace=True)

    plotar_grafico_linha_ponderada(
        data=df_ponderado, x='PERIODO_INGRESSO_FORMATADO', y='CRA_PONDERADO',
        hue='FORMA_INGRESSO_SIMPLES', titulo='Média Ponderada do CRA por Forma de Ingresso',
        xlabel='Período de Ingresso', ylabel='Média Ponderada do CRA'
    )
    salvar_grafico('variacao_media_ponderada_cra_forma_ingresso')


def plot_variacao_media_ponderada_cra_forma_evasao(dataframe):
    """
    Mostra a variação da média ponderada do CRA por forma de evasão ao longo dos períodos.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    dataframe['QUANTIDADE'] = 1
    dataframe['CRA_PONDERADO'] = dataframe['CRA'] * dataframe['QUANTIDADE']

    # Especificar as colunas numéricas para realizar a soma
    numeric_columns = ['QUANTIDADE', 'CRA_PONDERADO']
    df_ponderado = dataframe.groupby(['STATUS_EVASAO', 'PERIODO_INGRESSO_FORMATADO'])[numeric_columns].sum()

    df_ponderado['CRA_PONDERADO'] /= df_ponderado['QUANTIDADE']
    df_ponderado.reset_index(inplace=True)

    plotar_grafico_linha_ponderada(
        data=df_ponderado, x='PERIODO_INGRESSO_FORMATADO', y='CRA_PONDERADO',
        hue='STATUS_EVASAO', titulo='Média Ponderada do CRA por Forma de Evasão',
        xlabel='Período de Ingresso', ylabel='Média Ponderada do CRA'
    )
    salvar_grafico('variacao_media_ponderada_cra_forma_evasao')


def plot_variacao_media_acumulada_cra_periodo_ingresso(dataframe):
    """
    Mostra a variação acumulada da média do CRA por período de ingresso.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    df_sorted = dataframe.sort_values('PERIODO_INGRESSO_FORMATADO')
    df_acumulada = df_sorted.groupby('PERIODO_INGRESSO_FORMATADO')['CRA'].expanding().mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_acumulada, x='PERIODO_INGRESSO_FORMATADO', y='CRA')
    plt.title('Variação da Média do CRA Acumulada por Período')
    plt.xlabel('Período de Ingresso')
    plt.ylabel('Média do CRA Acumulada')
    plt.xticks(rotation=45)
    salvar_grafico('variacao_media_acumulada_cra_periodo_ingresso')


def plot_tendencia_ingresso(dataframe):
    """
    Analisa a tendência de ingresso no curso ao longo dos anos, separada por forma de ingresso.
    """
    tendencia_ingresso = dataframe.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(
        name='Quantidade')
    plotar_grafico_linha(x='ANO_PERIODO_INGRESSO', y='Quantidade', data=tendencia_ingresso,
                         titulo='Tendência de Ingresso por Ano e Forma de Ingresso',
                         xlabel='Ano de Ingresso', ylabel='Quantidade de Alunos')
    salvar_grafico('tendencia_ingresso')


def plot_tendencia_evasao(dataframe):
    """
    Analisa a tendência de evasão no curso ao longo dos anos, separada por forma de evasão.
    """
    tendencia_evasao = dataframe.groupby(['ANO_PERIODO_INGRESSO', 'STATUS_EVASAO']).size().reset_index(name='Quantidade')
    plotar_grafico_linha(x='ANO_PERIODO_INGRESSO', y='Quantidade', data=tendencia_evasao,
                         titulo='Tendência de Evasão por Ano e Forma de Evasão',
                         xlabel='Ano de Ingresso', ylabel='Quantidade de Evasões')
    salvar_grafico('tendencia_evasao')


if __name__ == "__main__":
    df = carregar_dados()
    analise_temporal(df)
