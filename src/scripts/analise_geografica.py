import geopandas as gpd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.utils.plots import criar_pasta_graficos, salvar_grafico, plot_treemap
from src.utils.utils import carregar_dados, pega_caminho_base, remover_acentos_e_maiusculas


def executar_analise_geografica(df):
    print("\nIniciando Análise Geográfica...")
    criar_pasta_graficos()

    bairros_rj = carregar_bairros_rj()
    bairros_rj = consolidar_ilha_do_governador(bairros_rj)
    bairros_rj = preparar_dados_bairros(df, bairros_rj)

    plot_mapa_calor_comparativo(bairros_rj, df)
    plot_treemap_comparativo_bairros(df)
    plot_cra_por_distancia(df)
    plot_media_cra_por_zona(df)
    plot_quantidade_alunos_por_zona(df)

    print("\nAnálise Geográfica Concluída com Sucesso!")


def preparar_dados_bairros(df, bairros_rj):
    df['BAIRRO'] = df['BAIRRO'].apply(remover_acentos_e_maiusculas)
    bairros_rj['nome'] = bairros_rj['nome'].apply(remover_acentos_e_maiusculas)

    # Contagem de alunos por bairro
    contagem_alunos = df['BAIRRO'].value_counts().reset_index()
    contagem_alunos.columns = ['nome', 'ALUNOS']

    # Faz o merge com bairros_rj, preenchendo com 0 onde não houver correspondência
    bairros_rj = bairros_rj.merge(contagem_alunos, on='nome', how='left')

    # Verifica se a coluna 'ALUNOS' existe antes de manipulá-la
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


def plot_mapa_calor_comparativo(bairros_rj, df):
    fig, axs = plt.subplots(1, 2, figsize=(30, 15))

    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    bairros_rj_cotistas = preparar_dados_bairros(cotistas, bairros_rj.copy())
    bairros_rj_nao_cotistas = preparar_dados_bairros(nao_cotistas, bairros_rj.copy())

    cmap = colors.ListedColormap(sns.color_palette("Blues", 12))
    norm = colors.BoundaryNorm(boundaries=[0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50], ncolors=12)

    bairros_rj_cotistas.plot(column='ALUNOS', ax=axs[0], legend=True, cmap=cmap, norm=norm, edgecolor='black')
    axs[0].set_title('Densidade de Alunos Cotistas por Bairro')
    axs[0].axis('off')

    bairros_rj_nao_cotistas.plot(column='ALUNOS', ax=axs[1], legend=True, cmap=cmap, norm=norm, edgecolor='black')
    axs[1].set_title('Densidade de Alunos Ampla Concorrência por Bairro')
    axs[1].axis('off')

    salvar_grafico('mapa_calor_comparativo')


def plot_treemap_comparativo_bairros(df):
    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    cotistas_count = cotistas['BAIRRO'].value_counts().nlargest(20)
    nao_cotistas_count = nao_cotistas['BAIRRO'].value_counts().nlargest(20)

    plot_treemap(cotistas_count, 0, 'Top 20 Bairros com mais Alunos Cotistas')
    plot_treemap(nao_cotistas_count, 0, 'Top 20 Bairros com mais Alunos Ampla Concorrência')


def plot_cra_por_distancia(df):
    plt.figure(figsize=(10, 6))

    # Ajustando o gráfico para raio de 40 km
    sns.lineplot(x='DISTANCIA_URCA', y='CRA', hue='FORMA_INGRESSO_SIMPLES', data=df[df['DISTANCIA_URCA'] <= 40])

    plt.title('Relação entre Distância até a Urca e CRA (até 40 km)')
    plt.xlabel('Distância até a Urca (km)')
    plt.ylabel('CRA')
    plt.tight_layout()
    salvar_grafico('cra_por_distancia_40km')


def plot_media_cra_por_zona(df):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']

    # Filtrando apenas as zonas de interesse
    df_foco = df[df['ZONA'].isin(zonas_foco)]

    # Calculando a média do CRA por zona
    media_cra_zona = df_foco.groupby('ZONA')['CRA'].mean().reset_index()

    plt.figure(figsize=(12, 8))
    sns.barplot(x='ZONA', y='CRA', data=media_cra_zona, palette='muted')
    plt.title('Média do CRA por Zona da Cidade (Zonas Selecionadas)')
    plt.xlabel('Zona')
    plt.ylabel('Média do CRA')
    plt.xticks(rotation=90)  # Rotaciona os labels para 90 graus
    plt.tight_layout()
    salvar_grafico('media_cra_por_zona_foco')


def plot_quantidade_alunos_por_zona(df):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']

    # Filtrando apenas as zonas de interesse
    df_foco = df[df['ZONA'].isin(zonas_foco)]

    # Contagem de alunos por zona e tipo de ingresso
    contagem_alunos_zona = df_foco.groupby(['ZONA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='QUANTIDADE')

    plt.figure(figsize=(12, 8))
    sns.barplot(x='ZONA', y='QUANTIDADE', hue='FORMA_INGRESSO_SIMPLES', data=contagem_alunos_zona, palette='muted')
    plt.title('Quantidade de Alunos por Zona e Forma de Ingresso (Zonas Selecionadas)')
    plt.xlabel('Zona')
    plt.ylabel('Quantidade de Alunos')
    plt.xticks(rotation=90)  # Rotaciona os labels para 90 graus
    plt.tight_layout()
    salvar_grafico('quantidade_alunos_por_zona_foco')


if __name__ == "__main__":
    df = carregar_dados()
    executar_analise_geografica(df)
