import geopandas as gpd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.utils.plots import criar_pasta_graficos, salvar_grafico, plot_treemap
from src.utils.utils import carregar_dados, remover_acentos_e_maiusculas, separar_por_periodo, pega_caminho_base
from colorama import Fore, Style, init

# Inicializa o Colorama
init(autoreset=True)


def analise_geografica(df_periodo, nome_pasta, periodo_nome):
    print(Fore.BLUE + f"\nIniciando Análise Geográfica para o período: {periodo_nome}")

    bairros_rj = carregar_bairros_rj()
    bairros_rj = consolidar_ilha_do_governador(bairros_rj)
    bairros_rj = preparar_dados_bairros(df_periodo, bairros_rj)

    # Executar as análises geográficas para cada período
    plot_mapa_calor_comparativo(bairros_rj, df_periodo, nome_pasta, periodo_nome)
    plot_treemap_comparativo_bairros(df_periodo, nome_pasta, periodo_nome)
    #plot_cra_por_distancia(df_periodo, nome_pasta, periodo_nome)
    plot_cra_por_bairro(df_periodo, nome_pasta, periodo_nome)
    plot_cra_por_zona(df_periodo, nome_pasta, periodo_nome)
    plot_cra_evasao(df_periodo, nome_pasta, periodo_nome)
    plot_quantidade_alunos_por_zona(df_periodo, nome_pasta, periodo_nome)

    print(Fore.GREEN + f"\nAnálise Geográfica Concluída para o período: {periodo_nome}")


def preparar_dados_bairros(df, bairros_rj):
    """
    Prepara os dados de bairros para plotagem, lidando com casos de bairros desconhecidos ou vazios.
    """
    # Remover bairros "Desconhecido"
    df = df[df['BAIRRO'] != 'Desconhecido']

    # Garantir que todos os bairros estejam em minúsculas e sem acentos para o merge
    df['BAIRRO'] = df['BAIRRO'].apply(remover_acentos_e_maiusculas)
    bairros_rj['nome'] = bairros_rj['nome'].apply(remover_acentos_e_maiusculas)

    # Contagem de alunos por bairro
    contagem_alunos = df['BAIRRO'].value_counts().reset_index()
    contagem_alunos.columns = ['nome', 'ALUNOS']

    # Realizar o merge entre os bairros e as contagens de alunos
    bairros_rj = bairros_rj.merge(contagem_alunos, on='nome', how='left')

    # Preencher NaNs com 0 no caso de não haver alunos em determinados bairros
    if 'ALUNOS' not in bairros_rj.columns:
        bairros_rj['ALUNOS'] = 0
    else:
        bairros_rj['ALUNOS'] = bairros_rj['ALUNOS'].fillna(0).astype(int)

    return bairros_rj


def consolidar_ilha_do_governador(bairros_rj):
    ilha = bairros_rj[bairros_rj['regiao_adm'].str.contains('ILHA DO GOVERNADOR', na=False)]
    ilha_consolidada = ilha.dissolve(by='regiao_adm')
    ilha_consolidada['nome'] = 'ILHA DO GOVERNADOR'

    bairros_rj = bairros_rj[~bairros_rj['regiao_adm'].str.contains('ILHA DO GOVERNADOR', na=False)]
    bairros_rj = pd.concat([bairros_rj, ilha_consolidada])

    return bairros_rj


def carregar_bairros_rj():
    bairros_rj = gpd.read_file(pega_caminho_base() + '/dados/Limite_de_Bairros.geojson')
    return bairros_rj


def plot_mapa_calor_comparativo(bairros_rj, df, nome_pasta, periodo_nome):
    fig, axs = plt.subplots(1, 2, figsize=(30, 15))

    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    bairros_rj_cotistas = preparar_dados_bairros(cotistas, bairros_rj.copy())
    bairros_rj_nao_cotistas = preparar_dados_bairros(nao_cotistas, bairros_rj.copy())

    cmap = colors.ListedColormap(sns.color_palette("Blues", 12))
    norm = colors.BoundaryNorm(boundaries=[0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50], ncolors=12)

    # Plot para cotistas
    bairros_rj_cotistas.plot(column='ALUNOS', ax=axs[0], legend=True, cmap=cmap, norm=norm, edgecolor='black', missing_kwds={"color": "lightgrey"})
    axs[0].set_title(f'Densidade de Alunos Cotistas por Bairro - {periodo_nome}')
    axs[0].axis('off')

    # Plot para não cotistas
    if not bairros_rj_nao_cotistas.empty:
        bairros_rj_nao_cotistas.plot(column='ALUNOS', ax=axs[1], legend=True, cmap=cmap, norm=norm, edgecolor='black', missing_kwds={"color": "lightgrey"})
        axs[1].set_title(f'Densidade de Alunos Ampla Concorrência por Bairro - {periodo_nome}')
        axs[1].axis('off')
    else:
        axs[1].set_title(f'Sem dados de Ampla Concorrência - {periodo_nome}')
        axs[1].axis('off')

    salvar_grafico(f'mapa_calor_comparativo_{periodo_nome}', nome_pasta)


def plot_treemap_comparativo_bairros(df, nome_pasta, periodo_nome):
    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    cotistas_count = cotistas['BAIRRO'].value_counts().nlargest(20)
    nao_cotistas_count = nao_cotistas['BAIRRO'].value_counts().nlargest(20)

    # Definindo um threshold mínimo para o treemap, por exemplo, 1
    threshold = 1

    plot_treemap(cotistas_count, threshold, f'Treemap dos 20 Bairros com mais Alunos Cotistas - {periodo_nome}', 'Spectral', nome_pasta, show_values=True)
    plot_treemap(nao_cotistas_count, threshold, f'Treemap dos 20 Bairros com mais Alunos Ampla Concorrência - {periodo_nome}', 'Spectral', nome_pasta, show_values=True)


# def plot_cra_por_distancia(df, nome_pasta, periodo_nome):
#     plt.figure(figsize=(10, 6))
#
#     # Contagem de alunos (ou seja, número de registros por distância)
#     df_agrupado = df.groupby('DISTANCIA_URCA').agg({'CRA': 'mean', 'DISTANCIA_URCA': 'size'}).reset_index()
#     df_agrupado.columns = ['DISTANCIA_URCA', 'CRA_MEDIO', 'ALUNOS']
#
#     # Plotando a linha da média ponderada (média simples nesse caso, já que cada linha é um aluno)
#     sns.lineplot(x='DISTANCIA_URCA', y='CRA_MEDIO', data=df_agrupado[df_agrupado['DISTANCIA_URCA'] <= 40])
#
#     plt.title(f'Relação entre Distância até a Urca e CRA - {periodo_nome} (Média até 40 km)')
#     plt.xlabel('Distância até a Urca (km)')
#     plt.ylabel('CRA Médio')
#     plt.tight_layout()
#     salvar_grafico(f'cra_por_distancia_{periodo_nome}', nome_pasta)


def plot_cra_por_bairro(df, nome_pasta, periodo_nome):
    # Filtrar apenas os bairros com pelo menos 4 alunos
    bairros_filtrados = df.groupby('BAIRRO').filter(lambda x: len(x) >= 4)

    # Calcular a média do CRA por bairro
    cra_bairro = bairros_filtrados.groupby('BAIRRO')['CRA'].mean().reset_index()

    # Ordenando a média do CRA em ordem crescente
    cra_bairro = cra_bairro.sort_values(by='CRA')

    # Ajustar o tamanho da figura dinamicamente com base na quantidade de bairros
    plt.figure(figsize=(14, max(6, int(len(cra_bairro) / 3))))  # Converte o valor da divisão para inteiro
    sns.barplot(x='CRA', y='BAIRRO', data=cra_bairro, palette='muted')
    plt.title(f'Média do CRA por Bairro - {periodo_nome} (Com pelo menos 4 alunos)')
    plt.xlabel('CRA')
    plt.ylabel('Bairro')
    plt.tight_layout()
    salvar_grafico(f'cra_por_bairro_filtrado_{periodo_nome}', nome_pasta)


def plot_cra_por_zona(df, nome_pasta, periodo_nome):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']

    # Filtrando apenas as zonas de interesse
    df_foco = df[df['ZONA'].isin(zonas_foco)]

    media_cra_zona = df_foco.groupby('ZONA')['CRA'].mean().reset_index()

    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='ZONA', y='CRA', data=media_cra_zona, palette='muted')

    # Adicionando os valores exatos do CRA em cima de cada barra
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    plt.title(f'Média do CRA por Zona - {periodo_nome} (Zonas Selecionadas)')
    plt.xlabel('Zona')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=90)
    plt.tight_layout()
    salvar_grafico(f'cra_por_zona_{periodo_nome}', nome_pasta)


def plot_cra_evasao(df, nome_pasta, periodo_nome):
    plt.figure(figsize=(10, 6))
    cra_evasao = df.groupby('STATUS_EVASAO')['CRA'].mean().reset_index()
    ax = sns.barplot(x='STATUS_EVASAO', y='CRA', data=cra_evasao, palette='pastel')

    # Adicionando os valores exatos em cima das barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    plt.title(f'Média do CRA por Status de Evasão - {periodo_nome}')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'cra_evasao_{periodo_nome}', nome_pasta)


def plot_quantidade_alunos_por_zona(df, nome_pasta, periodo_nome):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']

    df_foco = df[df['ZONA'].isin(zonas_foco)]
    contagem_alunos_zona = df_foco.groupby(['ZONA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='QUANTIDADE')

    total_alunos = contagem_alunos_zona['QUANTIDADE'].sum()
    contagem_alunos_zona['PERCENTUAL'] = (contagem_alunos_zona['QUANTIDADE'] / total_alunos) * 100

    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='ZONA', y='PERCENTUAL', hue='FORMA_INGRESSO_SIMPLES', data=contagem_alunos_zona, palette='muted')

    # Adicionando o valor percentual em cima das barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    plt.title(f'Quantidade de Alunos por Zona - {periodo_nome} e Forma de Ingresso (Zonas Selecionadas)')
    plt.xlabel('Zona')
    plt.ylabel('Percentual de Alunos (%)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    salvar_grafico(f'quantidade_alunos_por_zona_percentual_{periodo_nome}', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_geografica(df, "resultados", "2023")
