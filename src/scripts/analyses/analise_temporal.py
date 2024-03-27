import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def definir_periodos(df):
    periodos = {
        'Antes das Cotas': ('2000-01-01', '2009-12-31'),
        'Depois das Cotas': ('2010-01-01', '2019-12-31'),
        'Período Pandêmico': ('2020-01-01', '2022-12-31')
    }
    dfs_periodos = {nome: df[(df['DT_INGRESSO'] >= inicio) & (df['DT_INGRESSO'] <= fim)] for nome, (inicio, fim) in periodos.items()}
    return dfs_periodos

def plot_tendencias(dfs_periodos):
    for nome, df_periodo in dfs_periodos.items():
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_periodo, x='ANO_PERIODO_INGRESSO', y='CRA', estimator='mean')
        plt.title(f'Tendência do CRA ao longo do tempo - {nome}')
        plt.xlabel('Ano')
        plt.ylabel('CRA Médio')
        plt.show()

def analise_temporal(df):
    print("\nIniciando Análise Temporal...")
    dfs_periodos = definir_periodos(df)
    plot_tendencias(dfs_periodos)

if __name__ == "__main__":
    df = pd.read_csv('../dados/processado/dfPrincipal.csv')
    analise_temporal(df)
