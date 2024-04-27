import geopandas as gpd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import squarify
from mapclassify import UserDefined
import numpy as np
from matplotlib.patches import Patch

from src.utils import salvar_grafico, criar_pasta_graficos, carregar_dados, remover_acentos_e_maiusculas, \
    string_para_imagem


def executar_analise_geografica(dataframe):
    print("\nIniciando Análise Geográfica...")
    criar_pasta_graficos()

    bairros_rj = carregar_bairros_rj()
    bairros_rj = consolidar_ilha_do_governador(bairros_rj)
    bairros_rj = preparar_dados_bairros(dataframe, bairros_rj)

    estatisticas_descritivas(dataframe)
    plot_distribuicao_bairros(dataframe)
    plot_distribuicao_cidade(dataframe)
    plot_distribuicao_estado(dataframe)
    plot_mapa_calor(bairros_rj)
    plot_treemap(bairros_rj)
    plot_grafico_bolha_cidades(dataframe)
    plot_grafico_bolha_estados(dataframe)
    plot_grafico_bolha_bairros(dataframe)
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
    bairros_rj = gpd.read_file('C:\Dev\dashboard-bsi\dados\Limite_de_Bairros.geojson')
    return bairros_rj


def estatisticas_descritivas(dataframe):
    """
    Gera uma imagem com estatísticas descritivas dos dados.
    """
    texto = "\nEstatísticas Descritivas:\n"
    texto += "\nOs 15 bairros com mais alunos:\n"
    texto += dataframe['BAIRRO'].value_counts().head(15).to_string()
    texto += "\n\nOs 5 bairros com menos alunos:\n"
    texto += dataframe['BAIRRO'].value_counts().tail(5).to_string()
    texto += "\n\nQuantidade de bairros únicos:\n" + str(dataframe['BAIRRO'].nunique())
    texto += "\n\nQuantidade de alunos por bairro:\n"
    texto += dataframe['BAIRRO'].value_counts().describe().to_string()
    texto += "\n\nDistância Média da Urca: {:.2f} km".format(dataframe['DISTANCIA_URCA'].mean())
    texto += "\n\nQuantidade de alunos a mais de 10 km da Urca:\n " + str(
        dataframe[dataframe['DISTANCIA_URCA'] > 10].shape[0])
    texto += "\n\nQuantidade de alunos sem distância da Urca: \n " + str(dataframe['DISTANCIA_URCA'].isnull().sum())
    texto += "\n\nOs 5 alunos mais distantes da Urca:\n"
    texto += dataframe.sort_values('DISTANCIA_URCA', ascending=False).head(5)[['BAIRRO', 'DISTANCIA_URCA']].to_string(
        index=False)

    string_para_imagem(texto, nome_arquivo='estatisticas_descritivas')


import matplotlib.pyplot as plt


def plot_distribuicao_bairros(dataframe):
    """
    Plota a distribuição de alunos por bairro, incluindo apenas bairros com mais de 5 alunos.
    """
    plt.figure(figsize=(10, 6))

    aluno_count = dataframe['BAIRRO'].value_counts()
    aluno_count = aluno_count[aluno_count > 5]

    colors = sb.color_palette("husl", len(aluno_count))
    aluno_count.plot(kind='bar', color=colors)
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

def plot_treemap(bairros_rj):
    """
    Plota um Treemap dos alunos por bairro, considerando apenas bairros com mais de 5 alunos.
    """
    plt.figure(figsize=(12, 8))

    bairros_filtrados = bairros_rj[bairros_rj['ALUNOS'] > 5]

    sizes = bairros_filtrados['ALUNOS'].values
    labels = bairros_filtrados['nome'].values

    _colors = sb.color_palette("Spectral", len(sizes))
    text_kwargs = {'fontsize': 10, 'fontfamily': 'sans-serif'}

    squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=_colors, pad=True, text_kwargs=text_kwargs)

    plt.title('Treemap de Alunos por Bairro (mais de 5 alunos)')
    plt.axis('off')
    salvar_grafico('treemap_alunos_por_bairro')


def plot_grafico_bolha(dataframe, coluna, titulo, arquivo_salvar, min_alunos=0, tamanho_figura=(14, 10)):
    """
    Função geral para criar gráficos de bolhas com melhorias visuais e funcionais.
    """
    plt.figure(figsize=tamanho_figura)
    contagem = dataframe[coluna].value_counts()
    contagem = contagem[contagem > min_alunos]  # Filtrando bairros com mais de min_alunos
    tamanhos = contagem.values * 10  # Escala para visibilidade
    cores = sb.color_palette("hsv", len(contagem))

    posicoes_x = np.random.rand(len(tamanhos)) * 100  # Posições x aleatórias
    posicoes_y = np.random.rand(len(tamanhos)) * 10  # Posições y aleatórias

    scatter = plt.scatter(posicoes_x, posicoes_y, s=tamanhos, c=cores, alpha=0.5)
    handles_legendas = [Patch(color=cor, label=etiqueta) for cor, etiqueta in zip(cores, contagem.index)]
    # Ajustando a posição da legenda para o canto inferior direito dentro do gráfico
    plt.legend(handles=handles_legendas, title=coluna, loc='lower right')

    plt.title(f'Gráfico de Bolha de Distribuição de Alunos por {titulo}')
    plt.xticks([])  # Ocultando os ticks do eixo X
    plt.yticks([])  # Ocultando os ticks do eixo Y
    plt.grid(True)
    salvar_grafico(arquivo_salvar)


def plot_grafico_bolha_bairros(dataframe):
    # Configurações específicas para bairros
    plot_grafico_bolha(dataframe, 'BAIRRO', 'Bairro', 'grafico_bolha_bairros', min_alunos=5, tamanho_figura=(12, 8))


def plot_grafico_bolha_cidades(dataframe):
    # Configurações específicas para cidades
    plot_grafico_bolha(dataframe, 'CIDADE', 'Cidade', 'grafico_bolha_cidades', tamanho_figura=(6, 4))


def plot_grafico_bolha_estados(dataframe):
    # Configurações específicas para estados
    plot_grafico_bolha(dataframe, 'ESTADO', 'Estado', 'grafico_bolha_estados', tamanho_figura=(6, 4))


if __name__ == "__main__":
    df = carregar_dados()
    executar_analise_geografica(df)
