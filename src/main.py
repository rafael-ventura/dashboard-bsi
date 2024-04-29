from src.scripts.analise_exploratoria import analise_exploratoria
from src.scripts.analise_ingresso_evasao import analise_ingresso_evasao
from src.scripts.analise_performance_academica import analise_performance_academica
from src.scripts.analise_temporal import analise_temporal
from scripts.formatacao_dados import formatar
from src.scripts.analise_geografica import executar_analise_geografica


def main():
    """
    Função principal para execução das análises.
    """
    df = formatar(incluir_outros=False, dados_anterior_2013=True)

    analise_exploratoria(df)
    analise_temporal(df)
    analise_ingresso_evasao(df)
    analise_performance_academica(df)
    executar_analise_geografica(df)


if __name__ == "__main__":
    main()
