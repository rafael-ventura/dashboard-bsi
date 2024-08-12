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


def criar_grafico_de_contagem(x, data, titulo, xlabel, ylabel, hue=None, ax=None):
    """
    Função para plotar um gráfico de contagem.
    :param x: Nome da coluna do eixo x.
    :param data: DataFrame com os dados.
    :param titulo: Título do gráfico.
    :param xlabel: Rótulo do eixo x.
    :param ylabel: Rótulo do eixo y.
    :param hue: Nome da coluna para agrupamento.
    :param ax: Eixo do gráfico.
    :return: None
    """
    if ax is None:
        fig, ax = plt.subplots()
    sns.countplot(x=x, data=data, hue=hue, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


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


def plot_treemap(data, threshold, title, color_scheme='Spectral'):
    """
    Plota um Treemap genérico baseado nos dados fornecidos.
    :param data: Series com os dados (índices serão usados como labels).
    :param threshold: Limite mínimo para inclusão no treemap.
    :param title: Título do Treemap.
    :param color_scheme: Esquema de cores para o treemap.
    """
    filtered_data = data[data > threshold]

    sizes = filtered_data.values
    labels = filtered_data.index

    colors = sns.color_palette(color_scheme, len(sizes))
    text_kwargs = {'fontsize': 10, 'fontfamily': 'sans-serif'}

    plt.figure(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=colors, pad=True, text_kwargs=text_kwargs)
    plt.title(title)
    plt.axis('off')
    salvar_grafico(title.lower().replace(' ', '_'))


def criar_pasta_graficos(nome_pasta='graficos'):
    """
    Função para criar uma pasta para salvar os gráficos.
    :param nome_pasta: Nome da pasta a ser criada.
    :return: None
    """
    caminho_pasta = os.path.join(pega_caminho_base(), 'dados', 'processado', nome_pasta)
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
        print(f'Pasta "{caminho_pasta}" criada com sucesso!')


def salvar_grafico(nome_grafico, nome_pasta='graficos'):
    """
    Função para salvar um gráfico em uma pasta específica.
    :param nome_grafico: Nome do gráfico a ser salvo.
    :param nome_pasta: Nome da pasta onde o gráfico será salvo.
    :return: None
    """
    caminho_pasta = os.path.join(pega_caminho_base(), 'dados', 'processado', nome_pasta)
    criar_pasta_graficos(nome_pasta)
    caminho_completo = os.path.join(caminho_pasta, f'{nome_grafico}.png')
    plt.savefig(caminho_completo)
    plt.close()
    print(f'Gráfico "{nome_grafico}" salvo com sucesso em "{caminho_completo}"!')
