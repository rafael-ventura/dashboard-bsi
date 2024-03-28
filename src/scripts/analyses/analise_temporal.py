import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def definir_periodos(df):
    periodos_unicos = df['PER_PERIODO_INGRESSO_FORMAT'].unique()
    periodos_unicos = sorted(periodos_unicos)
    dfs_periodos = {periodo: df[df['PER_PERIODO_INGRESSO_FORMAT'] == periodo] for periodo in periodos_unicos}
    return dfs_periodos


def plot_tendencias(dfs_periodos):
    for periodo, df_periodo in dfs_periodos.items():
        sns.lineplot(data=df_periodo, x='PER_PERIODO_INGRESSO_FORMAT', y='CRA', estimator='mean')
        plt.title(f'Tendência do CRA - Período {periodo}')
        plt.xlabel('Período')
        plt.ylabel('CRA Médio')


def analise_temporal(df, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    print("\nIniciando Análise Temporal...")
    dfs_periodos = definir_periodos(df)
    plot_tendencias(dfs_periodos)

if __name__ == "__main__":
    df = pd.read_csv('../dados/processado/dfPrincipal.csv')
    analise_temporal(df)