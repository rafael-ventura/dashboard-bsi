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
    plot_evasao_por_cra_arredondado(df_periodo, nome_pasta, periodo_nome)

    print(Fore.GREEN + f"\nAnálise de Ingresso e Evasão Concluída para o período: {periodo_nome}")


# Funções de plotagem com prints informativos

def plot_media_cra_evasao(dataframe, nome_pasta, periodo_nome):
    print(Fore.YELLOW + "Plotando Média do CRA por Forma de Evasão...")
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
    """
    Plota a distribuição dos alunos por forma de ingresso, mostrando valores absolutos nas barras.
    """
    print(Fore.YELLOW + "Plotando Distribuição de Cotistas e Não-Cotistas...")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calcula a contagem absoluta dos alunos por forma de ingresso
    contagem_alunos = dataframe['FORMA_INGRESSO_SIMPLES'].value_counts().reset_index()
    contagem_alunos.columns = ['FORMA_INGRESSO_SIMPLES', 'QUANTIDADE']

    # Plota a distribuição com os valores absolutos
    sns.barplot(x='FORMA_INGRESSO_SIMPLES', y='QUANTIDADE', data=contagem_alunos, palette='pastel', ax=ax)

    # Adiciona valores absolutos nas barras
    for p in ax.patches:
        height = int(p.get_height())  # Pega o valor absoluto (quantidade de alunos)
        ax.annotate(f'{height}',
                    (p.get_x() + p.get_width() / 2., height),  # Localização do texto
                    ha='center', va='center', xytext=(0, 10),  # Ajuste de posicionamento
                    textcoords='offset points', fontsize=14)  # Tamanho da fonte

    ajustar_estilos_grafico(ax, title=f'Distribuição dos Alunos por Forma de Ingresso',
                            xlabel='Forma de Ingresso', ylabel='Quantidade de Alunos')

    salvar_grafico(f'distribuicao_ingresso_{periodo_nome}', nome_pasta)


def plot_evasao_detalhada(dataframe, nome_pasta, periodo_nome):
    print(Fore.YELLOW + "Plotando Evasão Detalhada...")
    total_original = len(dataframe)
    evasao_filtrada = dataframe[~dataframe['FORMA_EVASAO_DETALHADA'].isin(['CON - Curso concluído', 'Sem evasão'])]
    total_evasao = len(evasao_filtrada)
    registros_descartados = total_original - total_evasao

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.BLUE + f"Total de registros descartados: {registros_descartados}")
    print(Fore.BLUE + f"Total de registros após o filtro: {total_evasao}")

    evasao_agrupada = evasao_filtrada.groupby(['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='contagem')
    evasao_agrupada['percentual'] = (evasao_agrupada['contagem'] / total_evasao) * 100
    evasao_agrupada['FORMA_EVASAO_DETALHADA'] = evasao_agrupada['FORMA_EVASAO_DETALHADA'].apply(lambda x: x.split()[0])

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='FORMA_EVASAO_DETALHADA', y='percentual', hue='FORMA_INGRESSO_SIMPLES', data=evasao_agrupada, palette='pastel')

    adicionar_valores_barras(ax, exibir_percentual=False, fontsize=14)
    ajustar_estilos_grafico(ax, title=f'Evasão Detalhada', xlabel='Tipo de Evasão', ylabel='Porcentagem de Alunos (%)')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))

    plt.text(1.02, 0.6, "ABA = Abandono do Curso \nCAN = Cancelamento \nJUB = Jubilamento \nDES = Desistencia", ha="left", fontsize=17, transform=ax.transAxes)

    plt.tight_layout()
    salvar_grafico(f'evasao_detalhada_{periodo_nome}', nome_pasta)


def plot_evasao_sexo(dataframe, nome_pasta, periodo_nome):
    print(Fore.YELLOW + "Plotando Evasão por Sexo...")
    # Filtra apenas os alunos que evadiram
    total_original = len(dataframe)
    evadidos = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']
    total_filtrado = len(evadidos)
    registros_descartados = total_original - total_filtrado

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.BLUE + f"Total de registros descartados: {registros_descartados}")
    print(Fore.BLUE + f"Total de registros após o filtro: {total_filtrado}")

    # Filtra cotistas e não cotistas
    cotistas = evadidos[evadidos['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = evadidos[evadidos['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    # Criar uma figura com o número correto de subplots
    if not cotistas.empty and not nao_cotistas.empty:
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    else:
        fig, axs = plt.subplots(1, 1, figsize=(7, 6))

    # Plot para cotistas se houver
    if not cotistas.empty:
        total_cotistas = len(cotistas)
        cotistas_contagem = cotistas.groupby('SEXO').size().reset_index(name='contagem')
        cotistas_contagem['percentual'] = (cotistas_contagem['contagem'] / total_cotistas) * 100

        if not nao_cotistas.empty:
            ax_cotistas = axs[0]
        else:
            ax_cotistas = axs  # Se houver só cotistas, usar o único subplot

        sns.barplot(x='SEXO', y='percentual', data=cotistas_contagem, palette='pastel', ax=ax_cotistas)
        ax_cotistas.set_title(f'Evasão por Sexo (Cotistas)')
        ax_cotistas.set_xlabel('Sexo')
        ax_cotistas.set_ylabel('Porcentagem de Alunos (%)')

        adicionar_valores_barras(ax_cotistas, exibir_percentual=True, total=100, fontsize=14)

    # Plot para não-cotistas se houver
    if not nao_cotistas.empty:
        total_nao_cotistas = len(nao_cotistas)
        nao_cotistas_contagem = nao_cotistas.groupby('SEXO').size().reset_index(name='contagem')
        nao_cotistas_contagem['percentual'] = (nao_cotistas_contagem['contagem'] / total_nao_cotistas) * 100

        if not cotistas.empty:
            ax_nao_cotistas = axs[1]
        else:
            ax_nao_cotistas = axs  # Se houver só não cotistas, usar o único subplot

        sns.barplot(x='SEXO', y='percentual', data=nao_cotistas_contagem, palette='pastel', ax=ax_nao_cotistas)
        ax_nao_cotistas.set_title(f'Evasão por Sexo (Não Cotistas)')
        ax_nao_cotistas.set_xlabel('Sexo')
        ax_nao_cotistas.set_ylabel('Porcentagem de Alunos (%)')

        adicionar_valores_barras(ax_nao_cotistas, exibir_percentual=True, total=100, fontsize=14)

    plt.tight_layout()
    salvar_grafico(f'evasao_sexo_{periodo_nome}', nome_pasta)


def plot_evasao_idade(dataframe, nome_pasta, periodo_nome):
    """
    Ajusta o gráfico de evasão por idade, aplicando a porcentagem corretamente e removendo valores inválidos.
    """
    print(Fore.YELLOW + "Plotando Evasão por Idade...")
    total_original = len(dataframe)

    # Filtra apenas alunos que evadiram e que têm idade válida no momento da evasão
    evasao_filtrada = dataframe[(dataframe['STATUS_EVASAO'] == 'Evasão') & dataframe['IDADE_EVASAO'].notnull()]
    total_filtrado = len(evasao_filtrada)
    registros_descartados = total_original - total_filtrado

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.BLUE + f"Total de registros descartados: {registros_descartados}")
    print(Fore.BLUE + f"Total de registros após o filtro: {total_filtrado}")

    # Converter a coluna 'IDADE_EVASAO' para inteiros
    evasao_filtrada['IDADE_EVASAO'] = evasao_filtrada['IDADE_EVASAO'].astype(int)

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
    adicionar_valores_barras(ax, exibir_percentual=True, total=100, fontsize=10)

    # Ajustar o estilo do gráfico
    ajustar_estilos_grafico(ax, title=f'Distribuição de Idades dos Alunos na Evasão',
                            xlabel='Idade no Momento da Evasão', ylabel='Porcentagem de Alunos (%)')

    # Salvar o gráfico
    salvar_grafico(f'evasao_idade_{periodo_nome}', nome_pasta)


def plot_evasao_por_periodo(df, nome_pasta, periodo_nome, periodo_inicio, periodo_fim):
    """
    Plota a distribuição de evasão por período do curso, separada por cotistas e ampla concorrência.
    """
    print(Fore.YELLOW + "Plotando Evasão por Período do Curso...")
    total_original = len(df)

    evadidos = df[(df['STATUS_EVASAO'] == 'Evasão') & (df['PERIODO_EVASAO'] >= periodo_inicio) & (df['PERIODO_EVASAO'] <= periodo_fim)].copy()
    total_filtrado = len(evadidos)
    registros_descartados = total_original - total_filtrado

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.BLUE + f"Total de registros descartados: {registros_descartados}")
    print(Fore.BLUE + f"Total de registros após o filtro: {total_filtrado}")

    evadidos['PERIODO_EVASAO'] = (evadidos['TEMPO_CURSO'] * 2).round().astype(int)

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.histplot(data=evadidos, x='PERIODO_EVASAO', hue='FORMA_INGRESSO_SIMPLES', multiple='stack', bins=range(1, 20),
                 palette='pastel', edgecolor='black', ax=ax)

    # Ajustar os ticks do eixo x para mostrar de 1 em 1
    ax.set_xticks(range(1, 20))
    ax.set_xticklabels(range(1, 20))

    ajustar_estilos_grafico(ax, title=f'Evasão por Período do Curso', xlabel='Período do Curso', ylabel='Número de Evasões')

    # Salvar o gráfico
    salvar_grafico(f'evasao_por_periodo_{periodo_nome}', nome_pasta)


def plot_evasao_por_cra_arredondado(dataframe, nome_pasta, periodo_nome):
    """
    Plota a distribuição da evasão por níveis de CRA arredondados e adiciona manualmente os valores nas barras.
    """
    print(Fore.YELLOW + "Plotando Evasão por Nível de CRA Arredondado...")
    total_original = len(dataframe)

    dataframe_filtrado = dataframe[dataframe['CRA_ARREDONDADO'].notnull()]
    total_filtrado = len(dataframe_filtrado)
    registros_descartados = total_original - total_filtrado

    print(Fore.BLUE + f"Total de registros antes do filtro: {total_original}")
    print(Fore.BLUE + f"Total de registros descartados: {registros_descartados}")
    print(Fore.BLUE + f"Total de registros após o filtro: {total_filtrado}")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='CRA_ARREDONDADO', hue='STATUS_EVASAO', data=dataframe_filtrado, palette='pastel', ax=ax)

    # Adicionando valores manualmente nas barras
    for p in ax.patches:
        height = int(p.get_height())  # Pegando o valor da altura da barra (quantidade de alunos)
        ax.annotate(f'{height}',
                    (p.get_x() + p.get_width() / 2., height),  # Localização do texto
                    ha='center', va='center', xytext=(0, 10),  # Ajustes de posicionamento do texto
                    textcoords='offset points', fontsize=8)  # Tamanho da fonte

    ajustar_estilos_grafico(ax, title=f'Distribuição de Evasão por Nível de CRA Arredondado',
                            xlabel='CRA Arredondado', ylabel='Quantidade de Alunos')

    salvar_grafico(f'evasao_por_cra_arredondado_{periodo_nome}', nome_pasta)


if __name__ == '__main__':
    # Carregar os dados
    df = carregar_dados('dados/dados_limpos.csv')

    # Análise de Ingresso e Evasão
    analise_ingresso_evasao(df, 'resultados', 'geral')
