import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils import criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_exploratoria(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise Exploratória...")

    plot_estatisticas_descritivas(dataframe, 'CRA')
    plot_countplot_CRA(dataframe)
    plot_distribuicao_sexo(dataframe)
    plot_distribuicao_idade(dataframe)
    plot_distribuicao_evasao(dataframe)

    print("\nAnálise Exploratória Concluída!")


def plot_estatisticas_descritivas(dataframe, coluna):
    if coluna in dataframe.columns:
        desc = dataframe[coluna].describe()
        var = dataframe[coluna].var()
        skew = dataframe[coluna].skew()
        kurt = dataframe[coluna].kurtosis()

        estatisticas = pd.DataFrame({
            'Métrica': ['Média', 'Desvio Padrão', 'Variância', 'Assimetria', 'Curtose'],
            'Valor': [desc['mean'], desc['std'], var, skew, kurt]
        })

        plt.figure(figsize=(10, 6))
        color = sns.color_palette('viridis')[0]
        sns.barplot(x='Métrica', y='Valor', data=estatisticas, color=color)
        plt.title(f'Estatísticas Descritivas de {coluna}')
        plt.ylabel('Valor')
        plt.tight_layout()

        salvar_grafico(f'estatisticas_descritivas_{coluna}')
    else:
        print(f"A coluna '{coluna}' não existe no DataFrame.")


def plot_countplot_CRA(dataframe):
    if 'CRA' in dataframe.columns:
        dataframe['CRA'] = dataframe['CRA'].astype(str).str.replace(',', '.').astype(float)
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('viridis')[0]
        sns.countplot(x='CRA', data=dataframe, color=color)
        plt.title('Distribuição do CRA')
        plt.xlabel('CRA')
        plt.ylabel('Quantidade de Alunos')
        plt.tight_layout()
        salvar_grafico('distribuicao_CRA')
    else:
        print("A coluna 'CRA' não existe no DataFrame.")


def plot_distribuicao_sexo(dataframe):
    if 'SEXO' in dataframe.columns:
        plt.figure(figsize=(8, 6))
        palette_sexo = {'F': '#FF6347', 'M': '#4169E1'}
        sns.countplot(x='SEXO', data=dataframe, palette=palette_sexo)
        plt.title('Distribuição por Sexo')
        plt.xlabel('Sexo')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_sexo')
    else:
        print("A coluna 'SEXO' não existe no DataFrame.")


def plot_distribuicao_idade(dataframe):
    if 'IDADE' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('viridis')[0]
        sns.histplot(dataframe['IDADE'], kde=True, color=color)
        plt.title('Distribuição por Idade')
        plt.xlabel('Idade')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_idade')
    else:
        print("A coluna 'IDADE' não existe no DataFrame.")


def plot_distribuicao_evasao(dataframe):
    if 'STATUS_EVASAO' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('pastel')[0]
        sns.countplot(x='CRA', data=dataframe, color=color)
        plt.title('Distribuição de Evasões')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_evasao')
    else:
        print("A coluna 'STATUS_EVASAO' não existe no DataFrame.")


if __name__ == "__main__":
    df = carregar_dados()
    analise_exploratoria(df)
