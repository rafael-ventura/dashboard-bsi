from src.utils import plot_countplot, plot_histplot, criar_pasta_graficos, salvar_grafico, carregar_dados

def analise_ingresso_evasao(df):
    criar_pasta_graficos()
    print("\nIniciando Análise de Ingresso e Evasão...")

    plot_distribuicao_ingresso(df)
    plot_evasao_sexo(df)
    plot_evasao_idade(df)

    print("\nAnálise de Ingresso e Evasão Concluída!")

def plot_distribuicao_ingresso(df):
    # Usar função plot_countplot do utils.py
    plot_countplot(x='FORMA_INGRESSO_SIMPLES', data=df, titulo='Distribuição de Cotistas e Não-Cotistas', xlabel='Forma de Ingresso', ylabel='Quantidade')
    salvar_grafico('distribuicao_ingresso')

def plot_evasao_sexo(df):
    # Usar função plot_countplot do utils.py com o parâmetro hue
    plot_countplot(x='STATUS_EVASAO', data=df, hue='SEXO', titulo='Distribuição de Evasões por Sexo', xlabel='Forma de Evasão', ylabel='Quantidade')
    salvar_grafico('evasao_sexo')

def plot_evasao_idade(df):
    # Usar função plot_histplot do utils.py
    plot_histplot(x=df[df['STATUS_EVASAO'] == 'Evasão']['IDADE'], data=df, titulo='Distribuição de Idades dos Alunos com Evasão', xlabel='Idade', ylabel='Quantidade')
    salvar_grafico('evasao_idade')

if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df)
