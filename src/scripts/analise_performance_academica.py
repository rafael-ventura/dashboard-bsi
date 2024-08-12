import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.utils.plots import criar_pasta_graficos, salvar_grafico
from src.utils.utils import carregar_dados


def analise_performance_academica(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise de Performance Acadêmica...")

    plot_distribuicao_cra(dataframe)
    plot_comparacao_cra(dataframe)
    plot_impacto_cra_evasao(dataframe)
    plot_cra_medio_por_ano_ingresso(dataframe)
    plot_cra_medio_por_periodo_curso(dataframe)
    plot_distribuicao_cra_sexo(dataframe)

    print("\nAnálise de Performance Acadêmica Concluída!")


def plot_distribuicao_cra(dataframe):
    """
    Plota a distribuição do CRA para Cotistas e Ampla Concorrência.
    """
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe, inner='quartile')
    plt.title('Distribuição do CRA por Forma de Ingresso')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('distribuicao_cra')


def plot_comparacao_cra(dataframe):
    """
    Plota a comparação das médias e medianas do CRA entre cotistas e ampla concorrência.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe)
    plt.title('Comparação do CRA entre Cotistas e Ampla Concorrência')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('comparacao_cra')


def plot_impacto_cra_evasao(dataframe):
    """
    Plota o impacto do CRA sobre a evasão, comparando cotistas e ampla concorrência.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='STATUS_EVASAO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe)
    plt.title('Impacto do CRA sobre a Evasão por Forma de Ingresso')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('impacto_cra_evasao')


def plot_cra_medio_por_ano_ingresso(dataframe):
    """
    Plota o CRA médio ao longo dos anos de ingresso, separado por cotistas e ampla concorrência.
    """
    # Agrupa por ano de ingresso e forma de ingresso
    cra_medio = dataframe.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    plt.figure(figsize=(14, 7))
    sns.lineplot(x='ANO_PERIODO_INGRESSO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio, marker='o')
    plt.title('CRA Médio ao Longo dos Anos de Ingresso')
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('cra_medio_por_ano_ingresso')


def plot_cra_medio_por_periodo_curso(dataframe):
    """
    Plota o CRA médio por período do curso, considerando o tempo de curso dos alunos.
    """
    # Substitui valores 0 por 1 na coluna TEMPO_CURSO
    dataframe['TEMPO_CURSO'] = dataframe['TEMPO_CURSO'].replace(0, 1).fillna(1)

    # Calcula em qual período do curso o aluno está atualmente
    dataframe['PERIODO_CURSO_ATUAL'] = (dataframe['TEMPO_CURSO'] * 2).round().astype(int)

    # Agrupa por período do curso e forma de ingresso
    cra_medio_por_periodo = dataframe.groupby(['PERIODO_CURSO_ATUAL', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    plt.figure(figsize=(14, 7))
    sns.lineplot(x='PERIODO_CURSO_ATUAL', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio_por_periodo, marker='o')
    plt.title('CRA Médio por Período do Curso')
    plt.xlabel('Período do Curso')
    plt.ylabel('CRA Médio')
    plt.tight_layout()
    salvar_grafico('cra_medio_por_periodo_curso')


def plot_distribuicao_cra_sexo(dataframe):
    """
    Função para plotar a distribuição do CRA por sexo e forma de ingresso.
    """
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title('Distribuição do CRA por Sexo e Forma de Ingresso')
    plt.xlabel('Sexo')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('distribuicao_cra_sexo')


if __name__ == "__main__":
    df = carregar_dados()
    analise_performance_academica(df)
