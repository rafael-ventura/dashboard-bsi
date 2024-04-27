from src.utils import criar_grafico_de_contagem, plotar_histograma, criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_ingresso_evasao(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise de Ingresso e Evasão...")

    plot_distribuicao_ingresso(dataframe)
    plot_evasao_sexo(dataframe)
    plot_evasao_idade(dataframe)

    print("\nAnálise de Ingresso e Evasão Concluída!")


def plot_distribuicao_ingresso(dataframe):
    """
    Função para plotar a distribuição de cotistas e não-cotistas.
    :param dataframe: DataFrame com os dados
    :return: None
    """
    criar_grafico_de_contagem(x='FORMA_INGRESSO_SIMPLES', data=dataframe,
                              titulo='Distribuição de Cotistas e Não-Cotistas',
                              xlabel='Forma de Ingresso', ylabel='Quantidade')
    salvar_grafico('distribuicao_ingresso')


def plot_evasao_sexo(dataframe):
    """
    Função para plotar a distribuição de evasões por sexo.
    :param dataframe: DataFrame com os dados
    :return: None
    """
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe, hue='SEXO', titulo='Distribuição de Evasões por Sexo',
                              xlabel='Forma de Evasão', ylabel='Quantidade')
    salvar_grafico('evasao_sexo')


def plot_evasao_idade(dataframe):
    """
    Função para plotar a distribuição de evasões por idade.
    :param dataframe: DataFrame com os dados
    :return: None
    """
    plotar_histograma(x=dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']['IDADE_INGRESSO'], data=dataframe,
                      titulo='Distribuição de Idades dos Alunos com Evasão', xlabel='Idade', ylabel='Quantidade')
    salvar_grafico('evasao_idade')


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df)
