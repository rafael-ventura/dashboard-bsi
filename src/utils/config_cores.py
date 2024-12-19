# src/utils/config_cores.py

class ConfigCores:
    """
    Classe responsável por armazenar as configurações de cores para os gráficos.
    """

    # Paleta de cores para os períodos temporais
    cores_periodos = {
        'Antes Cotas': '#1f77b4',       # Azul
        'Cotas 2014-2020': '#ff7f0e',    # Laranja
        'Pandemia': '#2ca02c',           # Verde
        'Pos Pandemia': '#d62728'        # Vermelho
    }

    # Paleta de cores para as formas de ingresso
    cores_forma_ingresso = {
        'Ampla Concorrencia': '#9467bd', # Roxo
        'Cotas': '#8c564b'                # Marrom
    }

    @staticmethod
    def get_cores_periodos():
        return ConfigCores.cores_periodos

    @staticmethod
    def get_cores_forma_ingresso():
        return ConfigCores.cores_forma_ingresso
