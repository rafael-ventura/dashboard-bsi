import os
import matplotlib.pyplot as plt
import seaborn as sns


def criar_pasta_graficos(nome_pasta):
    """
    Cria uma pasta para salvar os gráficos.
    """
    caminho_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dados/processado', nome_pasta))
    if not os.path.exists(caminho_base):
        os.makedirs(caminho_base)
        print(f'Pasta criada: {caminho_base}')
    return caminho_base


def salvar_grafico(nome_grafico, nome_pasta):
    """
    Salva o gráfico atual na pasta especificada.
    """
    caminho_completo = os.path.join(nome_pasta, f'{nome_grafico}.png')
    plt.savefig(caminho_completo)
    plt.close()
    print(f"Gráfico salvo: {caminho_completo}")


def ajustar_estilos_grafico(ax, title="", xlabel="", ylabel="", title_size=18, xlabel_size=14, ylabel_size=14, xticks_size=12, yticks_size=12, legend_size=12):
    """
    Ajusta os estilos do gráfico.
    """
    ax.set_title(title, fontsize=title_size)
    ax.set_xlabel(xlabel, fontsize=xlabel_size)
    ax.set_ylabel(ylabel, fontsize=ylabel_size)
    ax.tick_params(axis='x', labelsize=xticks_size)
    ax.tick_params(axis='y', labelsize=yticks_size)
    if ax.get_legend():
        ax.legend(fontsize=legend_size)
    plt.tight_layout()


def adicionar_valores_barras(ax, exibir_percentual=False, total=None, fontsize=12, offset=5):
    """
    Adiciona valores sobre as barras de um gráfico.
    """
    for p in ax.patches:
        altura = p.get_height()
        if altura > 0:
            texto = f'{altura:.0f}' if not exibir_percentual else f'{(altura / total) * 100:.1f}%'
            ax.annotate(
                texto,
                (p.get_x() + p.get_width() / 2., altura),
                ha='center',
                va='bottom',
                fontsize=fontsize,
                xytext=(0, offset),
                textcoords='offset points'
            )


def plotar_grafico_de_barras(data, x, y, titulo, xlabel, ylabel, nome_grafico, nome_pasta, palette='pastel', exibir_percentual=False):
    """
    Plota um gráfico de barras.
    """
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=x, y=y, data=data, palette=palette)
    total = data[y].sum() if exibir_percentual else None
    adicionar_valores_barras(ax, exibir_percentual, total)
    ajustar_estilos_grafico(ax, title=titulo, xlabel=xlabel, ylabel=ylabel)
    salvar_grafico(nome_grafico, nome_pasta)


def plotar_grafico_de_linhas(data, x, y, titulo, xlabel, ylabel, nome_grafico, nome_pasta, hue=None):
    """
    Plota um gráfico de linhas.
    """
    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(x=x, y=y, hue=hue, data=data, marker='o')
    ajustar_estilos_grafico(ax, title=titulo, xlabel=xlabel, ylabel=ylabel)
    salvar_grafico(nome_grafico, nome_pasta)
