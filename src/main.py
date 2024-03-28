from scripts.formatacao_dados import formatar_e_classificar_dados
from scripts.analyses.analise_exploratoria import analise_exploratoria
from scripts.analyses.analise_temporal import analise_temporal
from scripts.analyses.analise_ingresso_evasao import analise_ingresso_evasao
from scripts.analyses.analise_performance_academica import analise_performance_academica
from scripts.gerar_relatorio import salvar_graficos_como_imagem


def main():
    df = formatar_e_classificar_dados()

    secoes = {
        "Análise Exploratória": [analise_exploratoria],
        "Análise Temporal": [analise_temporal],
        "Análise de Ingresso e Evasão": [analise_ingresso_evasao],
        "Análise de Performance Acadêmica": [analise_performance_academica]
    }

    salvar_graficos_como_imagem(secoes, df)


if __name__ == "__main__":
    main()
