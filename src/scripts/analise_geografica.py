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


def analise_geografica(df_periodo, nome_pasta):
    print(Fore.BLUE + "\nIniciando Análise Geográfica...")

    bairros_rj = carregar_bairros_rj()
    bairros_rj = consolidar_ilha_do_governador(bairros_rj)
    bairros_rj = preparar_dados_bairros(df_periodo, bairros_rj)

    # Executar as análises geográficas para cada período
    plot_mapa_calor_comparativo(bairros_rj, df_periodo, nome_pasta, 'geografico')
    plot_treemap_comparativo_bairros(df_periodo, nome_pasta)
    plot_cra_por_distancia(df_periodo, nome_pasta)
    plot_cra_por_bairro(df_periodo, nome_pasta)
    plot_cra_por_zona(df_periodo, nome_pasta)
    plot_cra_evasao(df_periodo, nome_pasta)
    plot_quantidade_alunos_por_zona(df_periodo, nome_pasta)

    print(Fore.GREEN + "\nAnálise Geográfica Concluída com Sucesso!")


def preparar_dados_bairros(df, bairros_rj):
    """
    Prepara os dados de bairros para plotagem, lidando com casos de bairros desconhecidos ou vazios.
    """
    # Preencher bairros vazios ou desconhecidos com uma string específica para evitar problemas no merge
    df['BAIRRO'] = df['BAIRRO'].fillna('Desconhecido').apply(remover_acentos_e_maiusculas)

    # Garantir que todos os bairros estejam em minúsculas e sem acentos para o merge
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


def plot_mapa_calor_comparativo(bairros_rj, df, nome_pasta, periodo):
    fig, axs = plt.subplots(1, 2, figsize=(30, 15))

    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    bairros_rj_cotistas = preparar_dados_bairros(cotistas, bairros_rj.copy())
    bairros_rj_nao_cotistas = preparar_dados_bairros(nao_cotistas, bairros_rj.copy())

    cmap = colors.ListedColormap(sns.color_palette("Blues", 12))
    norm = colors.BoundaryNorm(boundaries=[0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50], ncolors=12)

    # Plot para cotistas
    bairros_rj_cotistas.plot(column='ALUNOS', ax=axs[0], legend=True, cmap=cmap, norm=norm, edgecolor='black', missing_kwds={"color": "lightgrey"})
    axs[0].set_title(f'Densidade de Alunos Cotistas por Bairro - {periodo}')
    axs[0].axis('off')

    # Plot para não cotistas
    if not bairros_rj_nao_cotistas.empty:
        bairros_rj_nao_cotistas.plot(column='ALUNOS', ax=axs[1], legend=True, cmap=cmap, norm=norm, edgecolor='black', missing_kwds={"color": "lightgrey"})
        axs[1].set_title(f'Densidade de Alunos Ampla Concorrência por Bairro - {periodo}')
        axs[1].axis('off')
    else:
        axs[1].set_title(f'Sem dados de Ampla Concorrência - {periodo}')
        axs[1].axis('off')

    salvar_grafico(f'mapa_calor_comparativo_{periodo}', nome_pasta)


def plot_treemap_comparativo_bairros(df, nome_pasta):
    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    cotistas_count = cotistas['BAIRRO'].value_counts().nlargest(20)
    nao_cotistas_count = nao_cotistas['BAIRRO'].value_counts().nlargest(20)

    # Definindo um threshold mínimo para o treemap, por exemplo, 1
    threshold = 1

    plot_treemap(cotistas_count, threshold, 'Treemap dos 20 Bairros com mais Alunos Cotistas', 'Spectral', nome_pasta)
    plot_treemap(nao_cotistas_count, threshold, 'Treemap dos 20 Bairros com mais Alunos Ampla Concorrência', 'Spectral', nome_pasta)


def plot_cra_por_distancia(df, nome_pasta):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='DISTANCIA_URCA', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=df[df['DISTANCIA_URCA'] <= 40])

    plt.title('Relação entre Distância até a Urca e CRA (até 40 km)')
    plt.xlabel('Distância até a Urca (km)')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('cra_por_distancia_40km', nome_pasta)


def plot_cra_por_bairro(df, nome_pasta):
    cra_bairro = df.groupby('BAIRRO')['CRA'].mean().reset_index()

    plt.figure(figsize=(14, 8))
    sns.barplot(x='CRA', y='BAIRRO', data=cra_bairro, palette='muted')
    plt.title('Média do CRA por Bairro')
    plt.xlabel('CRA')
    plt.ylabel('Bairro')
    plt.tight_layout()
    salvar_grafico('cra_por_bairro', nome_pasta)


def plot_cra_por_zona(df, nome_pasta):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']

    # Filtrando apenas as zonas de interesse
    df_foco = df[df['ZONA'].isin(zonas_foco)]

    media_cra_zona = df_foco.groupby('ZONA')['CRA'].mean().reset_index()

    plt.figure(figsize=(12, 8))
    sns.barplot(x='ZONA', y='CRA', data=media_cra_zona, palette='muted')
    plt.title('Média do CRA por Zona da Cidade (Zonas Selecionadas)')
    plt.xlabel('Zona')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=90)
    plt.tight_layout()
    salvar_grafico('cra_por_zona', nome_pasta)


def plot_cra_evasao(df, nome_pasta):
    plt.figure(figsize=(10, 6))
    cra_evasao = df.groupby('STATUS_EVASAO')['CRA'].mean().reset_index()
    sns.barplot(x='STATUS_EVASAO', y='CRA', data=cra_evasao, palette='pastel')
    plt.title('Média do CRA por Status de Evasão')
    plt.xlabel('Status de Evasão')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico('cra_evasao', nome_pasta)


def plot_quantidade_alunos_por_zona(df, nome_pasta):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']

    df_foco = df[df['ZONA'].isin(zonas_foco)]
    contagem_alunos_zona = df_foco.groupby(['ZONA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='QUANTIDADE')

    plt.figure(figsize=(12, 8))
    sns.barplot(x='ZONA', y='QUANTIDADE', hue='FORMA_INGRESSO_SIMPLES', data=contagem_alunos_zona, palette='muted')
    plt.title('Quantidade de Alunos por Zona e Forma de Ingresso (Zonas Selecionadas)')
    plt.xlabel('Zona')
    plt.ylabel('Quantidade de Alunos')
    plt.xticks(rotation=90)
    plt.tight_layout()
    salvar_grafico('quantidade_alunos_por_zona_foco', nome_pasta)


def plot_cra_vs_distancia_urca(dataframe, nome_pasta):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='DISTANCIA_URCA', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='coolwarm')
    plt.title('Correlação entre CRA e Distância até a Urca')
    plt.xlabel('Distância até a Urca (km)')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('cra_vs_distancia_urca', nome_pasta)


def plot_distribuicao_cra_por_distancia(dataframe, nome_pasta):
    bins = [0, 10, 20, 30, 40]
    labels = ['0-10 km', '10-20 km', '20-30 km', '30-40 km']
    dataframe['Faixa_Distancia'] = pd.cut(dataframe['DISTANCIA_URCA'], bins=bins, labels=labels)

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Faixa_Distancia', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=dataframe, palette='muted')
    plt.title('Distribuição do CRA por Faixa de Distância até a Urca')
    plt.xlabel('Faixa de Distância')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('distribuicao_cra_por_distancia', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_geografica(df)
