# src/utils/config_cores.py

import seaborn as sns
import matplotlib.colors as mcolors
import numpy as np


def lighten_color(color, amount=0.3):
    """
    Clareia a cor recebida.
    :param color: Cor em formato hex ou reconhecido pelo matplotlib.
    :param amount: Quanto clarear (0 a 1).
    :return: Cor clara em formato hex.
    """
    try:
        c = mcolors.cnames[color]
    except:
        c = color
    c = np.array(mcolors.to_rgb(c))
    white = np.array([1, 1, 1])
    return mcolors.to_hex((1 - amount) * c + amount * white)


def darken_color(color, amount=0.3):
    """
    Escurece a cor recebida.
    :param color: Cor em formato hex ou reconhecido pelo matplotlib.
    :param amount: Quanto escurecer (0 a 1).
    :return: Cor escura em formato hex.
    """
    try:
        c = mcolors.cnames[color]
    except:
        c = color
    c = np.array(mcolors.to_rgb(c))
    black = np.array([0, 0, 0])
    return mcolors.to_hex((1 - amount) * c + amount * black)


class ConfigCores:
    def __init__(self):
        pass

    def get_cores_periodos(self):
        """
        Define uma paleta de cores para os períodos temporais.
        """
        return {
            'Antes Cotas': '#1f77b4',  # Azul
            'Cotas 2014-2020': '#ff7f0e',  # Laranja
            'Pandemia': '#2ca02c',  # Verde
            'Pos Pandemia': '#d62728',  # Vermelho
            'Outro': '#9467bd'  # Roxo
        }

    def get_cores_forma_ingresso(self):
        """
        Define uma paleta de cores para as formas de ingresso.
        """
        return {
            'Cotas': '#17becf',  # Azul Claro
            'Ampla Concorrencia': '#bcbd22',  # Verde Oliva
            'Geral': '#8c564b'  # Marrom
        }

    def get_cores_grupo(self):
        """
        Define uma paleta de cores para os grupos (Cotistas vs Não Cotistas).
        """
        return {
            'Cotistas': '#1f77b4',  # Azul
            'Não Cotistas': '#ff7f0e'  # Laranja
        }

    def get_cores_forma_evasao(self):
        """
        Define uma paleta de cores para os diferentes tipos de evasão detalhada.
        """
        return {
            'DES': '#d62728',  # Vermelho
            'CAN': '#2ca02c',  # Verde
            'JUB': '#9467bd',  # Roxo
            'TIC': '#8c564b',  # Marrom
            'FAL': '#e377c2',  # Rosa
            'ABA': '#7f7f7f'  # Cinza para categorias inesperadas
        }

    def get_cores_status_evasao(self):
        """
        Define uma paleta de cores para os diferentes status de evasão.
        """
        return {
            'Cursando': '#1f77b4',  # Azul
            'Evasão': '#d62728',  # Vermelho
            'Concluído': '#2ca02c',  # Verde
            'Outro': '#7f7f7f'  # Cinza para categorias inesperadas
        }

    def get_cores_sexo_periodo(self):
        """
        Define uma paleta de cores para comparar sexos em cada período temporal.
        Cada período terá duas tonalidades (clara e escura) para os sexos.
        """
        cores_periodos = self.get_cores_periodos()
        cores_sexo = {}

        for periodo, cor in cores_periodos.items():
            # Gerar tonalidades claras e escuras
            clara = lighten_color(cor, 0.3)
            escura = darken_color(cor, 0.3)
            cores_sexo[f'{periodo} - Masculino'] = clara
            cores_sexo[f'{periodo} - Feminino'] = escura

        return cores_sexo

    def get_cores_forma_ingresso_periodo(self):
        """
        Define uma paleta de cores para comparar formas de ingresso em cada período temporal.
        Cada período terá duas tonalidades (clara e escura) para as formas de ingresso.
        """
        cores_periodos = self.get_cores_periodos()
        cores_ingresso = {}

        for periodo, cor in cores_periodos.items():
            # Gerar tonalidades claras e escuras
            clara = lighten_color(cor, 0.3)
            escura = darken_color(cor, 0.3)
            cores_ingresso[f'{periodo} - Cotistas'] = clara
            cores_ingresso[f'{periodo} - Ampla Concorrencia'] = escura

        return cores_ingresso
