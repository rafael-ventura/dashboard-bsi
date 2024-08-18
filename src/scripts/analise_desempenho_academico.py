import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, init

from src.utils.plots import salvar_grafico, plotar_grafico_caixa_com_estatisticas
from src.utils.utils import carregar_dados

# Inicializa o Colorama
init(autoreset=True)


def analise_desempenho_academico(df_periodo, nome_pasta, periodo_nome):
    print(Fore.BLUE + f"\nIniciando Análise de Performance Acadêmica para o período: {periodo_nome}")

    plot_distribuicao_cra(df_periodo, nome_pasta, periodo_nome)
    plot_distribuicao_cra_sexo(df_periodo, nome_pasta, periodo_nome)
    plot_impacto_cra_evasao(df_periodo, nome_pasta, periodo_nome)
    plot_cra_medio_por_ano_ingresso(df_periodo, nome_pasta, periodo_nome)
    plot_cra_medio_por_periodo_curso(df_periodo, nome_pasta, periodo_nome)

    # Exibir diferença de tempo de término
    plot_diferenca_media_tempo_termino(df_periodo, nome_pasta, periodo_nome)

    print(Fore.GREEN + f"\nAnálise de Performance Acadêmica Concluída para o período: {periodo_nome}")


def plot_distribuicao_cra(dataframe, nome_pasta, periodo_nome):
    """
    Plota a distribuição do CRA para Cotistas e Ampla Concorrência usando boxplot.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe, palette='muted')
    plt.title(f'Distribuição do CRA por Forma de Ingresso - {periodo_nome}')
    plt.xlabel('Forma de Ingresso')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'distribuicao_cra_{periodo_nome}', nome_pasta)


def plot_distribuicao_cra_sexo(dataframe, nome_pasta, periodo_nome):
    """
    Função para plotar a distribuição do CRA por sexo e forma de ingresso usando boxplot.
    """
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title(f'Distribuição do CRA por Sexo e Forma de Ingresso - {periodo_nome}')
    plt.xlabel('Sexo')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'distribuicao_cra_sexo_{periodo_nome}', nome_pasta)


def plot_impacto_cra_evasao(dataframe, nome_pasta, periodo_nome):
    """
    Plota o impacto do CRA sobre a evasão, comparando cotistas e ampla concorrência usando boxplot.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='STATUS_EVASAO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title(f'Impacto do CRA sobre a Evasão por Forma de Ingresso - {periodo_nome}')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico(f'impacto_cra_evasao_{periodo_nome}', nome_pasta)


def plot_cra_medio_por_ano_ingresso(dataframe, nome_pasta, periodo_nome):
    """
    Plota o CRA médio ao longo dos anos de ingresso, separado por cotistas e ampla concorrência.
    """
    cra_medio = dataframe.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    plt.figure(figsize=(14, 7))
    sns.lineplot(x='ANO_PERIODO_INGRESSO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio, marker='o')
    plt.title(f'CRA Geral do Curso ao Longo dos Anos - {periodo_nome}')  # Alterado o título
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'cra_medio_por_ano_ingresso_{periodo_nome}', nome_pasta)


def plot_cra_medio_por_periodo_curso(dataframe, nome_pasta, periodo_nome):
    """
    Plota o CRA médio por período do curso, considerando o tempo de curso dos alunos.
    """
    # Ajustando o cálculo do período atual do curso
    dataframe['TEMPO_CURSO'] = dataframe['TEMPO_CURSO'].replace(0, 1).fillna(1)
    dataframe['PERIODO_CURSO_ATUAL'] = (dataframe['TEMPO_CURSO'] * 2).round().astype(int)

    # Calcula o CRA médio por período e por forma de ingresso
    cra_medio_por_periodo = dataframe.groupby(['PERIODO_CURSO_ATUAL', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    # Configuração do gráfico
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='PERIODO_CURSO_ATUAL', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio_por_periodo, marker='o')

    # Título explicando o que o gráfico representa
    plt.title(f'CRA Médio dos Alunos ao Longo dos Períodos - {periodo_nome}')

    # Rótulos explicando melhor os eixos
    plt.xlabel('Período do Curso')
    plt.ylabel('CRA Médio dos Alunos')

    # Ajuste dos ticks no eixo X para garantir que todos os períodos sejam exibidos corretamente
    max_periodo = dataframe['PERIODO_CURSO_ATUAL'].max()
    plt.xticks(ticks=[x / 2 for x in range(1, int(max_periodo * 2 + 1))])

    # Ajustando o layout e salvando o gráfico
    plt.tight_layout()
    salvar_grafico(f'cra_medio_por_periodo_{periodo_nome}', nome_pasta)


def plot_diferenca_media_tempo_termino(dataframe, nome_pasta, periodo_nome):
    # Filtra os alunos que já concluíram o curso
    concluidos = dataframe[dataframe['STATUS_EVASAO'] == 'Concluído']

    # Verifica se há dados de cotistas para o período analisado
    if 'Cotas' in concluidos['FORMA_INGRESSO_SIMPLES'].unique():
        medias = concluidos.groupby('FORMA_INGRESSO_SIMPLES')['TEMPO_CURSO'].mean().reset_index()

        # Exibe as médias em um gráfico de barras
        plt.figure(figsize=(8, 6))
        sns.barplot(x='FORMA_INGRESSO_SIMPLES', y='TEMPO_CURSO', data=medias, palette='pastel')
        plt.title(f'Diferença de Tempo de Término entre Cotistas e Não Cotistas - {periodo_nome}')
        plt.xlabel('Forma de Ingresso')
        plt.ylabel('Média de Tempo de Curso (Anos)')  # Alterado de 'Períodos' para 'Anos'
        plt.tight_layout()
        salvar_grafico(f'diferenca_media_tempo_termino_{periodo_nome}', nome_pasta)
    else:
        print(Fore.YELLOW + f"\nAviso: Não há dados de cotistas para o período {periodo_nome}.")


if __name__ == "__main__":
    df = carregar_dados()
    analise_desempenho_academico(df, 'resultados_performance', '2023')
