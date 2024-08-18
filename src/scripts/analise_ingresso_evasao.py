import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, init
from src.utils.plots import salvar_grafico, criar_grafico_de_contagem, plotar_histograma
from src.utils.utils import carregar_dados

# Inicializa o Colorama
init(autoreset=True)


def analise_ingresso_evasao(df_periodo, nome_pasta, periodo_nome):
    print(Fore.BLUE + f"\nIniciando Análise de Ingresso e Evasão para o período: {periodo_nome}")

    plot_media_cra_evasao(df_periodo, nome_pasta, periodo_nome)
    plot_distribuicao_ingresso(df_periodo, nome_pasta, periodo_nome)
    plot_evasao_detalhada(df_periodo, nome_pasta, periodo_nome)
    plot_evasao_sexo(df_periodo, nome_pasta, periodo_nome)
    plot_evasao_idade(df_periodo, nome_pasta, periodo_nome)
    plot_evasao_ao_longo_do_tempo(df_periodo, nome_pasta, periodo_nome)
    plot_evasao_por_periodo(df_periodo, nome_pasta, periodo_nome)
    plot_distribuicao_temporal_sexo(df_periodo, nome_pasta, periodo_nome)
    plot_distribuicao_temporal_idade(df_periodo, nome_pasta, periodo_nome)

    print(Fore.GREEN + f"\nAnálise de Ingresso e Evasão Concluída para o período: {periodo_nome}")


def plot_media_cra_evasao(dataframe, nome_pasta, periodo_nome):
    if 'STATUS_EVASAO' in dataframe.columns and 'CRA' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        # Dividido por 'FORMA_INGRESSO_SIMPLES'
        media_cra = dataframe.groupby(['STATUS_EVASAO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()
        ax = sns.barplot(x='STATUS_EVASAO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=media_cra, palette='pastel')

        # Adiciona os valores exatos em cima de cada barra
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', xytext=(0, 8), textcoords='offset points')

        # Título e ajustes
        plt.title(f'Média do CRA por Forma de Evasão - {periodo_nome}')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Média do CRA')

        # Remover rotação no eixo X
        plt.xticks(rotation=0)
        plt.tight_layout()
        salvar_grafico(f'media_cra_evasao_{periodo_nome}', nome_pasta)
    else:
        print(Fore.RED + "A coluna 'STATUS_EVASAO' ou 'CRA' não existe no DataFrame.")


def plot_distribuicao_ingresso(dataframe, nome_pasta, periodo_nome):
    criar_grafico_de_contagem(
        x='FORMA_INGRESSO_SIMPLES',
        data=dataframe,
        titulo=f'Distribuição de Cotistas e Não-Cotistas - {periodo_nome}',
        xlabel='Forma de Ingresso',
        ylabel='Porcentagem de Alunos (%)',
        exibir_percentual=True
    )
    salvar_grafico(f'distribuicao_ingresso_{periodo_nome}', nome_pasta)


def plot_evasao_detalhada(dataframe, nome_pasta, periodo_nome):
    # Filtra apenas os casos de evasão, removendo "Curso Concluído" e "Sem Evasão"
    evasao_filtrada = dataframe[~dataframe['FORMA_EVASAO_DETALHADA'].isin(['CON - Curso concluído', 'Sem evasão'])]

    # Calcula a porcentagem de evasões para cotistas e ampla concorrência
    total_evasao = len(evasao_filtrada)
    evasao_agrupada = evasao_filtrada.groupby(['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='contagem')
    evasao_agrupada['percentual'] = (evasao_agrupada['contagem'] / total_evasao) * 100

    # Substitui os valores do eixo X por apenas a primeira palavra
    evasao_agrupada['FORMA_EVASAO_DETALHADA'] = evasao_agrupada['FORMA_EVASAO_DETALHADA'].apply(lambda x: x.split()[0])

    # Cria o gráfico
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='FORMA_EVASAO_DETALHADA', y='percentual', hue='FORMA_INGRESSO_SIMPLES', data=evasao_agrupada, palette='pastel')

    # Adiciona o valor absoluto no topo de cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{int(height)}%', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    # Ajusta os rótulos e o título
    plt.title(f'Evasão por Tipo e Forma de Ingresso - {periodo_nome}')
    plt.xlabel('Tipo de Evasão')
    plt.ylabel('Porcentagem de Alunos (%)')

    # Cria a legenda explicativa dos códigos de evasão
    plt.legend(title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))
    legenda_evasao = "ABA = Abandono do Curso, CAN = Cancelamento Geral do Curso, JUB = Jubilamento, Desistencia = Desistencia SISU, FAL = Falecimento"
    plt.figtext(0.1, -0.1, legenda_evasao, ha="left", fontsize=8)

    plt.tight_layout()
    salvar_grafico(f'evasao_detalhada_{periodo_nome}', nome_pasta)


def plot_evasao_sexo(dataframe, nome_pasta, periodo_nome):
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas'],
                              hue='SEXO', titulo=f'Distribuição de Evasões por Sexo (Cotistas) - {periodo_nome}',
                              xlabel='Forma de Evasão', ylabel='Quantidade')

    plt.subplot(1, 2, 2)
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia'],
                              hue='SEXO', titulo=f'Distribuição de Evasões por Sexo (Não Cotistas) - {periodo_nome}',
                              xlabel='Forma de Evasão', ylabel='Quantidade')

    plt.tight_layout()
    salvar_grafico(f'evasao_sexo_{periodo_nome}', nome_pasta)


def plot_evasao_idade(dataframe, nome_pasta, periodo_nome):
    # Calcula a idade no momento da evasão
    dataframe['IDADE_EVASAO'] = dataframe['ANO_PERIODO_EVASAO'] - dataframe['DT_NASCIMENTO'].year

    # Calcula a porcentagem de evasões por idade de evasão
    total_evasao = len(dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'])
    idade_agrupada = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby('IDADE_EVASAO').size().reset_index(name='contagem')
    idade_agrupada['percentual'] = (idade_agrupada['contagem'] / total_evasao) * 100

    # Cria o histograma com porcentagens no eixo Y
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='IDADE_EVASAO', y='percentual', data=idade_agrupada, palette='pastel')

    # Adiciona o valor absoluto no topo de cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{int(height)}%', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    # Ajusta os rótulos e o título
    plt.title(f'Distribuição de Idades dos Alunos na Evasão - {periodo_nome}')
    plt.xlabel('Idade no Momento da Evasão')
    plt.ylabel('Porcentagem de Alunos (%)')

    # Definir os ticks do eixo X para serem inteiros
    ax.set_xticks(range(int(idade_agrupada['IDADE_EVASA'].min()), int(idade_agrupada['IDADE_EVASA'].max()) + 1))

    plt.tight_layout()
    salvar_grafico(f'evasao_idade_evasa_{periodo_nome}', nome_pasta)


def plot_evasao_ao_longo_do_tempo(dataframe, nome_pasta, periodo_nome):
    evasao_por_periodo = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'FORMA_INGRESSO_SIMPLES']).size().unstack().fillna(0)
    evasao_por_periodo.plot(kind='bar', stacked=True, figsize=(14, 6))
    plt.title(f'Distribuição de Evasão por Período - {periodo_nome}')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Alunos Evadidos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'evasao_ao_longo_do_tempo_{periodo_nome}', nome_pasta)


def plot_evasao_por_periodo(df, nome_pasta, periodo_nome, periodo_inicio, periodo_fim):
    # Filtrar os dados para o período especificado
    evadidos = df[(df['STATUS_EVASAO'] == 'Evasão') & (df['PERIODO_EVASAO'] >= periodo_inicio) & (df['PERIODO_EVASAO'] <= periodo_fim)].copy()
    evadidos.loc[:, 'PERIODO_EVASAO'] = (evadidos['TEMPO_CURSO'] * 2).round().astype(int)

    plt.figure(figsize=(12, 7))
    sns.histplot(data=evadidos, x='PERIODO_EVASAO', hue='FORMA_INGRESSO_SIMPLES', multiple='stack', bins=range(1, 14),
                 palette='pastel', edgecolor='black')
    plt.title(f'Distribuição de Evasão por Período do Curso - {periodo_nome} (Cotistas vs Ampla Concorrência)')
    plt.xlabel('Período do Curso')
    plt.ylabel('Número de Evasões')
    plt.xticks(range(1, 13))
    plt.tight_layout()
    salvar_grafico(f'evasao_por_periodo_{periodo_nome}', nome_pasta)


def plot_distribuicao_temporal_sexo(dataframe, nome_pasta, periodo_nome):
    evasao_temporal = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'SEXO']).size().unstack().fillna(0)
    plt.figure(figsize=(14, 6))
    evasao_temporal.plot(kind='line', ax=plt.gca(), marker='o')
    plt.title(f'Evasão ao Longo do Tempo por Sexo - {periodo_nome}')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Evasões')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'evasao_temporal_sexo_{periodo_nome}', nome_pasta)


def plot_distribuicao_temporal_idade(dataframe, nome_pasta, periodo_nome):
    evasao_temporal_idade = dataframe.groupby(['PERIODO_EVASAO_FORMATADO', 'IDADE_INGRESSO']).size().unstack().fillna(0)
    plt.figure(figsize=(14, 6))
    evasao_temporal_idade.plot(kind='line', ax=plt.gca(), marker='o')
    plt.title(f'Evasão ao Longo do Tempo por Idade - {periodo_nome}')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Evasões')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'evasao_temporal_idade_{periodo_nome}', nome_pasta)


def plot_distribuicao_idade_por_sexo(dataframe, nome_pasta, periodo_nome):
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='IDADE_INGRESSO', data=dataframe, palette='pastel')
    plt.title(f'Distribuição da Idade no Ingresso por Sexo - {periodo_nome}')
    plt.xlabel('Sexo')
    plt.ylabel('Idade no Ingresso')
    plt.tight_layout()
    salvar_grafico(f'distribuicao_idade_por_sexo_{periodo_nome}', nome_pasta)


def plot_tempo_curso_por_forma_evasao(dataframe, nome_pasta, periodo_nome):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='FORMA_EVASAO', y='TEMPO_CURSO', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title(f'Distribuição do Tempo de Curso por Forma de Evasão - {periodo_nome}')
    plt.xlabel('Forma de Evasão')
    plt.ylabel('Tempo de Curso (Períodos)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'tempo_curso_por_forma_evasao_{periodo_nome}', nome_pasta)


def plot_evasao_por_cra_arredondado(dataframe, nome_pasta, periodo_nome):
    plt.figure(figsize=(12, 6))
    sns.countplot(x='CRA_ARREDONDADO', hue='STATUS_EVASAO', data=dataframe, palette='pastel')
    plt.title(f'Distribuição de Evasão por Nível de CRA Arredondado - {periodo_nome}')
    plt.xlabel('CRA Arredondado')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico(f'evasao_por_cra_arredondado_{periodo_nome}', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df, "resultados_ingresso_evasao", "2023")
