import os

import matplotlib.pyplot as plt
import seaborn as sns
import squarify

from src.utils.utils import pega_caminho_base


def plotar_grafico_de_barras(x, y, data, titulo, xlabel, ylabel, ax=None):
    """
    Função para plotar um gráfico de barras.
    :param x: Nome da coluna do eixo x.
    :param y: Nome da coluna do eixo y.
    :param data: DataFrame com os dados.
    :param titulo: Título do gráfico.
    :param xlabel: Rótulo do eixo x.
    :param ylabel: Rótulo do eixo y.
    :param ax: Eixo do gráfico.
    :return: None
    """
    if ax is None:
        fig, ax = plt.subplots()
    sns.barplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def criar_grafico_de_contagem(x, data, titulo, xlabel, ylabel, hue=None, ax=None, exibir_percentual=True):
    """
    Função para plotar um gráfico de contagem com opção de exibir porcentagens e valores exatos.
    """
    if ax is None:
        fig, ax = plt.subplots()

    total = len(data)

    sns.countplot(x=x, data=data, hue=hue, ax=ax)

    if exibir_percentual:
        for p in ax.patches:
            altura = p.get_height()
            percentual = f'{(altura / total) * 100:.1f}%'
            ax.annotate(f'{percentual}', (p.get_x() + p.get_width() / 2., altura), ha='center', va='center', xytext=(0, 8), textcoords='offset points')
    else:
        for p in ax.patches:
            altura = p.get_height()
            ax.annotate(f'{int(altura)}', (p.get_x() + p.get_width() / 2., altura), ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.tight_layout()


def plotar_histograma(x, data, titulo, xlabel, ylabel, ax=None):
    """
    Função para plotar um histograma.
    :param x: Nome da coluna do eixo x.
    :param data: DataFrame com os dados.
    :param titulo: Título do gráfico.
    :param xlabel: Rótulo do eixo x.
    :param ylabel: Rótulo do eixo y.
    :param ax: Eixo do gráfico.
    :return: None
    """
    if ax is None:
        fig, ax = plt.subplots()
    sns.histplot(x=x, data=data, kde=True, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plotar_grafico_caixa(x, y, data, titulo, xlabel, ylabel, ax=None):
    """
    Função para plotar um boxplot.
    :param x: Nome da coluna do eixo x.
    :param y: Nome da coluna do eixo y.
    :param data: DataFrame com os dados.
    :param titulo: Título do gráfico.
    :param xlabel: Rótulo do eixo x.
    :param ylabel: Rótulo do eixo y.
    :param ax: Eixo do gráfico.
    :return: None
    """
    if ax is None:
        fig, ax = plt.subplots()
    sns.boxplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plotar_grafico_linha(x, y, data, titulo, xlabel, ylabel, ax=None, x_tick_params=None):
    """
    Função para plotar um gráfico de linha.
    :param x: Nome da coluna do eixo x.
    :param y: Nome da coluna do eixo y.
    :param data: DataFrame com os dados.
    :param titulo: Título do gráfico.
    :param xlabel: Rótulo do eixo x.
    :param ylabel: Rótulo do eixo y.
    :param ax: Eixo do gráfico.
    :param x_tick_params: Parâmetros para os ticks do eixo x.
    :return: None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if x_tick_params:
        ax.tick_params(axis='x', **x_tick_params)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()


def plotar_grafico_linha_ponderada(data, x, y, hue=None, titulo="", xlabel="", ylabel=""):
    """
    Plota um gráfico de linha ponderada para dados agrupados.
    :param data: DataFrame com os dados.
    :param x: Coluna do DataFrame para o eixo x.
    :param y: Coluna do DataFrame para o eixo y.
    :param hue: Coluna do DataFrame para diferenciar linhas.
    :param titulo: Título do gráfico.
    :param xlabel: Rótulo para o eixo x.
    :param ylabel: Rótulo para o eixo y.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title=hue)
    plt.tight_layout()


def plot_treemap(data, threshold, title, color_scheme='Spectral', nome_pasta='graficos', show_values=False):
    """
    Plota um Treemap genérico baseado nos dados fornecidos.
    :param data: Series com os dados (índices serão usados como labels).
    :param threshold: Limite mínimo para inclusão no treemap.
    :param title: Título do Treemap.
    :param color_scheme: Esquema de cores para o treemap.
    :param nome_pasta: Pasta onde o gráfico será salvo.
    :param show_values: Booleano para determinar se os valores serão mostrados nas caixas.
    """
    # Filtrando os dados com base no threshold
    filtered_data = data[data > threshold]

    sizes = filtered_data.values
    labels = filtered_data.index

    # Definindo as cores do treemap
    colors = sns.color_palette(color_scheme, len(sizes))

    # Preparando o texto a ser exibido nas caixas do treemap
    if show_values:
        labels = [f'{label}\n{size} alunos' for label, size in zip(labels, sizes)]

    # Criando o gráfico treemap
    plt.figure(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=colors, pad=True)
    plt.title(title)
    plt.axis('off')

    # Salvando o gráfico
    salvar_grafico(title.lower().replace(' ', '_'), nome_pasta)


def criar_pasta_graficos(nome_pasta):
    """
    Função para criar uma pasta para salvar os gráficos.
    :param nome_pasta: Caminho completo da pasta onde os gráficos serão salvos.
    :return: None
    """
    caminho_base = os.path.join(pega_caminho_base(), 'dados', 'processado', nome_pasta)

    if not os.path.exists(caminho_base):
        os.makedirs(caminho_base)
        print(f'Pasta "{caminho_base}" criada com sucesso!')

    return caminho_base


def salvar_grafico(nome_grafico, nome_pasta):
    """
    Função para salvar gráficos em uma pasta específica.
    :param nome_grafico: Nome do arquivo do gráfico.
    :param nome_pasta: Caminho completo da pasta onde o gráfico será salvo.
    """
    caminho_completo = os.path.join(pega_caminho_base(), 'dados', 'processado', nome_pasta, f'{nome_grafico}.png')
    plt.savefig(caminho_completo)
    plt.close()
    print(f'Gráfico "{nome_grafico}" salvo com sucesso em "{caminho_completo}"!')


def plotar_grafico_caixa_com_estatisticas(x, y, data, titulo, xlabel, ylabel, nome_pasta, nome_grafico):
    """
    Função para plotar um boxplot com as principais estatísticas (média, mediana, etc.).
    """
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(x=x, y=y, data=data, palette='muted')

    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Calculando as estatísticas
    stats = data.groupby(x)[y].describe()

    # Adicionando as estatísticas no gráfico
    for idx, group in enumerate(stats.index):
        media = stats.loc[group, 'mean']
        mediana = stats.loc[group, '50%']
        q1 = stats.loc[group, '25%']
        q3 = stats.loc[group, '75%']

        ax.annotate(f'Média: {media:.2f}\nMediana: {mediana:.2f}\nQ1: {q1:.2f}\nQ3: {q3:.2f}',
                    xy=(idx, mediana), xycoords='data',
                    xytext=(0, -40), textcoords='offset points',
                    ha='center', fontsize=8, color='black', backgroundcolor='white')

    plt.tight_layout()
    salvar_grafico(nome_grafico, nome_pasta)
