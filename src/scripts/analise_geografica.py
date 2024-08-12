import geopandas as gpd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from src.utils.plots import criar_pasta_graficos, salvar_grafico, plot_treemap
from src.utils.utils import carregar_dados, pega_caminho_base, remover_acentos_e_maiusculas


def executar_analise_geografica(dataframe):
    print("\nIniciando Análise Geográfica...")
    criar_pasta_graficos()

    bairros_rj = carregar_bairros_rj()
    bairros_rj = consolidar_ilha_do_governador(bairros_rj)
    bairros_rj = preparar_dados_bairros(dataframe, bairros_rj)

    plot_distribuicao_bairros(dataframe)
    plot_distribuicao_cidade(dataframe)
    plot_distribuicao_estado(dataframe)
    plot_mapa_calor(bairros_rj)
    plot_treemap_bairros(bairros_rj)
    plot_tree_map_cidades(dataframe)
    plot_tree_map_estados(dataframe)
    plot_pie_bairros(bairros_rj)
    plot_pie_zonas(dataframe)
    print("\nAnálise Geográfica Concluída com Sucesso!")


def preparar_dados_bairros(dataframe, bairros_rj):
    """
    Prepara os dados de bairros para plotagem.
    """
    # Limpeza dos nomes de bairros para garantir a correspondência correta
    dataframe['BAIRRO'] = dataframe['BAIRRO'].apply(remover_acentos_e_maiusculas)
    bairros_rj['nome'] = bairros_rj['nome'].apply(remover_acentos_e_maiusculas)

    # Contagem de alunos por bairro
    contagem_alunos = dataframe['BAIRRO'].value_counts().reset_index()
    contagem_alunos.columns = ['nome', 'ALUNOS']

    # Merge baseado nos nomes dos bairros, preenchendo NaNs com zeros
    bairros_rj = bairros_rj.merge(contagem_alunos, on='nome', how='left')
    bairros_rj['ALUNOS'] = bairros_rj['ALUNOS'].fillna(0)  # Preenche NaNs com zeros
    return bairros_rj


def consolidar_ilha_do_governador(bairros_rj):
    """
    Consolida os sub-bairros da Ilha do Governador em um único polígono.
    """
    ilha = bairros_rj[bairros_rj['regiao_adm'].str.contains('ILHA DO GOVERNADOR', na=False)]
    ilha_consolidada = ilha.dissolve(by='regiao_adm')
    ilha_consolidada['nome'] = 'ILHA DO GOVERNADOR'

    bairros_rj = bairros_rj[~bairros_rj['regiao_adm'].str.contains('ILHA DO GOVERNADOR', na=False)]
    bairros_rj = pd.concat([bairros_rj, ilha_consolidada])

    return bairros_rj


def carregar_bairros_rj():
    bairros_rj = gpd.read_file(pega_caminho_base() + '/dados/Limite_de_Bairros.geojson')
    return bairros_rj


def plot_distribuicao_bairros(dataframe):
    """
    Plota a distribuição de alunos por bairro, incluindo apenas bairros com mais de 5 alunos.
    """
    plt.figure(figsize=(10, 6))

    aluno_count = dataframe['BAIRRO'].value_counts()
    aluno_count = aluno_count[aluno_count > 5]

    _colors = sb.color_palette("husl", len(aluno_count))
    aluno_count.plot(kind='bar', color=_colors)
    plt.xticks(rotation=45, ha='right')

    plt.title('Distribuição de Alunos por Bairro (mais de 5 alunos)')
    plt.xlabel('Bairro')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_bairro')


def plot_distribuicao_cidade(dataframe):
    """
    Plota a distribuição de alunos por cidade, excluindo cidades sem alunos.
    """
    plt.figure(figsize=(10, 6))

    # Contagem de alunos por cidade e remoção de cidades com zero alunos
    cidade_count = dataframe['CIDADE'].value_counts()
    cidade_count = cidade_count[cidade_count > 0]  # Remove cidades com zero alunos

    # Plotagem do gráfico de barras para cidades com alunos
    cidade_count.plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Alunos por Cidade')
    plt.xlabel('Cidade')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_cidade')


def plot_distribuicao_estado(dataframe):
    """
    Plota a distribuição de alunos por estado, excluindo estados sem alunos.
    """
    plt.figure(figsize=(10, 6))

    # Contagem de alunos por estado e remoção de estados com zero alunos
    estado_count = dataframe['ESTADO'].value_counts()
    estado_count = estado_count[estado_count > 0]  # Remove estados com zero alunos

    # Plotagem do gráfico de barras para estados com alunos
    estado_count.plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Alunos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_estado')


def plot_mapa_calor(bairros_rj):
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    # Define os intervalos e as cores correspondentes
    intervals = [0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 65, 95, 105]
    colors_palette = [
        "#D7E5F0", "#C0D1E5", "#B0C3DE", "#A9BCDB", "#99AFD3", "#8AA1CC", "#7A93C5", "#6B86BE",
        "#637FBA", "#5471B3", "#4464AC", "#3556A5", "#25489E", "#163B97"
    ]

    cmap = colors.ListedColormap(colors_palette)
    norm = colors.BoundaryNorm(boundaries=intervals, ncolors=len(intervals))

    bairros_rj.plot(column='ALUNOS', ax=ax, legend=True, cmap=cmap, norm=norm, edgecolor='black',
                    missing_kwds={"color": "lightgrey", "label": "Sem dados"},
                    legend_kwds={'label': "Número de Alunos por Bairro", 'orientation': "horizontal"})

    # Destaca a Urca em verde
    urca = bairros_rj[bairros_rj['nome'] == 'URCA']
    urca.plot(ax=ax, color='green', edgecolor='black')

    plt.title('Densidade de Alunos por Bairro no RJ')
    plt.axis('off')
    plt.legend()
    salvar_grafico('mapa_calor_alunos')


def plot_treemap_bairros(bairros_rj):
    """
    Plota um Treemap dos alunos por bairro, considerando apenas bairros com mais de 5 alunos.
    """
    plot_treemap(bairros_rj['ALUNOS'], 5, 'Treemap de Alunos por Bairro')


def plot_tree_map_cidades(dataframe):
    """
    Plota um Treemap dos alunos por cidade, considerando apenas cidades com mais de 5 alunos.
    """
    plot_treemap(dataframe['CIDADE'].value_counts(), 5, 'Treemap de Alunos por Cidade')


def plot_tree_map_estados(dataframe):
    """
    Plota um Treemap dos alunos por estado, considerando apenas estados com mais de 5 alunos.
    :param dataframe: DataFrame com os dados.
    :return: None
    """
    plot_treemap(dataframe['ESTADO'].value_counts(), 5, 'Treemap de Alunos por Estado')


def plot_pie_bairros(bairros_rj):
    """
    Plota um gráfico de pizza com a distribuição de alunos por bairro.
    """
    plt.figure(figsize=(10, 10))
    plt.pie(bairros_rj['ALUNOS'], labels=bairros_rj['nome'], autopct='%1.1f%%', startangle=90)
    plt.title('Distribuição de Alunos por Bairro')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_bairro_pie')


def plot_pie_zonas(dataframe):
    """
    Plota um gráfico de pizza com a distribuição de alunos por zona.
    """
    zona_count = dataframe['ZONA'].value_counts()
    plt.figure(figsize=(10, 10))
    plt.pie(zona_count, labels=zona_count.index, autopct='%1.1f%%', startangle=90, colors=sb.color_palette("husl", len(zona_count)))
    plt.title('Distribuição de Alunos por Zona')
    plt.tight_layout()
    salvar_grafico('distribuicao_alunos_zona_pie')


if __name__ == "__main__":
    df = carregar_dados()
    executar_analise_geografica(df)
