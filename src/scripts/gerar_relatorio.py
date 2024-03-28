import matplotlib.pyplot as plt

def salvar_graficos_como_imagem(secoes, df, nome_do_arquivo="relatorio_graficos.png"):
    fig, axs = plt.subplots(len(secoes), 1, figsize=(10, len(secoes) * 6), sharex=True)

    for i, (secao, funcoes) in enumerate(secoes.items()):
        ax = axs[i]
        ax.set_title(secao)
        ax.set_xlabel('Eixo X')  # Adicione rótulos adequados aqui, se necessário
        ax.set_ylabel('Eixo Y')

        for funcao in funcoes:
            funcao(df, ax)

    plt.tight_layout()
    plt.savefig(nome_do_arquivo)
    plt.close()
