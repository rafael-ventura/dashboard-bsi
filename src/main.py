import os
import pandas as pd

from src.scripts.analise_geografica import analise_geografica
from src.scripts.analise_ingresso_evasao import analise_ingresso_evasao
from src.scripts.analise_desempenho_academico import analise_desempenho_academico
from src.scripts.analise_resultados_gerais import analise_resultados_gerais
from src.scripts.formatacao_dados import formatar_dados
from src.utils.plots import criar_pasta_graficos
from src.utils.utils import separar_por_periodo
from colorama import Fore, init, Style

init(autoreset=True)


def imprimir_informacoes_gerais(df_original, df_formatado):
    """
    Imprime informações gerais sobre o número de registros antes e depois da formatação, incluindo descartes.
    """
    # Contagem de registros originais
    total_original = len(df_original)

    # Contagem de registros formatados
    total_formatado = len(df_formatado)

    # Calculando registros descartados
    registros_descartados = total_original - total_formatado

    print(Fore.CYAN + f"Total de alunos no dataset original: {total_original}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total de alunos após a formatação: {total_formatado}" + Style.RESET_ALL)
    print(Fore.RED + f"Total de registros descartados no geral: {registros_descartados}" + Style.RESET_ALL)


def main():
    """
    Função principal para execução das análises.
    """
    init(autoreset=True)
    print(Fore.CYAN + "Iniciando o processo de formatação de dados...")

    # Carregar os dados diretamente da planilha antes de qualquer formatação
    caminho_planilha = r'C:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx'
    df_original = pd.read_excel(caminho_planilha)

    # Chamar a função de formatação e obter os dados formatados
    df_formatado = formatar_dados(caminho_planilha, incluir_outros=False, dados_anterior_2014=True)

    # Exibir informações gerais comparando o dataset original e o formatado
    imprimir_informacoes_gerais(df_original, df_formatado)

    # Separar os dados por período
    periodos = separar_por_periodo(df_formatado)

    for periodo, df_periodo in periodos.items():
        # Atualizar a pasta de destino para os gráficos
        nome_pasta = f'graficos/periodo_{periodo}'

        # Criar subpastas específicas para cada análise
        pasta_geografico = criar_pasta_graficos(os.path.join(nome_pasta, 'geografico'))
        pasta_performance = criar_pasta_graficos(os.path.join(nome_pasta, 'performance_academica'))
        pasta_ingresso_evasao = criar_pasta_graficos(os.path.join(nome_pasta, 'ingresso_evasao'))

        # Realizar as análises específicas para cada período
        print(Fore.GREEN + f"\nAnálise de dados para o período: {periodo}")
        analise_ingresso_evasao(df_periodo, pasta_ingresso_evasao, periodo)
        # analise_desempenho_academico(df_periodo, pasta_performance, periodo)
        # analise_geografica(df_periodo, pasta_geografico, periodo)

    # Analisar os resultados gerais
    pasta_resultados_gerais = criar_pasta_graficos('graficos/resultados_gerais')
    # analise_resultados_gerais(df_formatado, pasta_resultados_gerais)

    print(Fore.CYAN + "Processo de análise concluído!")


if __name__ == "__main__":
    main()
