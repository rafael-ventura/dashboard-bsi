import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import plot_lineplot, criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_temporal(dataframe):
    print("\nIniciando Análise Temporal...")

    evolucao_media_cra(dataframe)

    variacao_media_cra_por_tipo_ingresso(dataframe)

    print("\nAnálise Temporal Concluída!")


def evolucao_media_cra(dataframe):
    # Calculando a média do CRA por período
    media_cra_por_periodo = dataframe.groupby('PER_PERIODO_INGRESSO_FORMAT')['CRA'].mean().reset_index()

    # Opcional: Abreviando os valores do período para facilitar a visualização no eixo x
    media_cra_por_periodo['PER_PERIODO_INGRESSO_FORMAT'] = media_cra_por_periodo['PER_PERIODO_INGRESSO_FORMAT'].apply(
        lambda x: x[2:])

    # Definindo parâmetros para os rótulos do eixo x
    x_tick_params = {'rotation': 45, 'labelsize': 8}

    # Usando o plot_lineplot de utils.py
    plot_lineplot(x='PER_PERIODO_INGRESSO_FORMAT', y='CRA', data=media_cra_por_periodo,
                  titulo='Evolução da Média do CRA por Período',
                  xlabel='Período de Ingresso', ylabel='Média do CRA',
                  x_tick_params=x_tick_params)

    salvar_grafico('evolucao_media_cra')


def variacao_media_cra_acumulada(dataframe):
    # Ordenando o dataframe pelo período de ingresso
    dataframe_sorted = dataframe.sort_values('PER_PERIODO_INGRESSO_FORMAT')

    # Lista para armazenar os resultados
    resultados = []

    # Iterar sobre os períodos de ingresso únicos, ordenados
    for periodo in dataframe_sorted['PER_PERIODO_INGRESSO_FORMAT'].unique():
        # Filtrar alunos que ingressaram até o período atual
        df_filtrado = dataframe_sorted[dataframe_sorted['PER_PERIODO_INGRESSO_FORMAT'] <= periodo]

        # Calcular a média do CRA para os alunos filtrados
        media_cra = df_filtrado['CRA'].mean()

        # Adicionar o resultado à lista
        resultados.append({'PER_PERIODO_INGRESSO_FORMAT': periodo, 'MEDIA_CRA': media_cra})

    # Converter a lista de resultados em um DataFrame
    df_resultados = pd.DataFrame(resultados)

    # Plotar o gráfico da variação da média do CRA acumulada
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PER_PERIODO_INGRESSO_FORMAT', y='MEDIA_CRA', data=df_resultados)
    plt.title('Variação da Média do CRA Acumulada por Período')
    plt.xlabel('Período de Ingresso')
    plt.ylabel('Média do CRA Acumulada')
    plt.xticks(rotation=45)
    plt.tight_layout()

    salvar_grafico('variacao_media_cra_acumulada')


def variacao_media_cra_por_tipo_ingresso(dataframe):
    print("\nIniciando Análise da Variação da Média de CRA por Tipo de Ingresso...")

    # Calculando a média do CRA por tipo de ingresso e por período
    media_cra_por_tipo_ingresso = dataframe.groupby(['FORMA_INGRESSO_SIMPLES', 'PER_PERIODO_INGRESSO_FORMAT'])[
        'CRA'].mean().reset_index()

    # Plotando a evolução da média do CRA para cada tipo de ingresso
    plt.figure(figsize=(12, 8))
    sns.lineplot(x='PER_PERIODO_INGRESSO_FORMAT', y='CRA', hue='FORMA_INGRESSO_SIMPLES',
                 data=media_cra_por_tipo_ingresso)
    plt.title('Variação da Média do CRA por Tipo de Ingresso ao Longo dos Períodos')
    plt.xlabel('Período de Ingresso')
    plt.ylabel('Média do CRA')
    plt.xticks(rotation=45)  # Rotaciona os labels do eixo x para melhor visualização
    plt.tight_layout()

    salvar_grafico('variacao_media_cra_tipo_ingresso')

    print("\nAnálise da Variação da Média de CRA por Tipo de Ingresso Concluída!")


if __name__ == "__main__":
    df = carregar_dados()
    analise_temporal(df)
    variacao_media_cra_por_tipo_ingresso(df)
