import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, init

from src.utils.plots import salvar_grafico
from src.utils.utils import carregar_dados

# Inicializa o Colorama
init(autoreset=True)


def analise_performance_academica(df_periodo, nome_pasta):
    print(Fore.BLUE + "\nIniciando Análise de Performance Acadêmica...")

    plot_distribuicao_cra(df_periodo, nome_pasta, 'performance_academica')
    plot_distribuicao_cra_sexo(df_periodo, nome_pasta, 'performance_academica')
    plot_distribuicao_cra_idade(df_periodo, nome_pasta, 'performance_academica')
    plot_impacto_cra_evasao(df_periodo, nome_pasta, 'performance_academica')
    plot_cra_medio_por_ano_ingresso(df_periodo, nome_pasta, 'performance_academica')
    plot_cra_medio_por_periodo_curso(df_periodo, nome_pasta, 'performance_academica')

    # Exibir diferença de tempo de término
    plot_diferenca_media_tempo_termino(df_periodo, nome_pasta, 'performance_academica')

    print(Fore.GREEN + "\nAnálise de Performance Acadêmica Concluída!")


def plot_distribuicao_cra(dataframe, nome_pasta, periodo):
    """
    Plota a distribuição do CRA para Cotistas e Ampla Concorrência.
    """
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe, inner='quartile')
    plt.title(f'Distribuição do CRA por Forma de Ingresso - {periodo}')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'distribuicao_cra_{periodo}', nome_pasta)


def plot_distribuicao_cra_sexo(dataframe, nome_pasta, periodo):
    """
    Função para plotar a distribuição do CRA por sexo e forma de ingresso.
    """
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title(f'Distribuição do CRA por Sexo e Forma de Ingresso - {periodo}')
    plt.xlabel('Sexo')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'distribuicao_cra_sexo_{periodo}', nome_pasta)


def plot_distribuicao_cra_idade(dataframe, nome_pasta, periodo):
    """
    Plota a distribuição do CRA por Idade e Forma de Ingresso.
    """
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='IDADE_INGRESSO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title(f'Distribuição do CRA por Idade e Forma de Ingresso - {periodo}')
    plt.xlabel('Idade no Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'distribuicao_cra_idade_{periodo}', nome_pasta)


def plot_impacto_cra_evasao(dataframe, nome_pasta, periodo):
    """
    Plota o impacto do CRA sobre a evasão, comparando cotistas e ampla concorrência.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='STATUS_EVASAO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe)
    plt.title(f'Impacto do CRA sobre a Evasão por Forma de Ingresso - {periodo}')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'impacto_cra_evasao_{periodo}', nome_pasta)


def plot_cra_medio_por_ano_ingresso(dataframe, nome_pasta, periodo):
    """
    Plota o CRA médio ao longo dos anos de ingresso, separado por cotistas e ampla concorrência.
    """
    cra_medio = dataframe.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    plt.figure(figsize=(14, 7))
    sns.lineplot(x='ANO_PERIODO_INGRESSO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio, marker='o')
    plt.title(f'CRA Médio ao Longo dos Anos de Ingresso - {periodo}')
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'cra_medio_por_ano_ingresso_{periodo}', nome_pasta)


def plot_cra_medio_por_periodo_curso(dataframe, nome_pasta, periodo):
    """
    Plota o CRA médio por período do curso, considerando o tempo de curso dos alunos.
    """
    dataframe['TEMPO_CURSO'] = dataframe['TEMPO_CURSO'].replace(0, 1).fillna(1)
    dataframe['PERIODO_CURSO_ATUAL'] = (dataframe['TEMPO_CURSO'] * 2).round().astype(int)

    cra_medio_por_periodo = dataframe.groupby(['PERIODO_CURSO_ATUAL', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    plt.figure(figsize=(14, 7))
    sns.lineplot(x='PERIODO_CURSO_ATUAL', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio_por_periodo, marker='o')
    plt.title(f'CRA Médio por Período do Curso - {periodo}')
    plt.xlabel('Período do Curso')
    plt.ylabel('CRA Médio')
    plt.tight_layout()
    salvar_grafico(f'cra_medio_por_periodo_curso_{periodo}', nome_pasta)


def plot_diferenca_media_tempo_termino(dataframe, nome_pasta, periodo):
    # Filtra os alunos que já concluíram o curso
    concluidos = dataframe[dataframe['STATUS_EVASAO'] == 'Concluído']

    # Verifica se há dados de cotistas para o período analisado
    if 'Cotas' in concluidos['FORMA_INGRESSO_SIMPLES'].unique():
        medias = concluidos.groupby('FORMA_INGRESSO_SIMPLES')['TEMPO_CURSO'].mean().reset_index()

        # Exibe as médias em um gráfico de barras
        plt.figure(figsize=(8, 6))
        sns.barplot(x='FORMA_INGRESSO_SIMPLES', y='TEMPO_CURSO', data=medias, palette='pastel')
        plt.title(f'Diferença de Tempo de Término entre Cotistas e Não Cotistas - {periodo}')
        plt.xlabel('Forma de Ingresso')
        plt.ylabel('Média de Tempo de Curso (Períodos)')
        plt.tight_layout()
        salvar_grafico(f'diferenca_media_tempo_termino_{periodo}', nome_pasta)
    else:
        print(Fore.YELLOW + f"\nAviso: Não há dados de cotistas para o período {periodo}.")


if __name__ == "__main__":
    df = carregar_dados()
    analise_performance_academica(df)
