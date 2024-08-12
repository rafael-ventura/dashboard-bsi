import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, Style, init
from src.utils.plots import criar_pasta_graficos, criar_grafico_de_contagem, salvar_grafico, plotar_histograma
from src.utils.utils import carregar_dados

# Inicializa o Colorama
init(autoreset=True)

def analise_ingresso_evasao(dataframe):
    criar_pasta_graficos()
    print(Fore.BLUE + "\nIniciando Análise de Ingresso e Evasão...")

    exibir_diferenca_media_tempo_termino(dataframe)
    exibir_porcentagem_concluidos_evasao_cursando(dataframe)
    exibir_porcentagem_bairros_evasao_concluidos(dataframe)

    plot_media_cra_evasao(dataframe)
    plot_distribuicao_ingresso(dataframe)
    plot_evasao_sexo(dataframe)
    plot_evasao_idade(dataframe)

    print(Fore.GREEN + "\nAnálise de Ingresso e Evasão Concluída!")


def exibir_diferenca_media_tempo_termino(dataframe):
    # Filtra os alunos que já concluíram o curso
    concluidos = dataframe[dataframe['STATUS_EVASAO'] == 'Concluído']

    # Calcula a média do tempo de conclusão para cotistas e não cotistas
    media_tempo_cotista = concluidos[concluidos['FORMA_INGRESSO_SIMPLES'] == 'Cotista']['TEMPO_CURSO'].mean()
    media_tempo_nao_cotista = concluidos[concluidos['FORMA_INGRESSO_SIMPLES'] == 'Não Cotista']['TEMPO_CURSO'].mean()

    # Exibe a diferença de forma visual
    print(Fore.CYAN + "Diferença de tempo de término entre Cotistas e Não Cotistas:")
    print(f"Cotistas: {media_tempo_cotista:.2f} períodos")
    print(f"Não Cotistas: {media_tempo_nao_cotista:.2f} períodos")
    print(Fore.YELLOW + f"Diferença: {abs(media_tempo_cotista - media_tempo_nao_cotista):.2f} períodos\n")


def exibir_porcentagem_concluidos_evasao_cursando(dataframe):
    # Calcula a porcentagem de alunos que concluíram, evadiram e estão cursando para cotistas e não cotistas
    total_cotistas = dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotista'].shape[0]
    total_nao_cotistas = dataframe[dataframe['FORMA_INGRESSO_SIMPLES'] == 'Não Cotista'].shape[0]

    porcentagem_cotistas_concluidos = dataframe[(dataframe['STATUS_EVASAO'] == 'Concluído') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotista')].shape[0] / total_cotistas * 100
    porcentagem_cotistas_evasao = dataframe[(dataframe['STATUS_EVASAO'] == 'Evasão') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotista')].shape[0] / total_cotistas * 100
    porcentagem_cotistas_cursando = dataframe[(dataframe['STATUS_EVASAO'] == 'Cursando') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Cotista')].shape[0] / total_cotistas * 100

    porcentagem_nao_cotistas_concluidos = dataframe[(dataframe['STATUS_EVASAO'] == 'Concluído') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Não Cotista')].shape[0] / total_nao_cotistas * 100
    porcentagem_nao_cotistas_evasao = dataframe[(dataframe['STATUS_EVASAO'] == 'Evasão') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Não Cotista')].shape[0] / total_nao_cotistas * 100
    porcentagem_nao_cotistas_cursando = dataframe[(dataframe['STATUS_EVASAO'] == 'Cursando') & (dataframe['FORMA_INGRESSO_SIMPLES'] == 'Não Cotista')].shape[0] / total_nao_cotistas * 100

    # Exibe os resultados
    print(Fore.MAGENTA + "Porcentagem de alunos Cotistas:")
    print(f"Concluídos: {porcentagem_cotistas_concluidos:.2f}%")
    print(f"Evasão: {porcentagem_cotistas_evasao:.2f}%")
    print(f"Cursando: {porcentagem_cotistas_cursando:.2f}%\n")

    print(Fore.MAGENTA + "Porcentagem de alunos Não Cotistas:")
    print(f"Concluídos: {porcentagem_nao_cotistas_concluidos:.2f}%")
    print(f"Evasão: {porcentagem_nao_cotistas_evasao:.2f}%")
    print(f"Cursando: {porcentagem_nao_cotistas_cursando:.2f}%\n")


def exibir_porcentagem_bairros_evasao_concluidos(dataframe):
    # Filtra os dados para alunos que concluíram e evadiram
    concluidos = dataframe[dataframe['STATUS_EVASAO'] == 'Concluído']
    evadidos = dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']

    # Calcula a porcentagem dos 5 bairros com mais alunos concluídos e evadidos
    top_bairros_concluidos = concluidos['BAIRRO'].value_counts(normalize=True).head(5) * 100
    top_bairros_evasao = evadidos['BAIRRO'].value_counts(normalize=True).head(5) * 100

    # Exibe os resultados
    print(Fore.LIGHTBLUE_EX + "Top 5 Bairros com mais alunos Concluídos:")
    for bairro, porcentagem in top_bairros_concluidos.items():
        print(f"{bairro}: {porcentagem:.2f}%")

    print("\n" + Fore.LIGHTBLUE_EX + "Top 5 Bairros com mais alunos Evadidos:")
    for bairro, porcentagem in top_bairros_evasao.items():
        print(f"{bairro}: {porcentagem:.2f}%")


def plot_media_cra_evasao(dataframe):
    if 'STATUS_EVASAO' in dataframe.columns and 'CRA' in dataframe.columns:
        plt.figure(figsize=(10, 6))
        media_cra = dataframe.groupby('STATUS_EVASAO')['CRA'].mean().reset_index()
        sns.barplot(x='STATUS_EVASAO', y='CRA', data=media_cra)
        plt.title('Média do CRA por Forma de Evasão')
        plt.xlabel('Forma de Evasão')
        plt.ylabel('Média do CRA')
        plt.xticks(rotation=45)
        plt.tight_layout()
        salvar_grafico('media_cra_evasao')
    else:
        print("A coluna 'STATUS_EVASAO' ou 'CRA' não existe no DataFrame.")


def plot_distribuicao_ingresso(dataframe):
    criar_grafico_de_contagem(x='FORMA_INGRESSO_SIMPLES', data=dataframe,
                              titulo='Distribuição de Cotistas e Não-Cotistas',
                              xlabel='Forma de Ingresso', ylabel='Quantidade')
    salvar_grafico('distribuicao_ingresso')


def plot_evasao_sexo(dataframe):
    criar_grafico_de_contagem(x='STATUS_EVASAO', data=dataframe, hue='SEXO', titulo='Distribuição de Evasões por Sexo',
                              xlabel='Forma de Evasão', ylabel='Quantidade')
    salvar_grafico('evasao_sexo')


def plot_evasao_idade(dataframe):
    plotar_histograma(x=dataframe[dataframe['STATUS_EVASAO'] == 'Evasão']['IDADE_INGRESSO'], data=dataframe,
                      titulo='Distribuição de Idades dos Alunos com Evasão', xlabel='Idade', ylabel='Quantidade')
    salvar_grafico('evasao_idade')


if __name__ == "__main__":
    df = carregar_dados()
    analise_ingresso_evasao(df)
