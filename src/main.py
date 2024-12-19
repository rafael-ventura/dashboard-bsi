# src/scripts/main.py

import os
import pandas as pd
from src.scripts.analise_geografica import analise_geografica
from src.scripts.AnaliseIngressoEvasao import AnaliseIngressoEvasao
from src.scripts.analise_desempenho_academico import analise_desempenho_academico
from src.scripts.analise_resultados_gerais import analise_resultados_gerais
from src.scripts.formatacao_dados import formatar_dados
from src.utils.plots import criar_pasta_graficos
from src.utils.utils import separar_por_periodo
from src.utils.config_cores import ConfigCores
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
    try:
        print(Fore.CYAN + "Iniciando o processo de formatação de dados..." + Style.RESET_ALL)

        # Definir o caminho da planilha
        caminho_planilha = r'R:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx'

        # Verificar se o arquivo existe
        if not os.path.exists(caminho_planilha):
            raise FileNotFoundError(f"O arquivo '{caminho_planilha}' não foi encontrado.")

        # Carregar os dados
        df_original = pd.read_excel(caminho_planilha)

        # Chamar a função de formatação e obter os dados formatados
        df_formatado = formatar_dados(caminho_planilha, incluir_outros=False, dados_anterior_2014=True)

        # Exibir informações gerais comparando o dataset original e o formatado
        imprimir_informacoes_gerais(df_original, df_formatado)

        # Separar os dados por período
        periodos = separar_por_periodo(df_formatado)

        # Carregar as configurações de cores
        config_cores = ConfigCores()

        # Instanciar a classe de análise de ingresso e evasão
        pasta_ingresso_evasao = criar_pasta_graficos('graficos/ingresso_evasao')
        analise_ingresso_evasao = AnaliseIngressoEvasao(periodos, pasta_ingresso_evasao, config_cores=config_cores)

        # Executar as análises unificadas
        analise_ingresso_evasao.executar_analises()

        # # Analisar desempenho acadêmico
        # pasta_performance = criar_pasta_graficos('graficos/performance_academica')
        # analise_desempenho_academico(periodos, pasta_performance)
        #
        # # Analisar geográfica
        # pasta_geografico = criar_pasta_graficos('graficos/geografico')
        # analise_geografica(periodos, pasta_geografico)
        #
        # # Analisar resultados gerais
        # pasta_resultados_gerais = criar_pasta_graficos('graficos/resultados_gerais')
        # analise_resultados_gerais(df_formatado, pasta_resultados_gerais)

        print(Fore.CYAN + "Processo de análise concluído!" + Style.RESET_ALL)

    except FileNotFoundError as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ocorreu um erro inesperado: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
