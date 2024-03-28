import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import plot_lineplot, criar_pasta_graficos, salvar_grafico, carregar_dados

def analise_temporal(df):
    criar_pasta_graficos()
    print("\nIniciando Análise Temporal...")

    dfs_periodos = definir_periodos(df)
    plot_tendencias(dfs_periodos)

    print("\nAnálise Temporal Concluída!")

def definir_periodos(df):
    periodos_unicos = df['PER_PERIODO_INGRESSO_FORMAT'].unique()
    periodos_unicos = sorted(periodos_unicos)
    dfs_periodos = {periodo: df[df['PER_PERIODO_INGRESSO_FORMAT'] == periodo] for periodo in periodos_unicos}
    return dfs_periodos

def plot_tendencias(dfs_periodos):
    for periodo, df_periodo in dfs_periodos.items():
        plot_lineplot(x='PER_PERIODO_INGRESSO_FORMAT', y='CRA', data=df_periodo, titulo=f'Tendência do CRA - Período {periodo}', xlabel='Período', ylabel='CRA Médio')
        salvar_grafico(f'tendencia_cra_{periodo}')

if __name__ == "__main__":
    df = carregar_dados()
    analise_temporal(df)
