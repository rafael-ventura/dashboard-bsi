import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import plot_boxplot, criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_performance_academica(df):
    criar_pasta_graficos()
    print("\nIniciando Análise de Performance Acadêmica...")

    plot_comparacao_cra(df)
    plot_correlacao_cra(df)
    plot_evasao_cra(df)

    print("\nAnálise de Performance Acadêmica Concluída!")


def plot_comparacao_cra(dataframe):
    plot_boxplot(x='FORMA_INGRESSO_SIMPLES', y='CRA', data=dataframe,
                 titulo='Distribuição do CRA entre Cotistas e Não-Cotistas', xlabel='Forma de Ingresso', ylabel='CRA')
    salvar_grafico('comparacao_cra')


def plot_correlacao_cra(dataframe):
    # Plotar correlações
    plt.figure(figsize=(6, 4))
    sns.heatmap(dataframe[['CRA', 'IDADE']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlação entre CRA e Idade')
    salvar_grafico('correlacao_cra_idade')


def plot_evasao_cra(dataframe):
    plot_boxplot(x='STATUS_EVASAO', y='CRA', data=dataframe, titulo='CRA por Status de Evasão', xlabel='Status de Evasão',
                 ylabel='CRA')
    salvar_grafico('evasao_cra')


if __name__ == "__main__":
    df = carregar_dados()
    analise_performance_academica(df)
