import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, init

from src.utils.plots import salvar_grafico, adicionar_valores_barras, ajustar_estilos_grafico
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
    total_original = len(dataframe)
    dataframe_filtrado = dataframe[dataframe['CRA'].notnull()]
    registros_descartados = total_original - len(dataframe_filtrado)

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.RED + f"Total de registros descartados (CRA nulo): {registros_descartados}")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe_filtrado, palette='muted', ax=ax)

    ajustar_estilos_grafico(ax, title=f'Distribuição do CRA por Forma de Ingresso', xlabel='Forma de Ingresso', ylabel='CRA')
    salvar_grafico(f'distribuicao_cra_{periodo_nome}', nome_pasta)


def plot_distribuicao_cra_sexo(dataframe, nome_pasta, periodo_nome):
    """
    Função para plotar a distribuição do CRA por sexo e forma de ingresso usando boxplot.
    """
    total_original = len(dataframe)
    dataframe_filtrado = dataframe[dataframe['CRA'].notnull()]
    registros_descartados = total_original - len(dataframe_filtrado)

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.RED + f"Total de registros descartados (CRA nulo): {registros_descartados}")

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe_filtrado, palette='pastel', ax=ax)

    ajustar_estilos_grafico(ax, title=f'Distribuição do CRA por Sexo e Forma de Ingresso', xlabel='Sexo', ylabel='CRA')
    salvar_grafico(f'distribuicao_cra_sexo_{periodo_nome}', nome_pasta)


def plot_impacto_cra_evasao(dataframe, nome_pasta, periodo_nome):
    """
    Plota o impacto do CRA sobre a evasão, comparando cotistas e ampla concorrência usando boxplot.
    """
    total_original = len(dataframe)
    dataframe_filtrado = dataframe[dataframe['CRA'].notnull()]
    registros_descartados = total_original - len(dataframe_filtrado)

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.RED + f"Total de registros descartados (CRA nulo): {registros_descartados}")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='STATUS_EVASAO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe_filtrado, palette='pastel', ax=ax)

    ajustar_estilos_grafico(ax, title=f'Impacto do CRA sobre a Evasão por Forma de Ingresso', xlabel='Status de Evasão', ylabel='CRA')
    salvar_grafico(f'impacto_cra_evasao_{periodo_nome}', nome_pasta)


def plot_cra_medio_por_ano_ingresso(dataframe, nome_pasta, periodo_nome):
    """
    Plota o CRA médio ao longo dos anos de ingresso, separado por cotistas e ampla concorrência.
    """
    total_original = len(dataframe)
    dataframe_filtrado = dataframe[dataframe['CRA'].notnull()]
    registros_descartados = total_original - len(dataframe_filtrado)

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.RED + f"Total de registros descartados (CRA nulo): {registros_descartados}")

    cra_medio = dataframe_filtrado.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(x='ANO_PERIODO_INGRESSO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio, marker='o', ax=ax)

    ajustar_estilos_grafico(ax, title=f'CRA Geral do Curso ao Longo dos Anos', xlabel='Ano de Ingresso', ylabel='CRA Médio')
    salvar_grafico(f'cra_medio_por_ano_ingresso_{periodo_nome}', nome_pasta)


def plot_cra_medio_por_periodo_curso(dataframe, nome_pasta, periodo_nome):
    """
    Plota o CRA médio por período do curso, considerando o tempo de curso dos alunos.
    """
    total_original = len(dataframe)
    dataframe_filtrado = dataframe[dataframe['CRA'].notnull()]
    registros_descartados = total_original - len(dataframe_filtrado)

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.RED + f"Total de registros descartados (CRA nulo): {registros_descartados}")

    dataframe_filtrado['TEMPO_CURSO'] = dataframe_filtrado['TEMPO_CURSO'].replace(0, 1).fillna(1)
    dataframe_filtrado['PERIODO_CURSO_ATUAL'] = (dataframe_filtrado['TEMPO_CURSO'] * 2).round().astype(int)

    cra_medio_por_periodo = dataframe_filtrado.groupby(['PERIODO_CURSO_ATUAL', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(x='PERIODO_CURSO_ATUAL', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=cra_medio_por_periodo, marker='o', ax=ax)

    ajustar_estilos_grafico(ax, title=f'CRA Médio dos Alunos ao Longo dos Períodos', xlabel='Período do Curso', ylabel='CRA Médio dos Alunos')
    salvar_grafico(f'cra_medio_por_periodo_{periodo_nome}', nome_pasta)


def plot_diferenca_media_tempo_termino(dataframe, nome_pasta, periodo_nome):
    # Filtra os alunos que já concluíram o curso
    total_original = len(dataframe)
    concluidos = dataframe[(dataframe['STATUS_EVASAO'] == 'Concluído') & dataframe['TEMPO_CURSO'].notnull()]
    registros_descartados = total_original - len(concluidos)

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.RED + f"Total de registros descartados (não concluíram ou tempo de curso nulo): {registros_descartados}")

    medias = concluidos.groupby('FORMA_INGRESSO_SIMPLES')['TEMPO_CURSO'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='FORMA_INGRESSO_SIMPLES', y='TEMPO_CURSO', data=medias, palette='pastel', ax=ax)

    adicionar_valores_barras(ax, exibir_percentual=False)

    ajustar_estilos_grafico(ax, title=f'Média de Tempo de Término do Curso', xlabel='Forma de Ingresso', ylabel='Média de Tempo de Curso (Anos)')
    salvar_grafico(f'diferenca_media_tempo_termino_{periodo_nome}', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_desempenho_academico(df, 'resultados_performance', '2023')
