import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, Style, init
from src.utils.plots import criar_pasta_graficos, criar_grafico_de_contagem, salvar_grafico, plotar_histograma
from src.utils.utils import carregar_dados

# Inicializa o Colorama
init(autoreset=True)


def analise_ingresso_evasao(dataframe):
    criar_pasta_graficos()
    print(Fore.BLUE + "\nIniciando Análise de Ingresso e Evasão...")

    exibir_diferenca_media_tempo_termino(dataframe)
    exibir_porcentagem_concluidos_evasao_cursando(dataframe)
    exibir_porcentagem_bairros_evasao_concluidos(dataframe)

    plot_media_cra_evasao(dataframe)
    plot_distribuicao_ingresso(dataframe)
    plot_evasao_sexo(dataframe)
    plot_evasao_idade(dataframe)
    plot_evasao_ao_longo_do_tempo(dataframe)
    plot_evasao_por_periodo(dataframe)

    print(Fore.GREEN + "\nAnálise de Ingresso e Evasão Concluída!")


def exibir_diferenca_media_tempo_termino(dataframe):
    # Filtra os alunos que já concluíram o curso
    concluidos = dataframe[dataframe['STATUS_EVASAO'] == 'Concluído']

    # Calcula a média do tempo de conclusão para cotistas e não cotistas
    media_tempo_cotista = concluidos[concluidos['FORMA_INGRESSO_SIMPLES'] == 'Cotas']['TEMPO_CURSO'].mean()
    media_tempo_nao_cotista = concluidos[concluidos['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']['TEMPO_CURSO'].mean()

    # Exibe a diferença de forma visual
    print(Fore.CYAN + "Diferença de tempo de término entre Cotistas e Não Cotistas:")
    print(f"Cotistas: {media_tempo_cotista:.2f} períodos")
    print(f"Não Cotistas: {media_tempo_nao_cotista:.2f} períodos")
    print(Fore.YELLOW + f"Diferença: {abs(media_tempo_cotista - media_tempo_nao_cotista):.2f} períodos\n")


def exibir_porcentagem_concluidos_evasao_cursando(dataframe):
    # Calcula a porcentagem de alunos que concluíram, evadiram e estão cursando para cotistas e não cotistas
    total_cotistas = dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas'].shape[0]
    total_nao_cotistas = dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia'].shape[0]

    porcentagem_cotistas_concluidos = dataframe[(dataframe['STATUS_EVASAO'] == 'Concluído') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas')].shape[0] / total_cotistas * 100
    porcentagem_cotistas_evasao = dataframe[(dataframe['STATUS_EVASAO'] == 'Evasão') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas')].shape[0] / total_cotistas * 100
    porcentagem_cotistas_cursando = dataframe[(dataframe['STATUS_EVASAO'] == 'Cursando') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas')].shape[0] / total_cotistas * 100

    porcentagem_nao_cotistas_concluidos = dataframe[(dataframe['STATUS_EVASAO'] == 'Concluído') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia')].shape[0] / total_nao_cotistas * 100
    porcentagem_nao_cotistas_evasao = dataframe[(dataframe['STATUS_EVASAO'] == 'Evasão') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia')].shape[0] / total_nao_cotistas * 100
    porcentagem_nao_cotistas_cursando = dataframe[(dataframe['STATUS_EVASAO'] == 'Cursando') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia')].shape[0] / total_nao_cotistas * 100

    # Exibe os resultados
    print(Fore.MAGENTA + "Porcentagem de alunos Cotistas:")
    print(f"Concluídos: {porcentagem_cotistas_concluidos:.2f}%")
    print(f"Evasão: {porcentagem_cotistas_evasao:.2f}%")
    print(f"Cursando: {porcentagem_cotistas_cursando:.2f}%\n")

    print(Fore.MAGENTA + "Porcentagem de alunos Não Cotistas:")
    print(f"Concluídos: {porcentagem_nao_cotistas_concluidos:.2f}%")
    print(f"Evasão: {porcentagem_nao_cotistas_evasao:.2f}%")
    print(f"Cursando: {porcentagem_nao_cotistas_cursando:.2f}%\n")


def exibir_porcentagem_bairros_evasao_concluidos(dataframe):
    # Filtra os dados para alunos que concluíram e evadiram
    concluidos = dataframe[dataframe['STATUS_EVASAO'] == 'Concluído']
    evadidos = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']

    # Calcula a porcentagem dos 5 bairros com mais alunos concluídos e evadidos
    top_bairros_concluidos = calcular_porcentagem_ponderada(concluidos, 'Concluído')
    top_bairros_evasao = calcular_porcentagem_ponderada(evadidos, 'Evasão')

    # Exibe os resultados
    print(Fore.LIGHTBLUE_EX + "Top 5 Bairros com mais alunos Concluídos:")
    for bairro, porcentagem in top_bairros_concluidos.items():
        print(f"{bairro}: {porcentagem:.2f}%")

    print("\n" + Fore.LIGHTBLUE_EX + "Top 5 Bairros com mais alunos Evadidos:")
    for bairro, porcentagem in top_bairros_evasao.items():
        print(f"{bairro}: {porcentagem:.2f}%")


def calcular_porcentagem_ponderada(dataframe, status):
    bairros = dataframe['BAIRRO'].value_counts().index
    porcentagem_ponderada = {}

    for bairro in bairros:
        total_alunos_bairro = dataframe[dataframe['BAIRRO'] == bairro].shape[0]
        alunos_status = dataframe[(dataframe['BAIRRO'] == bairro) & (dataframe['STATUS_EVASAO'] == status)].shape[0]
        porcentagem = (alunos_status / total_alunos_bairro) * 100
        porcentagem_ponderada[bairro] = porcentagem * (total_alunos_bairro / len(dataframe))

    return pd.Series(porcentagem_ponderada).sort_values(ascending=False).head(5)


def plot_media_cra_evasao(dataframe):
    if 'STATUS_EVASAO' in dataframe.columns and 'CRA' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        media_cra = dataframe.groupby('STATUS_EVASAO')['CRA'].mean().reset_index()
        sns.barplot(x='STATUS_EVASAO', y='CRA', data=media_cra)
        plt.title('Média do CRA por Forma de Evasão')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Média do CRA')
        plt.xticks(rotation=45)
        plt.tight_layout()
        salvar_grafico('media_cra_evasao')
    else:
        print("A coluna 'STATUS_EVASAO' ou 'CRA' não existe no DataFrame.")


def plot_distribuicao_ingresso(dataframe):
    criar_grafico_de_contagem(x='FORMA_INGRESSO_SIMPLES', data=dataframe,
                              titulo='Distribuição de Cotistas e Não-Cotistas',
                              xlabel='Forma de Ingresso', ylabel='Quantidade')
    salvar_grafico('distribuicao_ingresso')


def plot_evasao_sexo(dataframe):
    plt.figure(figsize=(14, 6))

    # Gráfico para Cotistas
    plt.subplot(1, 2, 1)
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas'],
                              hue='SEXO', titulo='Distribuição de Evasões por Sexo (Cotistas)',
                              xlabel='Forma de Evasão', ylabel='Quantidade')

    # Gráfico para Não Cotistas
    plt.subplot(1, 2, 2)
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia'],
                              hue='SEXO', titulo='Distribuição de Evasões por Sexo (Não Cotistas)',
                              xlabel='Forma de Evasão', ylabel='Quantidade')

    plt.tight_layout()
    salvar_grafico('evasao_sexo')


def plot_evasao_idade(dataframe):
    plotar_histograma(x=dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']['IDADE_INGRESSO'], data=dataframe,
                      titulo='Distribuição de Idades dos Alunos com Evasão', xlabel='Idade', ylabel='Quantidade')
    salvar_grafico('evasao_idade')


def plot_evasao_ao_longo_do_tempo(dataframe):
    # Agrupa os dados por período de evasão e forma de ingresso
    evasao_por_periodo = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'FORMA_INGRESSO_SIMPLES']).size().unstack().fillna(0)

    # Plota a distribuição de evasão por período
    evasao_por_periodo.plot(kind='bar', stacked=True, figsize=(14, 6))
    plt.title('Distribuição de Evasão por Período')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Alunos Evadidos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('evasao_ao_longo_do_tempo')


def plot_evasao_por_periodo(df):
    """
    Função para plotar a distribuição de evasão por período do curso, diferenciando cotistas e não cotistas.
    """
    # Filtra os alunos que evadiram
    evadidos = df[df['STATUS_EVASAO'] == 'Evasão'].copy()

    # Calcula o período de evasão para cada aluno com base no tempo de curso
    evadidos.loc[:, 'PERIODO_EVASAO'] = (evadidos['TEMPO_CURSO'] * 2).round().astype(int)

    # Cria um histograma dos períodos de evasão com distinção entre cotistas e ampla concorrência
    plt.figure(figsize=(12, 7))
    sns.histplot(data=evadidos, x='PERIODO_EVASAO', hue='FORMA_INGRESSO_SIMPLES', multiple='stack', bins=range(1, 14),
                 palette='pastel', edgecolor='black')

    plt.title('Distribuição de Evasão por Período do Curso (Cotistas vs Ampla Concorrência)')
    plt.xlabel('Período do Curso')
    plt.ylabel('Número de Evasões')
    plt.xticks(range(1, 13))
    plt.tight_layout()
    salvar_grafico('evasao_por_periodo')


def analise_ingresso_evasao(dataframe):
    criar_pasta_graficos()
    print(Fore.BLUE + "\nIniciando Análise de Ingresso e Evasão...")

    exibir_diferenca_media_tempo_termino(dataframe)
    exibir_porcentagem_concluidos_evasao_cursando(dataframe)
    exibir_porcentagem_bairros_evasao_concluidos(dataframe)
    plot_evasao_temporal_sexo(dataframe)

    # Adicionando as análises de sexo e idade
    plot_distribuicao_sexo(dataframe)
    plot_distribuicao_idade(dataframe)

    plot_media_cra_evasao(dataframe)
    plot_distribuicao_ingresso(dataframe)
    plot_evasao_sexo(dataframe)
    plot_evasao_idade(dataframe)
    plot_evasao_ao_longo_do_tempo(dataframe)
    plot_evasao_por_periodo(dataframe)

    print(Fore.GREEN + "\nAnálise de Ingresso e Evasão Concluída!")


def plot_distribuicao_sexo(dataframe):
    """
    Função para plotar a distribuição de sexo dos alunos, separados por cotistas e não cotistas.
    """
    plt.figure(figsize=(14, 6))
    sns.countplot(x='SEXO', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel')
    plt.title('Distribuição de Sexo por Forma de Ingresso')
    plt.xlabel('Sexo')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    salvar_grafico('distribuicao_sexo')


def plot_distribuicao_idade(dataframe):
    """
    Função para plotar a distribuição de idades no ingresso, separando cotistas e não cotistas.
    """
    plt.figure(figsize=(14, 6))
    sns.histplot(data=dataframe, x='IDADE_INGRESSO', hue='FORMA_INGRESSO_SIMPLES', multiple='stack', palette='pastel')
    plt.title('Distribuição de Idades no Ingresso por Forma de Ingresso')
    plt.xlabel('Idade no Ingresso')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    salvar_grafico('distribuicao_idade')


def plot_evasao_temporal_sexo(dataframe):
    """
    Função para plotar a taxa de evasão ao longo do tempo, diferenciando por sexo.
    """
    evasao_temporal = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'SEXO']).size().unstack().fillna(0)

    plt.figure(figsize=(14, 6))
    evasao_temporal.plot(kind='line', ax=plt.gca(), marker='o')
    plt.title('Evasão ao Longo do Tempo por Sexo')
    plt.xlabel('Período de Evasão')
    plt.ylabel('Número de Evasões')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('evasao_temporal_sexo')


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df)
