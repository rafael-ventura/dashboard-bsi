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

    # Calcula o total para cada categoria (sem considerar hue)
    total_por_categoria = data.groupby(x).size().reset_index(name='total')

    sns.countplot(x=x, data=data, hue=hue, ax=ax)

    if exibir_percentual:
        # Caso haja hue, calcula o total dentro de cada subcategoria corretamente
        for p in ax.patches:
            altura = p.get_height()

            if altura > 0:  # Adiciona anotação apenas se a altura for maior que zero
                categoria = int(p.get_x() + p.get_width() / 2.0)
                categoria_nome = ax.get_xticklabels()[categoria].get_text()  # Pega o rótulo da categoria

                if categoria_nome in total_por_categoria[x].values:
                    total_categoria = total_por_categoria[total_por_categoria[x] == categoria_nome].iloc[0]['total']
                    percentual = f'{(altura / total_categoria) * 100:.1f}%'
                    ax.annotate(f'{percentual}', (p.get_x() + p.get_width() / 2., altura), ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    else:
        # Exibe o valor absoluto apenas quando a altura for maior que zero
        for p in ax.patches:
            altura = p.get_height()
            if altura > 0:
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
    # print(f'Gráfico "{nome_grafico}" salvo com sucesso em "{caminho_completo}"!')


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


def ajustar_fontes_eixos(ax, xlabel_size=16, ylabel_size=16, xticks_size=14, yticks_size=14):
    """
    Ajusta os tamanhos das fontes dos eixos e rótulos em um gráfico.

    Parâmetros:
    - ax: O objeto de eixos do matplotlib ou seaborn.
    - xlabel_size: Tamanho da fonte do rótulo do eixo X.
    - ylabel_size: Tamanho da fonte do rótulo do eixo Y.
    - xticks_size: Tamanho da fonte dos rótulos do eixo X.
    - yticks_size: Tamanho da fonte dos rótulos do eixo Y.
    """
    ax.set_xlabel(ax.get_xlabel(), fontsize=xlabel_size)
    ax.set_ylabel(ax.get_ylabel(), fontsize=ylabel_size)
    ax.tick_params(axis='x', labelsize=xticks_size)
    ax.tick_params(axis='y', labelsize=yticks_size)


def ajustar_estilos_grafico(ax, title="", xlabel="", ylabel="",
                            title_size=18, xlabel_size=14, ylabel_size=14,
                            xticks_size=12, yticks_size=12, legend_size=12):
    """
    Ajusta os tamanhos das fontes do título, rótulos dos eixos e dos ticks de um gráfico.

    Parâmetros:
    - ax: O objeto de eixos do matplotlib ou seaborn.
    - title: Título do gráfico.
    - xlabel: Rótulo do eixo X.
    - ylabel: Rótulo do eixo Y.
    - title_size: Tamanho da fonte do título.
    - xlabel_size: Tamanho da fonte do rótulo do eixo X.
    - ylabel_size: Tamanho da fonte do rótulo do eixo Y.
    - xticks_size: Tamanho da fonte dos rótulos do eixo X.
    - yticks_size: Tamanho da fonte dos rótulos do eixo Y.
    - legend_size: Tamanho da fonte da legenda (se houver).
    """
    # Definir título e tamanhos de fonte
    ax.set_title(title, fontsize=title_size)
    ax.set_xlabel(xlabel, fontsize=xlabel_size)
    ax.set_ylabel(ylabel, fontsize=ylabel_size)

    # Ajustar tamanhos dos ticks nos eixos
    ax.tick_params(axis='x', labelsize=xticks_size)
    ax.tick_params(axis='y', labelsize=yticks_size)

    # Ajustar tamanho da legenda, se existir
    if ax.get_legend() is not None:
        ax.legend(fontsize=legend_size)

    plt.tight_layout()


def adicionar_valores_barras(ax, exibir_percentual=True, total=None, fontsize=14, offset=8):
    """
    Adiciona valores exatos nas barras verticais.
    Se `exibir_percentual` for True, adiciona o percentual em vez do valor absoluto.

    Parâmetros:
    - ax: O objeto de eixos do matplotlib ou seaborn.
    - exibir_percentual: Exibe o percentual se True.
    - total: O valor total para calcular o percentual.
    - fontsize: Tamanho da fonte dos valores nas barras.
    - offset: Distância dos valores até a barra.
    """
    for p in ax.patches:
        altura = p.get_height()
        if altura > 0:  # Apenas adiciona valores se a barra for maior que zero
            if exibir_percentual and total is not None:
                percentual = altura / total * 100
                ax.annotate(f'{percentual:.1f}%', (p.get_x() + p.get_width() / 2., altura),
                            ha='center', va='bottom', fontsize=fontsize)
            else:
                ax.annotate(f'{altura:.1f}', (p.get_x() + p.get_width() / 2., altura),
                            ha='center', va='bottom', fontsize=fontsize)


def adicionar_valores_barras_laterais(ax, exibir_percentual=True, total=None, fontsize=12, offset=20):
    """
    Adiciona valores exatos nas barras horizontais (laterais).
    Se `exibir_percentual` for True, adiciona o percentual em vez do valor absoluto.

    Parâmetros:
    - ax: O objeto de eixos do matplotlib ou seaborn.
    - exibir_percentual: Exibe o percentual se True.
    - total: O valor total para calcular o percentual.
    - fontsize: Tamanho da fonte dos valores nas barras.
    - offset: Distância dos valores até a barra.
    """
    for p in ax.patches:
        largura = p.get_width()
        if largura > 0:  # Apenas adiciona valores se a barra for maior que zero
            if exibir_percentual and total is not None:
                percentual = largura / total * 100
                ax.annotate(f'{percentual:.1f}%', (largura, p.get_y() + p.get_height() / 2),
                            ha='center', va='center', xytext=(offset, 0), textcoords='offset points',
                            fontsize=fontsize)
            else:
                ax.annotate(f'', (largura, p.get_y() + p.get_height() / 2),
                            ha='center', va='center', xytext=(offset, 0), textcoords='offset points',
                            fontsize=fontsize)


def plotar_grafico_barras_laterais(data, x, y, title, xlabel, ylabel, ax=None, exibir_percentual=True):
    """
    Plota um gráfico de barras laterais customizado e aplica ajustes de estilos.

    Parâmetros:
    - data: DataFrame contendo os dados.
    - x: Coluna a ser usada no eixo X.
    - y: Coluna a ser usada no eixo Y.
    - title: Título do gráfico.
    - xlabel: Rótulo do eixo X.
    - ylabel: Rótulo do eixo Y.
    - ax: Objeto de eixo (opcional).
    - exibir_percentual: Exibe percentuais nas barras se True.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(x=x, y=y, data=data, ax=ax, orient='h')

    total = data[x].sum() if exibir_percentual else None
    adicionar_valores_barras_laterais(ax, exibir_percentual=exibir_percentual, total=total)

    ajustar_estilos_grafico(ax, title=title, xlabel=xlabel, ylabel=ylabel,
                            title_size=18, xlabel_size=14, ylabel_size=14,
                            xticks_size=12, yticks_size=12, legend_size=12)


def plotar_grafico_barras_customizado(data, x, y, title, xlabel, ylabel, ax=None, exibir_percentual=True):
    """
    Plota um gráfico de barras customizado e aplica ajustes de estilos.

    Parâmetros:
    - data: DataFrame contendo os dados.
    - x: Coluna a ser usada no eixo X.
    - y: Coluna a ser usada no eixo Y.
    - title: Título do gráfico.
    - xlabel: Rótulo do eixo X.
    - ylabel: Rótulo do eixo Y.
    - ax: Objeto de eixo (opcional).
    - exibir_percentual: Exibe percentuais nas barras se True.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(x=x, y=y, data=data, ax=ax)

    # Calcular o total para exibir percentuais corretamente
    total = data[y].sum() if exibir_percentual else None

    # Adicionar valores em cima das barras
    adicionar_valores_barras(ax, exibir_percentual=exibir_percentual, total=total)

    # Ajustar o estilo do gráfico
    ajustar_estilos_grafico(ax, title=title, xlabel=xlabel, ylabel=ylabel,
                            title_size=18, xlabel_size=14, ylabel_size=14,
                            xticks_size=12, yticks_size=12, legend_size=12)


# Exemplo de uso para gráfico de linha:
def plotar_grafico_linha_customizado(data, x, y, title, xlabel, ylabel, ax=None):
    """
    Plota um gráfico de linha customizado e aplica ajustes de estilos.

    Parâmetros:
    - data: DataFrame contendo os dados.
    - x: Coluna a ser usada no eixo X.
    - y: Coluna a ser usada no eixo Y.
    - title: Título do gráfico.
    - xlabel: Rótulo do eixo X.
    - ylabel: Rótulo do eixo Y.
    - ax: Objeto de eixo (opcional).
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(x=x, y=y, data=data, ax=ax)

    # Ajustar o estilo do gráfico
    ajustar_estilos_grafico(ax, title=title, xlabel=xlabel, ylabel=ylabel,
                            title_size=18, xlabel_size=14, ylabel_size=14,
                            xticks_size=12, yticks_size=12, legend_size=12)
