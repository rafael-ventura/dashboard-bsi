import os
from src.ingresso.AnaliseTipoIngresso import AnaliseTipoIngresso  # Nova análise
from src.formatacao.formatacao_dados import formatar_dados
from src.utils.plots import criar_pasta_graficos
from colorama import Fore, init, Style
from src.utils.utils import carregar_dados

init(autoreset=True)


def main(formatar_dados=True, considerar_curriculo_antigo=True):
    """
    Função principal para execução da análise de tipo de ingresso.
    :param formatar_dados: Flag para decidir se os dados serão formatados ou carregados do arquivo processado.
    :param considerar_curriculo_antigo: Flag para considerar alunos do currículo anterior a 2008/1 e posterior a 2023/2.
    """
    try:
        print(Fore.CYAN + "Iniciando o processo de análise..." + Style.RESET_ALL)
        caminho_planilha = r'R:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx'
        if not os.path.exists(caminho_planilha):
            raise FileNotFoundError(f"O arquivo '{caminho_planilha}' não foi encontrado.")

        try:
            if formatar_dados:
                print(Fore.CYAN + "Formatando os dados..." + Style.RESET_ALL)
                df_formatado = formatar_dados(caminho_planilha, incluir_outros=False, dados_anterior_2014=True)
                print(Fore.GREEN + "Dados formatados com sucesso!" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Pulando a formatação de dados. Carregando arquivo processado..." + Style.RESET_ALL)
                df_formatado = carregar_dados()

            # Filtro adicional: desconsiderar alunos do currículo antigo, se necessário
            if not considerar_curriculo_antigo:
                print(Fore.YELLOW + "Filtrando alunos do currículo antigo (antes de 2008/1 e depois de 2023/2)..." + Style.RESET_ALL)
                df_formatado = df_formatado[df_formatado['NUM_VERSAO'].isin(["2008/1", "2023/2"])]
                print(Fore.GREEN + f"Registros restantes após o filtro: {len(df_formatado)}" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao formatar ou carregar os dados: {e}" + Style.RESET_ALL)
            return

        # Executar as análises de tipo de ingresso
        pasta_tipo_ingresso = criar_pasta_graficos('graficos/tipo_ingresso')
        analise_tipo_ingresso = AnaliseTipoIngresso(df_formatado, pasta_tipo_ingresso)
        analise_tipo_ingresso.__init__(df_formatado, pasta_tipo_ingresso)
        print(Fore.CYAN + "Análise de tipo de ingresso concluída!" + Style.RESET_ALL)

    except FileNotFoundError as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ocorreu um erro inesperado: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main(formatar_dados=False, considerar_curriculo_antigo=False)
