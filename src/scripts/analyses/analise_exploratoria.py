import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils import criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_exploratoria(df):
    criar_pasta_graficos()
    print("\nIniciando Análise Exploratória...")

    plot_estatisticas_descritivas(df, 'CRA')
    plot_countplot_CRA(df)
    plot_distribuicao_sexo(df)
    plot_distribuicao_idade(df)
    plot_distribuicao_evasao(df)

    print("\nAnálise Exploratória Concluída!")


def plot_estatisticas_descritivas(df, coluna):
    if coluna in df.columns:
        desc = df[coluna].describe()
        var = df[coluna].var()
        skew = df[coluna].skew()
        kurt = df[coluna].kurtosis()

        estatisticas = pd.DataFrame({
            'Métrica': ['Média', 'Desvio Padrão', 'Variância', 'Assimetria', 'Curtose'],
            'Valor': [desc['mean'], desc['std'], var, skew, kurt]
        })

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Métrica', y='Valor', data=estatisticas, palette='viridis')
        plt.title(f'Estatísticas Descritivas de {coluna}')
        plt.ylabel('Valor')
        plt.tight_layout()

        salvar_grafico(f'estatisticas_descritivas_{coluna}')
    else:
        print(f"A coluna '{coluna}' não existe no DataFrame.")


def plot_countplot_CRA(df):
    if 'CRA' in df.columns:
        df['CRA'] = df['CRA'].astype(str).str.replace(',', '.').astype(float)
        plt.figure(figsize=(10, 6))
        sns.countplot(x='CRA', data=df, palette='viridis')
        plt.title('Distribuição do CRA')
        plt.xlabel('CRA')
        plt.ylabel('Quantidade de Alunos')
        plt.tight_layout()
        salvar_grafico('distribuicao_CRA')
    else:
        print("A coluna 'CRA' não existe no DataFrame.")


def plot_distribuicao_sexo(df):
    if 'SEXO' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(x='SEXO', data=df, palette=['#FF6347', '#4169E1'])
        plt.title('Distribuição por Sexo')
        plt.xlabel('Sexo')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_sexo')
    else:
        print("A coluna 'SEXO' não existe no DataFrame.")


def plot_distribuicao_idade(df):
    if 'IDADE' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df['IDADE'], kde=True, color='skyblue')
        plt.title('Distribuição por Idade')
        plt.xlabel('Idade')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_idade')
    else:
        print("A coluna 'IDADE' não existe no DataFrame.")


def plot_distribuicao_evasao(df):
    if 'STATUS_EVASAO' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(x='STATUS_EVASAO', data=df, palette='pastel')
        plt.title('Distribuição de Evasões')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_evasao')
    else:
        print("A coluna 'STATUS_EVASAO' não existe no DataFrame.")


if __name__ == "__main__":
    df = carregar_dados()
    analise_exploratoria(df)
