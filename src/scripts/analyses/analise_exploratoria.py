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
    plot_countplot_CRA(dataframe)

    # Análises estatísticas
    estatisticas_descritivas_cra(dataframe)
    analise_correlacao_cra_idade(dataframe)

    # Análises de frequência
    tabela_de_frequencia(dataframe, 'SEXO')
    tabela_de_frequencia(dataframe, 'FORMA_INGRESSO_SIMPLES')
    tabela_de_frequencia(dataframe, 'STATUS_EVASAO')

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


def plot_countplot_CRA(dataframe):
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
    if 'IDADE' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        color = sns.color_palette('viridis')[0]
        sns.histplot(dataframe['IDADE'], kde=True, color=color)
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


def tabela_de_frequencia(dataframe, coluna):
    print(f"\nTabela de Frequência para {coluna}:")
    frequencias = dataframe[coluna].value_counts()
    print(frequencias)

    print(f"\nTabela de Frequência Relativa (Percentual) para {coluna}:")
    frequencias_relativas = dataframe[coluna].value_counts(normalize=True) * 100
    print(frequencias_relativas)

    # Plotar gráfico de barras para frequências absolutas
    plt.figure(figsize=(10, 6))
    sns.barplot(x=frequencias.index, y=frequencias.values)
    plt.title(f'Frequências para {coluna}')
    plt.ylabel('Frequência Absoluta')
    plt.xlabel(coluna)
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico(f'frequencias_{coluna}')

    # Plotar gráfico de setores para frequências relativas, se for apropriado
    if len(frequencias) <= 10:  # Limita a plotagem do gráfico de setores a no máximo 10 categorias
        plt.figure(figsize=(8, 8))
        plt.pie(frequencias, labels=frequencias.index, autopct='%1.1f%%', startangle=90)
        plt.title(f'Proporção para {coluna}')
        plt.tight_layout()
        salvar_grafico(f'proporcao_{coluna}')


def analise_correlacao_cra_idade(dataframe):
    plt.figure(figsize=(8, 6))
    correlacao = dataframe[['CRA', 'IDADE']].corr()
    sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlação entre CRA e Idade')
    plt.tight_layout()
    salvar_grafico('correlacao_cra_idade')


if __name__ == "__main__":
    df = carregar_dados()
    analise_exploratoria(df)
