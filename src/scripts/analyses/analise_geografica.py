import geopandas as gpd
import matplotlib.pyplot as plt

from src.utils import salvar_grafico, criar_pasta_graficos, carregar_dados, remover_acentos_e_maiusculas


def executar_analise_geografica(dataframe):
    print("\nIniciando Análise Geográfica...")

    criar_pasta_graficos()

    plot_distribuicao_cidade(dataframe)

    plot_distribuicao_estado(dataframe)

    plot_mapa_calor(dataframe)

    plot_densidade_alunos(dataframe)

    print("\nAnálise Geográfica Concluída com Sucesso!")


def preparar_dados_bairros(dataframe, bairros_rj):
    """
    Prepara os dados dos bairros do RJ para serem plotados no mapa de calor.
    :return:
    """
    dataframe['BAIRRO'] = dataframe['BAIRRO'].apply(remover_acentos_e_maiusculas)
    bairros_rj['nome'] = bairros_rj['nome'].apply(remover_acentos_e_maiusculas)

    contagem_alunos = dataframe['BAIRRO'].value_counts().reset_index()
    contagem_alunos.columns = ['nome', 'ALUNOS']
    bairros_rj = bairros_rj.merge(contagem_alunos, on='nome', how='left')

    return bairros_rj


def carregar_bairros_rj():
    """
    Carrega o arquivo com os bairros do RJ.
    """
    bairros_rj = gpd.read_file('data/geo/bairros_rj.geojson')
    return bairros_rj


def plot_distribuicao_cidade(dataframe):
    """
    Plota a distribuição de alunos por cidade.
    """
    plt.figure(figsize=(10, 6))
    dataframe['CIDADE'] = dataframe['CIDADE'].apply(remover_acentos_e_maiusculas)
    dataframe['CIDADE'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Alunos por Cidade')
    plt.xlabel('Cidade')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_cidade')


def plot_distribuicao_estado(dataframe):
    """
    Plota a distribuição de alunos por estado.
    """
    plt.figure(figsize=(10, 6))
    dataframe['ESTADO'] = dataframe['ESTADO'].apply(remover_acentos_e_maiusculas)
    dataframe['ESTADO'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Alunos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_estado')


def plot_mapa_calor(dataframe):
    """
    Plota um mapa de calor com a densidade de alunos por bairro no RJ.
    """
    bairros_rj = carregar_bairros_rj()
    bairros_rj = preparar_dados_bairros(dataframe, bairros_rj)

    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    bairros_rj.plot(column='ALUNOS', ax=ax, legend=True, cmap='viridis', edgecolor='black',
                    missing_kwds={"color": "lightgrey", "label": "Sem dados"},
                    legend_kwds={'label': "Número de Alunos por Bairro", 'orientation': "horizontal"})
    urca = bairros_rj[bairros_rj['nome'] == 'URCA']
    urca.plot(ax=ax, color='red', edgecolor='black', label='Urca')
    plt.title('Densidade de Alunos por Bairro no RJ com destaque para Urca')
    plt.axis('off')
    plt.legend()
    salvar_grafico('mapa_calor_alunos')


def plot_densidade_alunos(dataframe):
    """
    Plota um mapa de calor com a densidade de alunos por bairro no RJ.
    """
    bairros_rj = carregar_bairros_rj()
    bairros_rj = preparar_dados_bairros(dataframe, bairros_rj)

    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    bairros_rj.plot(column='ALUNOS', ax=ax, legend=True,
                    cmap='viridis', scheme='quantiles',
                    legend_kwds={'label': "Densidade de Alunos por Bairro", 'orientation': "horizontal"})
    plt.title('Densidade de Alunos por Bairro no RJ')
    plt.axis('off')
    salvar_grafico('densidade_alunos_por_bairro')


if __name__ == "__main__":
    df = carregar_dados()
    executar_analise_geografica(df)
