import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, init
from src.utils.plots import salvar_grafico, criar_grafico_de_contagem, adicionar_valores_barras, ajustar_estilos_grafico
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
    plot_evasao_por_periodo(df_periodo, nome_pasta, periodo_nome, 1, 20)
    plot_distribuicao_temporal_sexo(df_periodo, nome_pasta, periodo_nome)

    print(Fore.GREEN + f"\nAnálise de Ingresso e Evasão Concluída para o período: {periodo_nome}")


def plot_media_cra_evasao(dataframe, nome_pasta, periodo_nome):
    if 'STATUS_EVASAO' in dataframe.columns and 'CRA' in dataframe.columns:
        fig, ax = plt.subplots(figsize=(10, 6))

        # Agrupa por status de evasão e forma de ingresso, calculando a média de CRA
        media_cra = dataframe.groupby(['STATUS_EVASAO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()
        sns.barplot(x='STATUS_EVASAO', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=media_cra, palette='pastel', ax=ax)

        # Adicionar valores em cima das barras
        adicionar_valores_barras(ax)

        # Ajustar o estilo do gráfico
        ajustar_estilos_grafico(ax, title=f'Média do CRA por Forma de Evasão', xlabel='Forma de Evasão', ylabel='Média do CRA')

        salvar_grafico(f'media_cra_evasao_{periodo_nome}', nome_pasta)
    else:
        print(Fore.RED + "A coluna 'STATUS_EVASAO' ou 'CRA' não existe no DataFrame.")


def plot_distribuicao_ingresso(dataframe, nome_pasta, periodo_nome):
    fig, ax = plt.subplots(figsize=(10, 6))

    total_alunos = len(dataframe)
    contagem_alunos = dataframe['FORMA_INGRESSO_SIMPLES'].value_counts().reset_index()
    contagem_alunos.columns = ['FORMA_INGRESSO_SIMPLES', 'QUANTIDADE']
    contagem_alunos['PERCENTUAL'] = (contagem_alunos['QUANTIDADE'] / total_alunos) * 100

    sns.barplot(x='FORMA_INGRESSO_SIMPLES', y='PERCENTUAL', data=contagem_alunos, palette='pastel', ax=ax)

    # Adiciona os valores de percentual em cima das barras
    adicionar_valores_barras(ax)

    ajustar_estilos_grafico(ax, title=f'Distribuição de Cotistas e Não-Cotistas', xlabel='Forma de Ingresso', ylabel='Porcentagem de Alunos (%)')

    salvar_grafico(f'distribuicao_ingresso_{periodo_nome}', nome_pasta)


def plot_evasao_detalhada(dataframe, nome_pasta, periodo_nome):
    evasao_filtrada = dataframe[~dataframe['FORMA_EVASAO_DETALHADA'].isin(['CON - Curso concluído', 'Sem evasão'])]
    total_evasao = len(evasao_filtrada)
    evasao_agrupada = evasao_filtrada.groupby(['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='contagem')
    evasao_agrupada['percentual'] = (evasao_agrupada['contagem'] / total_evasao) * 100
    evasao_agrupada['FORMA_EVASAO_DETALHADA'] = evasao_agrupada['FORMA_EVASAO_DETALHADA'].apply(lambda x: x.split()[0])

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='FORMA_EVASAO_DETALHADA', y='percentual', hue='FORMA_INGRESSO_SIMPLES', data=evasao_agrupada, palette='pastel')

    adicionar_valores_barras(ax)
    ajustar_estilos_grafico(ax, title=f'Evasão por Tipo e Forma de Ingresso', xlabel='Tipo de Evasão', ylabel='Porcentagem de Alunos (%)')

    # Ajustar a legenda para aparecer com o texto logo abaixo
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))

    # Texto explicativo abaixo da legenda principal
    plt.text(1.02, 0.6, "ABA = Abandono do Curso \nCAN = Cancelamento \nJUB = Jubilamento", ha="left", fontsize=17, transform=ax.transAxes)

    plt.tight_layout()
    salvar_grafico(f'evasao_detalhada_{periodo_nome}', nome_pasta)


def plot_evasao_sexo(dataframe, nome_pasta, periodo_nome):
    """
    Plota a distribuição de evasão por sexo, separada por cotistas e ampla concorrência.
    """
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico para cotistas
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotas'],
                              hue='SEXO', titulo=f'Evasão por Sexo (Cotistas)', xlabel='Forma de Evasão', ylabel='Quantidade', ax=axs[0])

    # Gráfico para não-cotistas
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia'],
                              hue='SEXO', titulo=f'Evasão por Sexo (Não Cotistas)', xlabel='Forma de Evasão', ylabel='Quantidade', ax=axs[1])

    plt.tight_layout()
    salvar_grafico(f'evasao_sexo_{periodo_nome}', nome_pasta)


def plot_evasao_idade(dataframe, nome_pasta, periodo_nome):
    """
    Ajusta o gráfico de evasão por idade, aplicando a porcentagem corretamente e removendo valores inválidos.
    """
    # Filtra apenas alunos que evadiram e que têm idade válida no momento da evasão
    evasao_filtrada = dataframe[(dataframe['STATUS_EVASAO'] == 'Evasão') & dataframe['IDADE_EVASAO'].notnull()]

    # Excluir grupos como 'Ampla Concorrência' ou qualquer outro, dependendo da coluna certa para filtrar
    evasao_filtrada = evasao_filtrada[evasao_filtrada['FORMA_INGRESSO_SIMPLES'] != 'Ampla Concorrencia']

    # Agrupar os dados pela idade no momento da evasão e calcular a contagem
    evasao_agrupada = evasao_filtrada.groupby('IDADE_EVASAO').size().reset_index(name='contagem')

    # Verifica se há algum dado para plotar
    if evasao_agrupada.empty:
        print(Fore.RED + "Nenhum dado de evasão para plotar.")
        return

    # Calcula a porcentagem em relação ao total
    total_evasao = len(evasao_filtrada)
    evasao_agrupada['percentual'] = (evasao_agrupada['contagem'] / total_evasao) * 100

    # Plotar o gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='IDADE_EVASAO', y='percentual', data=evasao_agrupada, palette='pastel', ax=ax)

    # Adicionar valores em cima das barras
    adicionar_valores_barras(ax)

    # Ajustar o estilo do gráfico
    ajustar_estilos_grafico(ax, title=f'Distribuição de Idades dos Alunos na Evasão',
                            xlabel='Idade no Momento da Evasão', ylabel='Porcentagem de Alunos (%)')

    salvar_grafico(f'evasao_idade_{periodo_nome}', nome_pasta)


def plot_evasao_por_periodo(df, nome_pasta, periodo_nome, periodo_inicio, periodo_fim):
    """
    Plota a distribuição de evasão por período do curso, separada por cotistas e ampla concorrência.
    """
    evadidos = df[(df['STATUS_EVASAO'] == 'Evasão') & (df['PERIODO_EVASAO'] >= periodo_inicio) & (df['PERIODO_EVASAO'] <= periodo_fim)].copy()
    evadidos['PERIODO_EVASAO'] = (evadidos['TEMPO_CURSO'] * 2).round().astype(int)

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.histplot(data=evadidos, x='PERIODO_EVASAO', hue='FORMA_INGRESSO_SIMPLES', multiple='stack', bins=range(1, 20),
                 palette='pastel', edgecolor='black', ax=ax)

    ajustar_estilos_grafico(ax, title=f'Evasão por Período do Curso', xlabel='Período do Curso', ylabel='Número de Evasões')

    salvar_grafico(f'evasao_por_periodo_{periodo_nome}', nome_pasta)


def plot_distribuicao_temporal_sexo(dataframe, nome_pasta, periodo_nome):
    """
    Plota a evasão ao longo do tempo separada por sexo.
    """
    evasao_temporal = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão'].groupby(['PERIODO_EVASAO_FORMATADO', 'SEXO']).size().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(14, 6))
    evasao_temporal.plot(kind='line', ax=ax, marker='o')

    ajustar_estilos_grafico(ax, title=f'Evasão ao Longo do Tempo por Sexo', xlabel='Período de Evasão', ylabel='Número de Evasões')

    salvar_grafico(f'evasao_temporal_sexo_{periodo_nome}', nome_pasta)


def plot_distribuicao_idade_por_sexo(dataframe, nome_pasta, periodo_nome):
    """
    Plota a distribuição da idade no ingresso por sexo.
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(x='SEXO', y='IDADE_INGRESSO', data=dataframe, palette='pastel', ax=ax)

    ajustar_estilos_grafico(ax, title=f'Distribuição da Idade no Ingresso por Sexo', xlabel='Sexo', ylabel='Idade no Ingresso')

    salvar_grafico(f'distribuicao_idade_por_sexo_{periodo_nome}', nome_pasta)


def plot_tempo_curso_por_forma_evasao(dataframe, nome_pasta, periodo_nome):
    """
    Plota a distribuição do tempo de curso por forma de evasão.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='FORMA_EVASAO', y='TEMPO_CURSO', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='pastel', ax=ax)

    ajustar_estilos_grafico(ax, title=f'Distribuição do Tempo de Curso por Forma de Evasão', xlabel='Forma de Evasão', ylabel='Tempo de Curso (Períodos)')

    plt.xticks(rotation=45)
    salvar_grafico(f'tempo_curso_por_forma_evasao_{periodo_nome}', nome_pasta)


def plot_evasao_por_cra_arredondado(dataframe, nome_pasta, periodo_nome):
    """
    Plota a distribuição da evasão por níveis de CRA arredondados.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='CRA_ARREDONDADO', hue='STATUS_EVASAO', data=dataframe, palette='pastel', ax=ax)

    adicionar_valores_barras(ax)
    ajustar_estilos_grafico(ax, title=f'Distribuição de Evasão por Nível de CRA Arredondado', xlabel='CRA Arredondado', ylabel='Quantidade de Alunos')

    salvar_grafico(f'evasao_por_cra_arredondado_{periodo_nome}', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df, "resultados_ingresso_evasao", "2023")
