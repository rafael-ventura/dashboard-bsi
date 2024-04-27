from src.utils import criar_pasta_graficos, salvar_grafico, carregar_dados
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def analise_exploratoria(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise Exploratória...")

    # Plotagem de distribuições
    plot_distribuicao_sexo(dataframe)
    plot_distribuicao_idade(dataframe)
    plot_distribuicao_evasao(dataframe)
    plot_distribuicao_CRA(dataframe)

    # Análises estatísticas
    estatisticas_descritivas_cra(dataframe)
    plot_media_cra_por_ingresso(dataframe)

    # Análises de frequência
    plot_tabela_frequencia(dataframe, 'SEXO')
    plot_tabela_frequencia(dataframe, 'FORMA_INGRESSO_SIMPLES')
    plot_tabela_frequencia(dataframe, 'STATUS_EVASAO')

    print("\nAnálise Exploratória Concluída!")


def estatisticas_descritivas_cra(dataframe):
    print("\nEstatísticas Descritivas para CRA:")
    print("Mínimo:", dataframe['CRA'].min())
    print("Máximo:", dataframe['CRA'].max())
    print("Moda:", dataframe['CRA'].mode())
    print("Amplitude:", dataframe['CRA'].max() - dataframe['CRA'].min())
    print("Média:", dataframe['CRA'].mean())
    print("Mediana:", dataframe['CRA'].median())
    print("Variância:", dataframe['CRA'].var())
    print("Desvio-padrão:", dataframe['CRA'].std())
    print("Assimetria:", dataframe['CRA'].skew())
    print("Curtose:", dataframe['CRA'].kurtosis())
    print("Quartil 1:", dataframe['CRA'].quantile(0.25))
    print("Quartil 2:", dataframe['CRA'].quantile(0.5))
    print("Quartil 3:", dataframe['CRA'].quantile(0.75))
    print("Coeficiente de Variação:", dataframe['CRA'].std() / dataframe['CRA'].mean() * 100)


def plot_distribuicao_CRA(dataframe):
    if 'CRA' in dataframe.columns:
        dataframe['CRA'] = dataframe['CRA'].astype(str).str.replace(',', '.').astype(float)
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('viridis')[0]
        sns.countplot(x='CRA', data=dataframe, color=color)
        plt.title('Distribuição do CRA')
        plt.xlabel('CRA')
        plt.ylabel('Quantidade de Alunos')
        plt.tight_layout()
        salvar_grafico('distribuicao_CRA')
    else:
        print("A coluna 'CRA' não existe no DataFrame.")


def plot_distribuicao_sexo(dataframe):
    if 'SEXO' in dataframe.columns:
        plt.figure(figsize=(8, 6))
        palette_sexo = {'F': '#FF6347', 'M': '#4169E1'}
        sns.countplot(x='SEXO', data=dataframe, palette=palette_sexo)
        plt.title('Distribuição por Sexo')
        plt.xlabel('Sexo')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_sexo')
    else:
        print("A coluna 'SEXO' não existe no DataFrame.")


def plot_distribuicao_idade(dataframe):
    if 'IDADE_INGRESSO' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('viridis')[0]
        sns.histplot(dataframe['IDADE_INGRESSO'], kde=True, color=color)
        plt.title('Distribuição por Idade')
        plt.xlabel('Idade')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_idade')
    else:
        print("A coluna 'IDADE' não existe no DataFrame.")


def plot_distribuicao_evasao(dataframe):
    if 'STATUS_EVASAO' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('pastel')[0]
        sns.countplot(x='CRA', data=dataframe, color=color)
        plt.title('Distribuição de Evasões')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_evasao')
    else:
        print("A coluna 'STATUS_EVASAO' não existe no DataFrame.")


def plot_tabela_frequencia(dataframe, coluna):
    print(f"\nTabela de Frequência para {coluna}:")
    frequencias = dataframe[coluna].value_counts()
    print(frequencias)

    print(f"\nTabela de Frequência Relativa para {coluna}:")
    frequencias_relativas = dataframe[coluna].value_counts(normalize=True) * 100
    print(frequencias_relativas)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=frequencias.index, y=frequencias.values)
    plt.title(f'Frequências para {coluna}')
    plt.ylabel('Frequência Absoluta')
    plt.xlabel(coluna)
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'frequencias_{coluna}')

    if len(frequencias) <= 10:
        plt.figure(figsize=(8, 8))
        plt.pie(frequencias, labels=frequencias.index, autopct='%1.1f%%', startangle=90)
        plt.title(f'Proporção para {coluna}')
        plt.tight_layout()
        salvar_grafico(f'proporcao_{coluna}')


def plot_media_cra_por_ingresso(dataframe):
    plt.figure(figsize=(12, 6))

    ordenado = dataframe.groupby('IDADE_INGRESSO')['CRA'].mean().reset_index().sort_values('IDADE_INGRESSO')
    sns.barplot(x='IDADE_INGRESSO', y='CRA', data=ordenado, palette="viridis")
    plt.title('Média de CRA por Idade de Ingresso')
    plt.xlabel('Idade de Ingresso')
    plt.ylabel('CRA Médio')
    plt.xticks(rotation=45)
    plt.tight_layout()

    salvar_grafico('media_cra_por_idade_ingresso')


if __name__ == "__main__":
    df = carregar_dados()
    analise_exploratoria(df)
