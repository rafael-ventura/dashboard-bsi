import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import unidecode


def criar_pasta_graficos(nome_pasta='graficos'):
    caminho_pasta = os.path.join(os.path.dirname(__file__), nome_pasta)
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
        print(f'Pasta "{caminho_pasta}" criada com sucesso!')


def salvar_grafico(nome_grafico, nome_pasta='graficos'):
    caminho_pasta = os.path.join(os.path.dirname(__file__), nome_pasta)
    criar_pasta_graficos(nome_pasta)  # Garante que a pasta exista
    caminho_completo = os.path.join(caminho_pasta, f'{nome_grafico}.png')
    plt.savefig(caminho_completo)
    plt.close()
    print(f'Gráfico "{nome_grafico}" salvo com sucesso em "{caminho_completo}"!')


def carregar_dados(caminho='dados/processado/dfPrincipal.csv'):
    caminho_completo = os.path.join(os.path.dirname(__file__), '..', caminho)
    return pd.read_csv(caminho_completo)


def plot_barplot(x, y, data, titulo, xlabel, ylabel, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    sns.barplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plot_countplot(x, data, titulo, xlabel, ylabel, hue=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    sns.countplot(x=x, data=data, hue=hue, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plot_histplot(x, data, titulo, xlabel, ylabel, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    sns.histplot(x=x, data=data, kde=True, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plot_boxplot(x, y, data, titulo, xlabel, ylabel, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    sns.boxplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plot_lineplot(x, y, data, titulo, xlabel, ylabel, ax=None, x_tick_params=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if x_tick_params:
        ax.tick_params(axis='x', **x_tick_params)
    plt.grid(True)
    plt.tight_layout()


def remover_acentos_e_maiusculas(texto):
    return unidecode.unidecode(texto).upper()
