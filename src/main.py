import os

from src.scripts.analise_geografica import analise_geografica
from src.scripts.analise_ingresso_evasao import analise_ingresso_evasao
from src.scripts.analise_desempenho_academico import analise_desempenho_academico
from src.scripts.analise_resultados_gerais import analise_resultados_gerais
from src.scripts.formatacao_dados import formatar_dados
from src.utils.plots import criar_pasta_graficos
from src.utils.utils import separar_por_periodo
from colorama import Fore, init


def main():
    """
    Função principal para execução das análises.
    """
    init(autoreset=True)
    print(Fore.CYAN + "Iniciando o processo de formatação de dados...")
    df_geral = formatar_dados(r'C:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx', incluir_outros=False, dados_anterior_2014=True)

    # Separar os dados por período
    periodos = separar_por_periodo(df_geral)

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
        analise_desempenho_academico(df_periodo, pasta_performance, periodo)
        analise_geografica(df_periodo, pasta_geografico, periodo)

    # Analisar os resultados gerais
    pasta_resultados_gerais = criar_pasta_graficos('graficos/resultados_gerais')
    analise_resultados_gerais(df_geral, pasta_resultados_gerais)

    print(Fore.CYAN + "Processo de análise concluído!")


if __name__ == "__main__":
    main()
