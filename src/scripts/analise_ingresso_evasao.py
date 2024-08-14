import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, Style, init
from src.utils.plots import salvar_grafico, criar_grafico_de_contagem, plotar_histograma
from src.utils.utils import carregar_dados

# Inicializa o Colorama
init(autoreset=True)


def analise_ingresso_evasao(df_periodo, nome_pasta):
    print(Fore.BLUE + "\nIniciando Análise de Ingresso e Evasão...")

    plot_media_cra_evasao(df_periodo, nome_pasta)
    plot_distribuicao_ingresso(df_periodo, nome_pasta)
    plot_evasao_detalhada(df_periodo, nome_pasta)
    plot_evasao_sexo(df_periodo, nome_pasta)
    plot_evasao_idade(df_periodo, nome_pasta)
    plot_evasao_ao_longo_do_tempo(df_periodo, nome_pasta)
    plot_evasao_por_periodo(df_periodo, nome_pasta)
    plot_distribuicao_temporal_sexo(df_periodo, nome_pasta)
    plot_distribuicao_temporal_idade(df_periodo, nome_pasta)

    print(Fore.GREEN + "\nAnálise de Ingresso e Evasão Concluída!")


def plot_media_cra_evasao(dataframe, nome_pasta):
    if 'STATUS_EVASAO' in dataframe.columns and 'CRA' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        media_cra = dataframe.groupby('STATUS_EVASAO')['CRA'].mean().reset_index()
        sns.barplot(x='STATUS_EVASAO', y='CRA', data=media_cra)
        plt.title('Média do CRA por Forma de Evasão')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Média do CRA')
        plt.xticks(rotation=45)
        plt.tight_layout()
        salvar_grafico('media_cra_evasao', nome_pasta)
    else:
        print(Fore.RED + "A coluna 'STATUS_EVASAO' ou 'CRA' não existe no DataFrame.")


def plot_distribuicao_ingresso(dataframe, nome_pasta):
    criar_grafico_de_contagem(x='FORMA_INGRESSO_SIMPLES', data=dataframe,
                              titulo='Distribuição de Cotistas e Não-Cotistas',
                              xlabel='Forma de Ingresso', ylabel='Quantidade')
    salvar_grafico('distribuicao_ingresso', nome_pasta)


def plot_evasao_detalhada(dataframe, nome_pasta):
    if 'FORMA_EVASAO_DETALHADA' in dataframe.columns:
        plt.figure(figsize=(12, 6))
        sns.countplot(x='FORMA_EVASAO_DETALHADA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
        plt.title('Evasão Detalhada por Tipo e Forma de Ingresso')
        plt.xlabel('Tipo de Evasão')
        plt.ylabel('Quantidade')
        plt.xticks(rotation=45)
        plt.tight_layout()
        salvar_grafico('evasao_detalhada', nome_pasta)
    else:
        print(Fore.RED + "A coluna 'FORMA_EVASAO_DETALHADA' não existe no DataFrame.")


def plot_evasao_sexo(dataframe, nome_pasta):
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas'],
                              hue='SEXO', titulo='Distribuição de Evasões por Sexo (Cotistas)',
                              xlabel='Forma de Evasão', ylabel='Quantidade')

    plt.subplot(1, 2, 2)
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia'],
                              hue='SEXO', titulo='Distribuição de Evasões por Sexo (Não Cotistas)',
                              xlabel='Forma de Evasão', ylabel='Quantidade')

    plt.tight_layout()
    salvar_grafico('evasao_sexo', nome_pasta)


def plot_evasao_idade(dataframe, nome_pasta):
    plotar_histograma(x=dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']['IDADE_INGRESSO'], data=dataframe,
                      titulo='Distribuição de Idades dos Alunos com Evasão', xlabel='Idade', ylabel='Quantidade')
    salvar_grafico('evasao_idade', nome_pasta)


def plot_evasao_ao_longo_do_tempo(dataframe, nome_pasta):
    evasao_por_periodo = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'FORMA_INGRESSO_SIMPLES']).size().unstack().fillna(0)
    evasao_por_periodo.plot(kind='bar', stacked=True, figsize=(14, 6))
    plt.title('Distribuição de Evasão por Período')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Alunos Evadidos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('evasao_ao_longo_do_tempo', nome_pasta)


def plot_evasao_por_periodo(df, nome_pasta):
    evadidos = df[df['STATUS_EVASAO'] == 'Evasão'].copy()
    evadidos.loc[:, 'PERIODO_EVASAO'] = (evadidos['TEMPO_CURSO'] * 2).round().astype(int)
    plt.figure(figsize=(12, 7))
    sns.histplot(data=evadidos, x='PERIODO_EVASAO', hue='FORMA_INGRESSO_SIMPLES', multiple='stack', bins=range(1, 14),
                 palette='pastel', edgecolor='black')
    plt.title('Distribuição de Evasão por Período do Curso (Cotistas vs Ampla Concorrência)')
    plt.xlabel('Período do Curso')
    plt.ylabel('Número de Evasões')
    plt.xticks(range(1, 13))
    plt.tight_layout()
    salvar_grafico('evasao_por_periodo', nome_pasta)


def plot_distribuicao_temporal_sexo(dataframe, nome_pasta):
    evasao_temporal = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'SEXO']).size().unstack().fillna(0)
    plt.figure(figsize=(14, 6))
    evasao_temporal.plot(kind='line', ax=plt.gca(), marker='o')
    plt.title('Evasão ao Longo do Tempo por Sexo')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Evasões')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('evasao_temporal_sexo', nome_pasta)


def plot_distribuicao_temporal_idade(dataframe, nome_pasta):
    evasao_temporal_idade = dataframe.groupby(['PERIODO_EVASAO_FORMATADO', 'IDADE_INGRESSO']).size().unstack().fillna(0)
    plt.figure(figsize=(14, 6))
    evasao_temporal_idade.plot(kind='line', ax=plt.gca(), marker='o')
    plt.title('Evasão ao Longo do Tempo por Idade')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Evasões')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('evasao_temporal_idade', nome_pasta)


def plot_distribuicao_idade_por_sexo(dataframe, nome_pasta):
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='IDADE_INGRESSO', data=dataframe, palette='pastel')
    plt.title('Distribuição da Idade no Ingresso por Sexo')
    plt.xlabel('Sexo')
    plt.ylabel('Idade no Ingresso')
    plt.tight_layout()
    salvar_grafico('distribuicao_idade_por_sexo', nome_pasta)


def plot_tempo_curso_por_forma_evasao(dataframe, nome_pasta):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='FORMA_EVASAO', y='TEMPO_CURSO', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title('Distribuição do Tempo de Curso por Forma de Evasão')
    plt.xlabel('Forma de Evasão')
    plt.ylabel('Tempo de Curso (Períodos)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('tempo_curso_por_forma_evasao', nome_pasta)


def plot_evasao_por_cra_arredondado(dataframe, nome_pasta):
    plt.figure(figsize=(12, 6))
    sns.countplot(x='CRA_ARREDONDADO', hue='STATUS_EVASAO', data=dataframe, palette='pastel')
    plt.title('Distribuição de Evasão por Nível de CRA Arredondado')
    plt.xlabel('CRA Arredondado')
    plt.ylabel('Quantidade de Alunos')
    plt.tight_layout()
    salvar_grafico('evasao_por_cra_arredondado', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df)
