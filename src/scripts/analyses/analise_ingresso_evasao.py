from src.utils import plot_countplot, plot_histplot, criar_pasta_graficos, salvar_grafico, carregar_dados


def analise_ingresso_evasao(dataframe):
    criar_pasta_graficos()
    print("\nIniciando Análise de Ingresso e Evasão...")

    plot_distribuicao_ingresso(dataframe)
    plot_evasao_sexo(dataframe)
    plot_evasao_idade(dataframe)

    print("\nAnálise de Ingresso e Evasão Concluída!")


def plot_distribuicao_ingresso(dataframe):
    # Usar função plot_countplot do utils.py
    plot_countplot(x='FORMA_INGRESSO_SIMPLES', data=dataframe, titulo='Distribuição de Cotistas e Não-Cotistas',
                   xlabel='Forma de Ingresso', ylabel='Quantidade')
    salvar_grafico('distribuicao_ingresso')


def plot_evasao_sexo(dataframe):
    # Usar função plot_countplot do utils.py com o parâmetro hue
    plot_countplot(x='STATUS_EVASAO', data=dataframe, hue='SEXO', titulo='Distribuição de Evasões por Sexo',
                   xlabel='Forma de Evasão', ylabel='Quantidade')
    salvar_grafico('evasao_sexo')


def plot_evasao_idade(dataframe):
    # Usar função plot_histplot do utils.py
    plot_histplot(x=dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']['IDADE'], data=dataframe,
                  titulo='Distribuição de Idades dos Alunos com Evasão', xlabel='Idade', ylabel='Quantidade')
    salvar_grafico('evasao_idade')


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df)
