from scripts.analyses.analise_exploratoria import analise_exploratoria
from scripts.analyses.analise_ingresso_evasao import analise_ingresso_evasao
from scripts.analyses.analise_performance_academica import analise_performance_academica
from scripts.analyses.analise_temporal import analise_temporal
from scripts.formatacao_dados import formatar


def main():
    df = formatar()

    analise_exploratoria(df)
    analise_temporal(df)
    analise_ingresso_evasao(df)
    analise_performance_academica(df)


if __name__ == "__main__":
    main()
