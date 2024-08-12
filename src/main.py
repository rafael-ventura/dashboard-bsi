from src.scripts.analise_geografica import executar_analise_geografica
from src.scripts.analise_ingresso_evasao import analise_ingresso_evasao
from src.scripts.analise_performance_academica import analise_performance_academica
from src.scripts.formatacao_dados import formatar_dados


def main():
    """
    Função principal para execução das análises.
    """
    # Análise dos dados incluindo alunos antes de 2014
    df_geral = formatar_dados(r'C:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx', incluir_outros=False, dados_anterior_2014=True)

    # Realizar as análises
    print("Análise de dados gerais (incluindo pré-2014):")
    analise_ingresso_evasao(df_geral)
    analise_performance_academica(df_geral)
    executar_analise_geografica(df_geral)


if __name__ == "__main__":
    main()
