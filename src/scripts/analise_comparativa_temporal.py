import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.plots import criar_pasta_graficos, salvar_grafico
from src.utils.utils import carregar_dados


def analisar_grupos(df):
    criar_pasta_graficos()

    # Separando os grupos
    grupo_antes_cotas = df[df['ANO_PERIODO_INGRESSO'] < 2014]
    grupo_cotistas = df[(df['ANO_PERIODO_INGRESSO'] >= 2014) & (df['FORMA_INGRESSO_SIMPLES'] == 'Cotas')]
    grupo_nao_cotistas = df[(df['ANO_PERIODO_INGRESSO'] >= 2014) & (df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia')]

    # Analisando a média de CRA por grupo
    plotar_media_cra_por_grupo(grupo_antes_cotas, grupo_cotistas, grupo_nao_cotistas)

    # Analisando a taxa de evasão, conclusão e cursando por grupo
    plotar_taxa_evasao_conclusao_cursando(grupo_antes_cotas, grupo_cotistas, grupo_nao_cotistas)


def plotar_media_cra_por_grupo(grupo_antes, grupo_cotistas, grupo_nao_cotistas):
    # Calculando as médias
    media_antes = grupo_antes['CRA'].mean() if not grupo_antes.empty else 0
    media_cotistas = grupo_cotistas['CRA'].mean() if not grupo_cotistas.empty else 0
    media_nao_cotistas = grupo_nao_cotistas['CRA'].mean() if not grupo_nao_cotistas.empty else 0

    # Criando o DataFrame para plotagem
    data = {
        'Grupo': ['Antes das Cotas', 'Cotistas (2014+)', 'Não Cotistas (2014+)'],
        'Média CRA': [media_antes, media_cotistas, media_nao_cotistas]
    }
    df_media = pd.DataFrame(data)

    # Plotando
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Grupo', y='Média CRA', data=df_media, palette='pastel')

    # Adicionando os valores exatos nas barras
    for i in range(len(df_media)):
        ax.text(i, df_media['Média CRA'][i] + 0.02, round(df_media['Média CRA'][i], 2), ha='center', va='bottom')

    plt.title('Média de CRA por Grupo')
    plt.xlabel('Grupo')
    plt.ylabel('Média CRA')
    plt.tight_layout()
    salvar_grafico('media_cra_por_grupo')


def plotar_taxa_evasao_conclusao_cursando(grupo_antes, grupo_cotistas, grupo_nao_cotistas):
    def calcular_taxas(grupo):
        total = len(grupo)
        if total == 0:
            return 0, 0, 0
        evasao = len(grupo[grupo['STATUS_EVASAO'] == 'Evasão']) / total * 100
        conclusao = len(grupo[grupo['STATUS_EVASAO'] == 'Concluído']) / total * 100
        cursando = len(grupo[grupo['STATUS_EVASAO'] == 'Cursando']) / total * 100
        return evasao, conclusao, cursando

    # Calculando as taxas
    taxas_antes = calcular_taxas(grupo_antes)
    taxas_cotistas = calcular_taxas(grupo_cotistas)
    taxas_nao_cotistas = calcular_taxas(grupo_nao_cotistas)

    # Criando o DataFrame para plotagem
    data = {
        'Grupo': ['Antes das Cotas', 'Cotistas (2014+)', 'Não Cotistas (2014+)'],
        'Evasão': [taxas_antes[0], taxas_cotistas[0], taxas_nao_cotistas[0]],
        'Conclusão': [taxas_antes[1], taxas_cotistas[1], taxas_nao_cotistas[1]],
        'Cursando': [taxas_antes[2], taxas_cotistas[2], taxas_nao_cotistas[2]],
    }
    df_taxas = pd.DataFrame(data)

    # Plotando Evasão, Conclusão e Cursando no mesmo gráfico
    df_taxas_melted = df_taxas.melt(id_vars='Grupo', var_name='Status', value_name='Porcentagem')

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Grupo', y='Porcentagem', hue='Status', data=df_taxas_melted, palette='muted')
    plt.title('Taxa de Evasão, Conclusão e Cursando por Grupo')
    plt.xlabel('Grupo')
    plt.ylabel('Porcentagem (%)')
    plt.tight_layout()
    salvar_grafico('taxa_evasao_conclusao_cursando_por_grupo')


if __name__ == "__main__":
    df = carregar_dados()
    analisar_grupos(df)
