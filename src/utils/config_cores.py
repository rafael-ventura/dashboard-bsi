# src/utils/config_cores.py

import seaborn as sns

class ConfigCores:
    def __init__(self):
        pass

    def get_cores_periodos(self):
        """
        Define uma paleta de cores para os períodos temporais.
        """
        return {
            'Antes Cotas': '#1f77b4',        # Azul
            'Cotas 2014-2020': '#ff7f0e',    # Laranja
            'Pandemia': '#2ca02c',           # Verde
            'Pos Pandemia': '#d62728',       # Vermelho
            'Outro': '#9467bd'                # Roxo
        }

    def get_cores_forma_ingresso(self):
        """
        Define uma paleta de cores para as formas de ingresso.
        """
        return {
            'Cotas': '#17becf',               # Azul Claro
            'Ampla Concorrencia': '#bcbd22',  # Verde Oliva
            'Geral': '#8c564b'                 # Marrom
        }

    def get_cores_grupo(self):
        """
        Define uma paleta de cores para os grupos (Cotistas vs Não Cotistas).
        """
        return {
            'Cotistas': '#1f77b4',            # Azul
            'Não Cotistas': '#ff7f0e'         # Laranja
        }

    def get_cores_forma_evasao(self):
        """
        Define uma paleta de cores para os diferentes tipos de evasão simples.
        """
        return {
            'DES': '#d62728',  # Vermelho
            'CAN': '#2ca02c',  # Verde
            'JUB': '#9467bd',  # Roxo
            'TIC': '#8c564b',  # Marrom
            'FAL': '#e377c2'   # Rosa
        }
