from src.scripts.analyses.analise_exploratoria import realizar_analise_exploratoria
from src.scripts.formatacao_dados import formatar_e_classificar_dados


def main():
    try:
        print("Iniciando formatação e classificação dos dados...")
        df = formatar_e_classificar_dados()

        print("Iniciando análise exploratória...")
        realizar_analise_exploratoria(df)

        print("Iniciando análise temporal...")
        analise_temporal(df)

        print("Iniciando análise de categorias...")
        analise_categoria(df)

        print("Iniciando análise específica...")
        analise_especifica(df)

    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()
