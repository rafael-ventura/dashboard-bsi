import geopandas as gpd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.utils.plots import salvar_grafico, plot_treemap, ajustar_estilos_grafico, adicionar_valores_barras, plotar_grafico_barras_laterais, adicionar_valores_barras_laterais
from src.utils.utils import carregar_dados, remover_acentos_e_maiusculas, pega_caminho_base
from colorama import Fore, init

from src.utils.zonas_geograficas import zona_norte, zona_oeste, zona_sul, bairros_centro, baixada_fluminense, regiao_volta_redonda, niteroi_sao_goncalo, regiao_serrana, regiao_campos, regiao_dos_lagos

# Inicializa o Colorama
init(autoreset=True)


def analise_geografica(df_periodo, nome_pasta, periodo_nome):
    print(Fore.BLUE + f"\nIniciando Análise Geográfica para o período: {periodo_nome}")

    # Remover alunos com bairro desconhecido
    df_periodo = df_periodo[df_periodo['BAIRRO'] != 'desconhecido']

    # Verifica se existem alunos no período
    if df_periodo.empty:
        print(Fore.RED + f"Sem dados de alunos para o período: {periodo_nome}")
        return

    bairros_rj = carregar_bairros_rj()
    bairros_rj = consolidar_ilha_do_governador(bairros_rj)
    bairros_rj = preparar_dados_bairros(df_periodo, bairros_rj)

    # Executar as análises geográficas para cada período
    plot_mapa_calor_comparativo(bairros_rj, df_periodo, nome_pasta, periodo_nome)
    plot_treemap_comparativo_bairros(df_periodo, nome_pasta, periodo_nome)
    # plot_cra_por_distancia(df_periodo, nome_pasta, periodo_nome)
    plot_cra_por_zona(df_periodo, nome_pasta, periodo_nome)
    plot_cra_evasao(df_periodo, nome_pasta, periodo_nome)
    plot_quantidade_alunos_por_zona(df_periodo, nome_pasta, periodo_nome)
    plot_cra_por_bairro(df_periodo, nome_pasta, periodo_nome)
    plot_cra_por_bairro_4_alunos(df_periodo, nome_pasta, periodo_nome)
    plot_cra_top_10_bairros(df_periodo, nome_pasta, periodo_nome)
    plot_cra_bottom_10_bairros(df_periodo, nome_pasta, periodo_nome)
    plot_quantidade_alunos_por_zona_geografica_e_ingresso(df_periodo, nome_pasta, periodo_nome)
    plot_quantidade_alunos_por_zona_e_ingresso(df_periodo, nome_pasta, periodo_nome)

    print(Fore.GREEN + f"\nAnálise Geográfica Concluída para o período: {periodo_nome}")


def preparar_dados_bairros(df, bairros_rj):
    """
    Prepara os dados de bairros para plotagem, lidando com casos de bairros desconhecidos ou fora do RJ.
    """
    # Filtra alunos com bairros 'Desconhecido' ou que não são do RJ
    print("Antes de filtrar por cidade e bairro:")
    print(df[['BAIRRO', 'CIDADE']].head())

    df = df[df['BAIRRO'] != 'desconhecido']
    df = df[df['CIDADE'] == 'rio de janeiro']

    print("\nDepois de filtrar por cidade e bairro:")
    print(df[['BAIRRO', 'CIDADE']].head())

    # Normaliza os nomes dos bairros para garantir correspondência
    df['BAIRRO'] = df['BAIRRO'].apply(remover_acentos_e_maiusculas)
    bairros_rj['nome'] = bairros_rj['nome'].apply(remover_acentos_e_maiusculas)

    print("\nDataFrame de alunos após normalização dos bairros:")
    print(df['BAIRRO'].unique())

    print("\nDataFrame de bairros_rj após normalização:")
    print(bairros_rj['nome'].unique())

    # Faz a contagem de alunos por bairro
    contagem_alunos = df['BAIRRO'].value_counts().reset_index()
    contagem_alunos.columns = ['nome', 'ALUNOS']

    # Identifica os bairros que estão no DataFrame de bairros_rj, mas não no de alunos
    bairros_faltantes = set(bairros_rj['nome']) - set(contagem_alunos['nome'])
    print("\nBairros faltantes no DataFrame de alunos:")
    print(bairros_faltantes)

    # Adiciona os bairros faltantes com contagem 0 ao DataFrame de contagem de alunos
    if bairros_faltantes:
        bairros_faltantes_df = pd.DataFrame({
            'nome': list(bairros_faltantes),
            'ALUNOS': [0] * len(bairros_faltantes)
        })
        contagem_alunos = pd.concat([contagem_alunos, bairros_faltantes_df], ignore_index=True)

    # Faz o merge dos bairros, garantindo que todos os bairros tenham uma contagem
    bairros_rj_merged = bairros_rj.merge(contagem_alunos, on='nome', how='left')

    # Verificar se a coluna 'ALUNOS' existe após o merge
    if 'ALUNOS' not in bairros_rj_merged.columns:
        print(Fore.RED + "Erro: A coluna 'ALUNOS' não foi criada corretamente no merge. Criando manualmente com valor 0.")
        bairros_rj_merged['ALUNOS'] = 0

    # Preenche os valores NaN na coluna 'ALUNOS' com 0
    bairros_rj_merged['ALUNOS'] = bairros_rj_merged['ALUNOS'].fillna(0).astype(int)

    print("\nDataFrame final de 'bairros_rj_merged' com contagem de alunos:")
    print(bairros_rj_merged[['nome', 'ALUNOS']].head())

    return bairros_rj_merged


def plot_mapa_calor_comparativo(bairros_rj, df, nome_pasta, periodo_nome):
    """
    Plota um mapa comparativo de calor para cotistas e não cotistas por bairro.
    """
    fig, axs = plt.subplots(1, 2, figsize=(30, 15))

    # Define o colormap e a normalização uma única vez para ambos os gráficos
    cmap = colors.ListedColormap(sns.color_palette("Blues", 12))
    norm = colors.BoundaryNorm(boundaries=[0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50], ncolors=12)

    # Filtra os dados de cotistas e não cotistas
    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    # Print para inspeção de dados filtrados
    print("\nCotistas DataFrame:")
    print(cotistas.head())

    print("\nNão Cotistas DataFrame:")
    print(nao_cotistas.head())

    # Valida se existem cotistas
    if cotistas.empty:
        print(Fore.YELLOW + f"Aviso: Não há dados de cotistas para o período {periodo_nome}. Pulando plotagem de cotistas.")
    else:
        bairros_rj_cotistas = preparar_dados_bairros(cotistas, bairros_rj.copy())
        bairros_rj_cotistas.plot(column='ALUNOS', ax=axs[0], legend=True, cmap=cmap, norm=norm, edgecolor='black')
        axs[0].set_title(f'Densidade de Alunos Cotistas por Bairro')
        axs[0].axis('off')

    # Valida se existem não cotistas
    if nao_cotistas.empty:
        print(Fore.YELLOW + f"Aviso: Não há dados de ampla concorrência para o período {periodo_nome}. Pulando plotagem de ampla concorrência.")
    else:
        bairros_rj_nao_cotistas = preparar_dados_bairros(nao_cotistas, bairros_rj.copy())
        bairros_rj_nao_cotistas.plot(column='ALUNOS', ax=axs[1], legend=True, cmap=cmap, norm=norm, edgecolor='black')
        axs[1].set_title(f'Densidade de Alunos Ampla Concorrência por Bairro')
        axs[1].axis('off')

    # Salva o gráfico
    salvar_grafico(f'mapa_calor_comparativo_{periodo_nome}', nome_pasta)


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


def plot_treemap_comparativo_bairros(df, nome_pasta, periodo_nome):
    cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
    nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

    # Corrigir contagem de alunos para garantir que os dados estejam no formato correto (int)
    cotistas_count = cotistas['BAIRRO'].value_counts().nlargest(20)
    nao_cotistas_count = nao_cotistas['BAIRRO'].value_counts().nlargest(20)

    # Definindo um threshold mínimo para o treemap, por exemplo, 1
    threshold = 1

    # Corrigindo a chamada de `plot_treemap` e garantindo que `threshold` seja comparado corretamente
    plot_treemap(cotistas_count.astype(int), threshold, f'Treemap dos 20 Bairros com mais Alunos Cotistas - {periodo_nome}', 'Spectral', nome_pasta, show_values=True)
    plot_treemap(nao_cotistas_count.astype(int), threshold, f'Treemap dos 20 Bairros com mais Alunos Ampla Concorrência - {periodo_nome}', 'Spectral', nome_pasta, show_values=True)


# O método abaixo foi comentado conforme sua solicitação, e mantido sem alterações:

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
    """
    Plota a média de CRA por bairro, sem filtro de número mínimo de alunos.
    """
    cra_bairro = df.groupby('BAIRRO')['CRA'].mean().reset_index()
    cra_bairro = cra_bairro.sort_values(by='CRA')

    # Plotar o gráfico de barras laterais
    fig, ax = plt.subplots(figsize=(20, max(6, int(len(cra_bairro) / 4))))
    plotar_grafico_barras_laterais(cra_bairro, 'CRA', 'BAIRRO',
                                   title=f'Média do CRA por Bairro',
                                   xlabel='CRA', ylabel='Bairro', ax=ax)

    # Salvar o gráfico
    salvar_grafico(f'cra_por_bairro_{periodo_nome}', nome_pasta)


def plot_cra_por_bairro_4_alunos(df, nome_pasta, periodo_nome):
    """
    Plota a média de CRA por bairro, considerando apenas bairros com pelo menos 4 alunos.
    """
    # Filtrar apenas os bairros com pelo menos 4 alunos
    bairros_filtrados = df.groupby('BAIRRO').filter(lambda x: len(x) >= 4)
    cra_bairro = bairros_filtrados.groupby('BAIRRO')['CRA'].mean().reset_index()
    cra_bairro = cra_bairro.sort_values(by='CRA')

    # Plotar o gráfico de barras laterais
    fig, ax = plt.subplots(figsize=(20, max(6, int(len(cra_bairro) / 2))))
    plotar_grafico_barras_laterais(cra_bairro, 'CRA', 'BAIRRO',
                                   title=f'Média do CRA por Bairro (Com pelo menos 4 alunos)',
                                   xlabel='CRA', ylabel='Bairro', ax=ax)

    # Salvar o gráfico
    salvar_grafico(f'cra_por_bairro_4_alunos_{periodo_nome}', nome_pasta)


def plot_cra_top_10_bairros(df, nome_pasta, periodo_nome):
    """
    Plota os 10 bairros com maior média de CRA.
    """
    cra_bairro = df.groupby('BAIRRO')['CRA'].mean().reset_index()
    cra_bairro = cra_bairro.sort_values(by='CRA', ascending=False).head(10)

    # Plotar o gráfico de barras laterais
    fig, ax = plt.subplots(figsize=(14, 10))
    plotar_grafico_barras_laterais(cra_bairro, 'CRA', 'BAIRRO',
                                   title=f'Top 10 Bairros com Maior CRA',
                                   xlabel='CRA', ylabel='Bairro', ax=ax)

    # Salvar o gráfico
    salvar_grafico(f'cra_top_10_bairros_{periodo_nome}', nome_pasta)


def plot_cra_bottom_10_bairros(df, nome_pasta, periodo_nome):
    """
    Plota os 10 bairros com menor média de CRA.
    """
    cra_bairro = df.groupby('BAIRRO')['CRA'].mean().reset_index()
    cra_bairro = cra_bairro.sort_values(by='CRA').head(10)

    # Plotar o gráfico de barras laterais
    fig, ax = plt.subplots(figsize=(14, 10))
    plotar_grafico_barras_laterais(cra_bairro, 'CRA', 'BAIRRO',
                                   title=f'Top 10 Bairros com Menor CRA',
                                   xlabel='CRA', ylabel='Bairro', ax=ax)

    # Salvar o gráfico
    salvar_grafico(f'cra_bottom_10_bairros_{periodo_nome}', nome_pasta)


def plot_cra_por_zona(df, nome_pasta, periodo_nome):
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']
    df_foco = df[df['ZONA'].isin(zonas_foco)]
    media_cra_zona = df_foco.groupby('ZONA')['CRA'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='ZONA', y='CRA', data=media_cra_zona, palette='muted', ax=ax)

    adicionar_valores_barras(ax)
    ajustar_estilos_grafico(ax, title=f'Média do CRA por Zona  (Zonas Selecionadas)', xlabel='Zona', ylabel='CRA Médio')

    salvar_grafico(f'cra_por_zona_{periodo_nome}', nome_pasta)


def plot_cra_evasao(df, nome_pasta, periodo_nome):
    fig, ax = plt.subplots(figsize=(10, 6))
    cra_evasao = df.groupby('STATUS_EVASAO')['CRA'].mean().reset_index()
    sns.barplot(x='STATUS_EVASAO', y='CRA', data=cra_evasao, palette='pastel', ax=ax)

    adicionar_valores_barras(ax)
    ajustar_estilos_grafico(ax, title=f'Média do CRA por Status de Evasão ', xlabel='Status de Evasão', ylabel='CRA Médio')

    salvar_grafico(f'cra_evasao_{periodo_nome}', nome_pasta)


def plot_quantidade_alunos_por_zona(df, nome_pasta, periodo_nome):
    """
    Plota a quantidade de alunos por zona e forma de ingresso, exibindo percentuais em relação ao total de alunos.
    """
    zonas_foco = ['Zona Sul', 'Zona Oeste', 'Zona Norte', 'Centro', 'Baixada Fluminense']
    df_foco = df[df['ZONA'].isin(zonas_foco)]

    # Agrupar por Zona e Forma de Ingresso e contar o número de alunos
    contagem_alunos_zona = df_foco.groupby(['ZONA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='QUANTIDADE')

    # Calcular o total de alunos para obter o percentual correto
    total_alunos = contagem_alunos_zona['QUANTIDADE'].sum()

    # Calcular o percentual correto em relação ao total de alunos
    contagem_alunos_zona['PERCENTUAL'] = (contagem_alunos_zona['QUANTIDADE'] / total_alunos) * 100

    # Plotar o gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='ZONA', y='PERCENTUAL', hue='FORMA_INGRESSO_SIMPLES', data=contagem_alunos_zona, palette='muted', ax=ax)

    # Adicionar os valores nas barras
    adicionar_valores_barras(ax, exibir_percentual=True, total=100, fontsize=14)

    # Ajustar estilos
    ajustar_estilos_grafico(ax, title=f'Quantidade de Alunos por Zona e Forma de Ingresso', xlabel='Zona', ylabel='Percentual de Alunos (%)')

    # Salvar o gráfico
    salvar_grafico(f'quantidade_alunos_por_zona_percentual_{periodo_nome}', nome_pasta)


def plot_quantidade_alunos_por_zona_e_ingresso(df, nome_pasta, periodo_nome):
    """
    Plota a porcentagem de alunos por zona e forma de ingresso (Cotistas e Não Cotistas) no mesmo gráfico.
    """
    zonas_municipio = ['Centro', 'Zona Norte', 'Zona Oeste', 'Zona Sul']
    df['ZONA_MUNICIPIO'] = df['ZONA'].apply(lambda z: z if z in zonas_municipio else 'Fora do Município')

    # Agrupar por Zona e Forma de Ingresso e contar o número de alunos
    contagem_alunos_zona_municipio = df.groupby(['ZONA_MUNICIPIO', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='QUANTIDADE')

    # Calcular o total de alunos para obter o percentual correto
    total_alunos = contagem_alunos_zona_municipio['QUANTIDADE'].sum()

    # Calcular o percentual correto em relação ao total de alunos
    contagem_alunos_zona_municipio['PERCENTUAL'] = (contagem_alunos_zona_municipio['QUANTIDADE'] / total_alunos) * 100

    # Plotar o gráfico de barras normais com agrupamento por Forma de Ingresso
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='ZONA_MUNICIPIO', y='PERCENTUAL', hue='FORMA_INGRESSO_SIMPLES', data=contagem_alunos_zona_municipio, palette='muted', ax=ax)

    # Adicionar os valores nas barras
    adicionar_valores_barras(ax, exibir_percentual=True, total=100, fontsize=14)

    # Ajustar estilos
    ajustar_estilos_grafico(ax, title=f'Percentual de Alunos por Zona e Forma de Ingresso', xlabel='Zona', ylabel='Percentual de Alunos (%)')

    # Salvar o gráfico
    salvar_grafico(f'percentual_alunos_por_zona_e_ingresso_{periodo_nome}', nome_pasta)


def plot_quantidade_alunos_por_zona_geografica_e_ingresso(df, nome_pasta, periodo_nome):
    """
    Plota a porcentagem de alunos por zona geográfica com base nas listas de zonas definidas,
    separando por forma de ingresso (cotistas e não cotistas).
    """
    df['BAIRRO'] = df['BAIRRO'].apply(remover_acentos_e_maiusculas)

    def categorizar_zona(bairro):
        if bairro in [remover_acentos_e_maiusculas(b) for b in zona_norte]:
            return 'Zona Norte'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in zona_oeste]:
            return 'Zona Oeste'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in zona_sul]:
            return 'Zona Sul'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in bairros_centro]:
            return 'Centro'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in baixada_fluminense]:
            return 'Baixada Fluminense'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in regiao_volta_redonda]:
            return 'Região Volta Redonda'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in niteroi_sao_goncalo]:
            return 'Niterói/São Gonçalo'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in regiao_serrana]:
            return 'Região Serrana'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in regiao_campos]:
            return 'Região Campos'
        elif bairro in [remover_acentos_e_maiusculas(b) for b in regiao_dos_lagos]:
            return 'Região dos Lagos'
        else:
            return 'Fora do Estado'

    # Aplicar a categorização de zonas geográficas
    df['ZONA_GEOGRAFICA'] = df['BAIRRO'].apply(categorizar_zona)

    # Agrupar por Zona Geográfica e Forma de Ingresso e contar o número de alunos
    contagem_alunos_zona_geografica = df.groupby(['ZONA_GEOGRAFICA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='QUANTIDADE')

    # Calcular o total de alunos para obter o percentual correto
    total_alunos = contagem_alunos_zona_geografica['QUANTIDADE'].sum()

    # Calcular o percentual correto em relação ao total de alunos
    contagem_alunos_zona_geografica['PERCENTUAL'] = (contagem_alunos_zona_geografica['QUANTIDADE'] / total_alunos) * 100

    # Plotar o gráfico de barras verticais com agrupamento por Forma de Ingresso
    fig, ax = plt.subplots(figsize=(16, 12))

    sns.barplot(x='ZONA_GEOGRAFICA', y='PERCENTUAL', hue='FORMA_INGRESSO_SIMPLES', data=contagem_alunos_zona_geografica, palette='muted', ax=ax)

    # Adicionar os valores nas barras
    adicionar_valores_barras(ax, exibir_percentual=True, total=100, fontsize=14)

    # Ajustar estilos
    ajustar_estilos_grafico(ax, title=f'Percentual de Alunos por Zona Geográfica e Forma de Ingresso', xlabel='Zona Geográfica', ylabel='Percentual de Alunos (%)')

    # Salvar o gráfico
    salvar_grafico(f'percentual_alunos_por_zona_geografica_e_ingresso_{periodo_nome}', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_geografica(df, "resultados", "2023")
