import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.plots import criar_pasta_graficos, salvar_grafico
from src.utils.utils import carregar_dados


def analise_exploratoria(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise Exploratória...")

    # Plotagem de distribuições
    plot_distribuicao_sexo(dataframe)
    plot_distribuicao_idade(dataframe)

    # Análises estatísticas
    estatisticas_descritivas(dataframe)

    # Análises de frequência
    plot_tabela_frequencia(dataframe, 'SEXO')
    plot_tabela_frequencia(dataframe, 'FORMA_INGRESSO_SIMPLES')
    plot_tabela_frequencia(dataframe, 'STATUS_EVASAO')

    print("\nAnálise Exploratória Concluída!")


def estatisticas_descritivas(dataframe):
    print("\nEstatísticas Descritivas referentes a Idade:")
    print("Mínimo de Idade:", dataframe['IDADE_INGRESSO'].min())
    print("Máximo de Idade:", dataframe['IDADE_INGRESSO'].max())
    print("Média de Idade:", dataframe['IDADE_INGRESSO'].mean())
    print("Mediana de Idade:", dataframe['IDADE_INGRESSO'].median())
    print("Desvio Padrão de Idade:", dataframe['IDADE_INGRESSO'].std())
    print("Moda de Idade:", dataframe['IDADE_INGRESSO'].mode())

    print("\nEstatísticas Descritivas referentes a CRA:")
    print("Mínimo de CRA:", dataframe['CRA'].min())
    print("Máximo de CRA:", dataframe['CRA'].max())
    print("Média de CRA:", dataframe['CRA'].mean())
    print("Mediana de CRA:", dataframe['CRA'].median())
    print("Desvio Padrão de CRA:", dataframe['CRA'].std())
    print("Moda de CRA:", dataframe['CRA'].mode())

    print("\nEstatísticas Descritivas referentes a Forma de Ingresso:")
    print(dataframe['FORMA_INGRESSO_SIMPLES'].value_counts())
    print("\n Maior CRA por Forma de Ingresso:")
    print(dataframe.groupby('FORMA_INGRESSO_SIMPLES')['CRA'].max())
    print("\n Menor CRA por Forma de Ingresso:")
    print(dataframe.groupby('FORMA_INGRESSO_SIMPLES')['CRA'].min())
    print("\n Média de CRA por Forma de Ingresso:")
    print(dataframe.groupby('FORMA_INGRESSO_SIMPLES')['CRA'].mean())
    print("\n Mediana de CRA por Forma de Ingresso:")
    print(dataframe.groupby('FORMA_INGRESSO_SIMPLES')['CRA'].median())

    print("\nEstatísticas Descritivas referentes a Status de Evasão:")
    print(dataframe['STATUS_EVASAO'].value_counts())
    print("\n Maior CRA por Status de Evasão:")
    print(dataframe.groupby('STATUS_EVASAO')['CRA'].max())
    print("\n Menor CRA por Status de Evasão:")
    print(dataframe.groupby('STATUS_EVASAO')['CRA'].min())
    print("\n Média de CRA por Status de Evasão:")
    print(dataframe.groupby('STATUS_EVASAO')['CRA'].mean())
    print("\n Mediana de CRA por Status de Evasão:")
    print(dataframe.groupby('STATUS_EVASAO')['CRA'].median())

    print("\nEstatísticas Descritivas referentes a Sexo:")
    print(dataframe['SEXO'].value_counts())
    print("\n Maior CRA por Sexo:")
    print(dataframe.groupby('SEXO')['CRA'].max())
    print("\n Menor CRA por Sexo:")
    print(dataframe.groupby('SEXO')['CRA'].min())
    print("\n Média de CRA por Sexo:")
    print(dataframe.groupby('SEXO')['CRA'].mean())
    print("\n Mediana de CRA por Sexo:")
    print(dataframe.groupby('SEXO')['CRA'].median())

    print("\nEstatísticas Descritivas referentes a Distância:")
    print("Mínimo de Distância:", dataframe['DISTANCIA_URCA'].min())
    print("Máximo de Distância:", dataframe['DISTANCIA_URCA'].max())
    print("Média de Distância:", dataframe['DISTANCIA_URCA'].mean())
    print("Mediana de Distância:", dataframe['DISTANCIA_URCA'].median())
    print("Desvio Padrão de Distância:", dataframe['DISTANCIA_URCA'].std())
    print("Moda de Distância:", dataframe['DISTANCIA_URCA'].mode())
    print("\n Maior CRA por Distância:")
    print(dataframe.groupby('DISTANCIA_URCA')['CRA'].max())
    print("\n Menor CRA por Distância:")
    print(dataframe.groupby('DISTANCIA_URCA')['CRA'].min())
    print("\n Média de CRA por Distância:")
    print(dataframe.groupby('DISTANCIA_URCA')['CRA'].mean())
    print("\n As 5 medias mais altas moram a uma distância de:")
    print(dataframe.groupby('DISTANCIA_URCA')['CRA'].mean().nlargest(5))
    print("\n As 5 medias mais baixas moram a uma distância de:")
    print(dataframe.groupby('DISTANCIA_URCA')['CRA'].mean().nsmallest(5))

    print("\nEstatísticas Descritivas referentes Bairros, Cidades e Estados:")
    print("Quantidade de Alunos:", dataframe.shape[0])
    print("Quantidade de Bairros:", dataframe['BAIRRO'].nunique())
    print("Quantidade de Cidades:", dataframe['CIDADE'].nunique())
    print("Quantidade de Estados:", dataframe['ESTADO'].nunique())
    # print("Quantidade de Zonas:", dataframe['ZONA'].nunique())
    print("Bairros com mais de 5 alunos:",
          dataframe['BAIRRO'].value_counts()[dataframe['BAIRRO'].value_counts() > 5].count())
    print("Cidades com mais de 5 alunos:",
          dataframe['CIDADE'].value_counts()[dataframe['CIDADE'].value_counts() > 5].count())
    print("Estados com mais de 3 alunos:",
          dataframe['ESTADO'].value_counts()[dataframe['ESTADO'].value_counts() > 5].count())
    print("\n Maior CRA por Bairro:")
    print(dataframe.groupby('BAIRRO')['CRA'].max())
    print("\n Menor CRA por Bairro:")
    print(dataframe.groupby('BAIRRO')['CRA'].min())
    print("\n Média de CRA por Bairro:")
    print(dataframe.groupby('BAIRRO')['CRA'].mean())
    print("\n Mediana de CRA por Bairro:")
    print(dataframe.groupby('BAIRRO')['CRA'].median())
    print("\n Maior CRA por Cidade:")
    print(dataframe.groupby('CIDADE')['CRA'].max())
    print("\n Menor CRA por Cidade:")
    print(dataframe.groupby('CIDADE')['CRA'].min())
    print("\n Média de CRA por Cidade:")
    print(dataframe.groupby('CIDADE')['CRA'].mean())

    print("\n Maior CRA por Estado:")
    print(dataframe.groupby('ESTADO')['CRA'].max())
    print("\n Menor CRA por Estado:")
    print(dataframe.groupby('ESTADO')['CRA'].min())
    print("\n Média de CRA por Estado:")
    print(dataframe.groupby('ESTADO')['CRA'].mean())

    print("\n As 5 maiores médias de CRA por Bairro:")
    print(dataframe.groupby('BAIRRO')['CRA'].mean().nlargest(5))
    print("\n As 5 maiores médias de CRA por Cidade:")
    print(dataframe.groupby('CIDADE')['CRA'].mean().nlargest(5))
    print("As 5 maiores médias de CRA por Estado:")
    print(dataframe.groupby('ESTADO')['CRA'].mean().nlargest(5))

    print("\n As 5 menores médias de CRA por Bairro:")
    print(dataframe.groupby('BAIRRO')['CRA'].mean().nsmallest(5))
    print("\n As 5 menores médias de CRA por Cidade:")
    print(dataframe.groupby('CIDADE')['CRA'].mean().nsmallest(5))
    print("As 5 menores médias de CRA por Estado:")
    print(dataframe.groupby('ESTADO')['CRA'].mean().nsmallest(5))

    # print("\n Maior CRA por Zona:")
    # print(dataframe.groupby('ZONA')['CRA'].max())
    # print("\n Menor CRA por Zona:")
    # print(dataframe.groupby('ZONA')['CRA'].min())
    # print("\n Média de CRA por Zona:")
    # print(dataframe.groupby('ZONA')['CRA'].mean())


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
        sns.histplot(dataframe['IDADE_INGRESSO'], kde=True, color="darkorange")
        plt.title('Distribuição por Idade')
        plt.xlabel('Idade')
        plt.ylabel('Quantidade')
        salvar_grafico('distribuicao_idade')
    else:
        print("A coluna 'IDADE' não existe no DataFrame.")


def plot_tabela_frequencia(dataframe, coluna):
    frequencias = dataframe[coluna].value_counts()
    print(frequencias)

    plt.figure(figsize=(8, 8))
    plt.pie(frequencias, labels=frequencias.index, autopct='%1.1f%%', startangle=90)
    plt.title('Frequências Relativas para {}'.format(coluna))
    plt.tight_layout()
    salvar_grafico('frequencias_relativas_{}'.format(coluna))


if __name__ == "__main__":
    df = carregar_dados()
    analise_exploratoria(df)
