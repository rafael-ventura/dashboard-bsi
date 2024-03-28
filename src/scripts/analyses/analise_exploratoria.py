import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


def criar_pasta_graficos():
    if not os.path.exists('../../graficos'):
        os.makedirs('../../graficos')
        print("Pasta 'graficos' criada com sucesso!")


def estatisticas_descritivas(df):
    # Criar um DataFrame com estatísticas descritivas
    desc = df.describe(include='all', datetime_is_numeric=True)

    # Salvar as estatísticas descritivas em um arquivo de imagem
    plt.figure(figsize=(10, 6))
    sns.barplot(data=desc, palette='muted')
    plt.title('Estatísticas Descritivas')
    plt.ylabel('Valor')
    plt.xlabel('Tipo de Estatística')
    plt.grid(True)
    salvar_grafico('estatisticas_descritivas')


def salvar_grafico(nome_grafico):
    plt.savefig(f'../../graficos/{nome_grafico}.png')
    plt.close()


def plot_countplot_CRA(df):
    # Substituir vírgulas por pontos na coluna 'CRA' e converter para float
    df['CRA'] = df['CRA'].str.replace(',', '.').astype(float)

    # Contar a quantidade de alunos para cada valor de CRA
    cra_counts = df['CRA'].value_counts().sort_index()

    # Plotar o gráfico de barras com as notas de CRA no eixo x e a contagem de alunos no eixo y
    plt.figure(figsize=(10, 6))
    sns.barplot(x=cra_counts.index, y=cra_counts.values, palette='viridis')
    plt.title('Distribuição do CRA')
    plt.xlabel('CRA')
    plt.ylabel('Quantidade de Alunos')
    plt.grid(True)
    plt.tight_layout()
    # Salvar o gráfico
    salvar_grafico('distribuicao_CRA')




def plot_distribuicao_sexo(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='SEXO', data=df, hue='SEXO', palette=['#FF6347', '#4169E1'], legend=False)
    plt.title('Distribuição por Sexo')
    plt.xlabel('Sexo')
    plt.ylabel('Quantidade')
    salvar_grafico('distribuicao_sexo')


def plot_distribuicao_idade(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['IDADE'], kde=True, color='skyblue')
    plt.title('Distribuição por Idade')
    plt.xlabel('Idade')
    plt.ylabel('Quantidade')
    salvar_grafico('distribuicao_idade')


def plot_distribuicao_evasao(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='STATUS_EVASAO', data=df, palette='pastel')
    plt.title('Distribuição de Evasões')
    plt.xlabel('Forma de Evasão')
    plt.ylabel('Quantidade')
    salvar_grafico('distribuicao_evasao')


def analise_exploratoria(df):
    criar_pasta_graficos()
    print("\nIniciando Análise Exploratória...")
    estatisticas_descritivas(df)
    plot_countplot_CRA(df)
    plot_distribuicao_sexo(df)
    plot_distribuicao_idade(df)
    plot_distribuicao_evasao(df)
    print("\nAnálise Exploratória Concluída!")


if __name__ == "__main__":
    df = pd.read_csv('C:\Dev\dashboard-bsi\dados\processado\dfPrincipal.csv')
    analise_exploratoria(df)
