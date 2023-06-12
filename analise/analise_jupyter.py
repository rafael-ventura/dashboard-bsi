import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Carregar o dataframe
df = pd.read_csv('../dados/dfPrincipal.csv')

# Converter as colunas de data para o tipo datetime
df['DT_NASCIMENTO'] = pd.to_datetime(df['DT_NASCIMENTO'])
df['DT_EVASAO'] = pd.to_datetime(df['DT_EVASAO'])

# Separar o dataframe em grupos
# As datas exatas para 'Antes das Cotas', 'Depois das Cotas' e 'Período Pandemico' precisarão ser ajustadas
antes_cotas = df[df['DT_INGRESSO'] < '2010-01-01']
depois_cotas = df[(df['DT_INGRESSO'] >= '2010-01-01') & (df['DT_INGRESSO'] < '2020-03-01')]
periodo_pandemico = df[(df['DT_INGRESSO'] >= '2020-03-01') & (df['DT_INGRESSO'] < '2021-06-30')]
todos = df.copy()  # inclui todos os três grupos acima

# Separação em Cotistas e Não-Cotistas
# Isso pressupõe que a coluna 'FORMA_INGRESSO_SIMPLES' indica se o aluno é cotista ou não
cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] != 'Cotas']

# Listas para percorrer facilmente os grupos e seus nomes
grupos = [antes_cotas, depois_cotas, periodo_pandemico, todos, cotistas, nao_cotistas]
nomes_grupos = ['Antes das Cotas', 'Depois das Cotas', 'Período Pandemico', 'Todos', 'Cotistas', 'Não-Cotistas']

for grupo, nome in zip(grupos, nomes_grupos):
    print(f'Analisando {nome}...')

    # Média do CR
    media_cr = grupo['CRA'].mean()
    print(f'Média do CR: {media_cr}')

    # Média do CR por período
    media_cr_periodo = grupo.groupby('PERIODO_INGRESSO')['CRA'].mean()
    print('Média do CR por período:')
    print(media_cr_periodo)

    # Média do CR por ano
    media_cr_ano = grupo.groupby(grupo['DT_INGRESSO'].dt.year)['CRA'].mean()
    print('Média do CR por ano:')
    print(media_cr_ano)

    # Taxa de evasão
    taxa_evasao = len(grupo[grupo['FORMA_EVASAO'] == 'Evasão']) / len(grupo)
    print(f'Taxa de evasão: {taxa_evasao * 100}%')

    # Taxa de evasão por período
    taxa_evasao_periodo = grupo[grupo['FORMA_EVASAO'] == 'Evasão'].groupby('PERIODO_INGRESSO').size() / grupo.groupby(
        'PERIODO_INGRESSO').size()
    print('Taxa de evasão por período:')
    print(taxa_evasao_periodo)

    # Taxa de evasão por ano
    taxa_evasao_ano = grupo[grupo['FORMA_EVASAO'] == 'Evasão'].groupby(
        grupo['DT_INGRESSO'].dt.year).size() / grupo.groupby(grupo['DT_INGRESSO'].dt.year).size()
    print('Taxa de evasão por ano:')
    print(taxa_evasao_ano)

    # Comparação do CR médio entre os que evadiram e os que concluíram
    cr_medio_evasao = grupo[grupo['FORMA_EVASAO'] == 'Evasão']['CRA'].mean()
    cr_medio_conclusao = grupo[grupo['FORMA_EVASAO'] == 'Concluído']['CRA'].mean()
    print(f'CR médio dos que evadiram: {cr_medio_evasao}')
    print(f'CR médio dos que concluíram: {cr_medio_conclusao}')

    # Visualização do mapa de calor do CR
    # A função heatmap do Seaborn exige dados em formato de matriz
    # Dependendo de como você deseja visualizar o CR, essa parte do código pode precisar ser ajustada
    plt.figure(figsize=(10, 8))
    sns.heatmap(grupo['CRA'].values.reshape(-1, 1))
    plt.title(f'Mapa de Calor do CR - {nome}')
    plt.show()

    # Distância média do centro de cada bairro até a UNIRIO
    # Isso requer um dataframe de distâncias com as distâncias de cada bairro até a UNIRIO
    # As distâncias poderiam ser calculadas a partir das coordenadas de latitude e longitude usando a função cdist do Scipy
    # Por simplicidade, vamos assumir que temos um dataframe 'distancias' com as colunas 'BAIRRO' e 'DISTANCIA'
    distancias = pd.read_csv('../../dados/distancias.csv')
    grupo = grupo.merge(distancias, on='BAIRRO')
    distancia_media = grupo['DISTANCIA'].mean()
    print(f'Distância média do centro de cada bairro até a UNIRIO: {distancia_media}')

    # Comparação da evasão olhando a zona que mora do RJ
    # Isso pressupõe que existe uma coluna 'ZONA' no dataframe indicando a zona do Rio de Janeiro onde o aluno mora
    evasao_por_zona = grupo[grupo['FORMA_EVASAO'] == 'Evasão'].groupby('ZONA').size() / grupo.groupby('ZONA').size()
    print('Taxa de evasão por zona:')
    print(evasao_por_zona)

