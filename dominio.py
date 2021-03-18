import requests
import re

class Canal:
    def __init__(self, nome, url):
        self.nome = nome
        self.url = url
        self.dados_brutos = self.pega_dados_brutos(url)
        self.dados_tratados = self.trata_dados(self.dados_brutos)
        self.tempo_em_dias = self.pega_tempo(self.dados_tratados)
        self.lista_visualizacoes = self.pega_visualizacoes(self.dados_tratados)
        self.dicionario = self.gera_dicionario(self.lista_visualizacoes, self.tempo_em_dias)
        self.numero_de_videos_no_periodo = self.pega_numero_de_videos_no_periodo(self.dicionario)
        self.visualizacoes_no_periodo = self.pega_visualizacoes_no_periodo(self.dicionario)
        self.media = self.gera_media(self.visualizacoes_no_periodo, self.numero_de_videos_no_periodo)

    def __str__(self):
        return f'Canal: {self.nome}\n'\
                f'{self.numero_de_videos_no_periodo} Vídeos nos últimos {self.retorna_periodo_de_busca()} dias.\n' \
                f'{self.visualizacoes_no_periodo}  Total de visualizações no período \n' \
                f'{self.media}  Média de visualizações por vídeo\n' \
                f'R${self.gera_valor_medio_do_anuncio_por_video(self.media)} Valor médio do anúncio por vídeo\n' \
                f'R${self.gera_valor_medio_do_anuncio_no_periodo(self.visualizacoes_no_periodo)} Valor médio do anúncio no período' \


    def pega_dados_brutos(self, url):
        dados_brutos = requests.get(url).text
        return dados_brutos

    def trata_dados(self, dados_brutos):
        padrao = self.retorna_padrao_regex
        texto_primeiro_tratamento = re.findall(padrao, dados_brutos)
        texto_segundo_tratamento = []
        for trecho in texto_primeiro_tratamento:
            trecho = str(trecho).replace("accessibilityData\":{\"label\":\"", "")
            trecho = str(trecho).replace("\"}}}", "")
            texto_segundo_tratamento.append(trecho)

        return texto_segundo_tratamento

    def pega_tempo(self, dados_tratados):
        lista_dados_tratados = dados_tratados
        lista_tempo = []
        for trecho in lista_dados_tratados:
            indice_tempo_comeco = trecho.find("há") + 3
            indice_tempo_fim = trecho.find("minutos") - 3
            tempo = trecho[indice_tempo_comeco:indice_tempo_fim]
            tempo = tempo.replace("meses", "30")
            tempo = tempo.replace("mês", "30")
            tempo = tempo.replace("semanas", "7")
            tempo = tempo.replace("semana", "7")
            tempo = tempo.replace("dias", "1")
            tempo = tempo.replace("dia", "1")
            tempo = tempo.replace("horas", "0")
            tempo = tempo.replace("hora", "0")
            lista_de_separacao_tempo = tempo.split()
            tempo_em_dias = int(lista_de_separacao_tempo[0]) * int(lista_de_separacao_tempo[1])
            lista_tempo.append(tempo_em_dias)
        return lista_tempo

    def pega_visualizacoes(self, dados_tratados):
        lista_visualizacoes = []
        for trecho in dados_tratados:
            if "segundos" in trecho:
                indice_visualizacoes_comeco = trecho.rfind("segundos") + len("segundos")
            elif "segundo" in trecho:
                indice_visualizacoes_comeco = trecho.rfind("segundo") + len("segundo")
            elif "minutos" in trecho:
                indice_visualizacoes_comeco = trecho.rfind("minutos") + len("minutos")
            elif "minuto" in trecho:
                indice_visualizacoes_comeco = trecho.rfind("minuto") + len("minuto")
            elif "horas" in trecho:
                indice_visualizacoes_comeco = trecho.rfind("horas") + len("horas")
            else:
                indice_visualizacoes_comeco = trecho.rfind("hora") + len("hora")
            indice_visualizacoes_fim = trecho.rfind("visualizações")
            visualizacoes = trecho[indice_visualizacoes_comeco:indice_visualizacoes_fim]
            visualizacoes = visualizacoes.replace(".", "")
            visualizacoes = int(visualizacoes)
            lista_visualizacoes.append(visualizacoes)
        return lista_visualizacoes

    def gera_dicionario(self, visualizacoes, tempo_em_dias):
        index = len(visualizacoes)
        dicionario = {}
        for i in range(0, index):
            dicionario[visualizacoes[i]] = tempo_em_dias[i]
        return dicionario

    def pega_numero_de_videos_no_periodo(self, dicionario):
        numero_de_videos = 0
        periodo_para_busca_em_dias = self.retorna_periodo_de_busca()
        for elemento in dicionario.keys():
            if dicionario[elemento] <= periodo_para_busca_em_dias:
                numero_de_videos += 1

        return numero_de_videos

    def pega_visualizacoes_no_periodo(self, dicionario):
        total_de_visualizacoes_no_periodo = 0
        periodo_para_busca_em_dias = self.retorna_periodo_de_busca()
        for elemento in dicionario.keys():
            if dicionario[elemento] <= periodo_para_busca_em_dias:
                total_de_visualizacoes_no_periodo += elemento

        return total_de_visualizacoes_no_periodo

    def gera_media(self, visualizacoes_no_periodo, numero_de_videos):
        media = visualizacoes_no_periodo/numero_de_videos
        media = round(media)
        return media

    def gera_valor_medio_do_anuncio_por_video(self, media):
        valor_medio_do_anuncio = self.retorna_valor_do_anuncio_por_visualizacao() * media
        valor_medio_do_anuncio = round(valor_medio_do_anuncio, 2)
        return valor_medio_do_anuncio

    def gera_valor_medio_do_anuncio_no_periodo(self, visualizacoes_no_periodo):
        valor_medio_do_anuncio = self.retorna_valor_do_anuncio_por_visualizacao() * visualizacoes_no_periodo
        valor_medio_do_anuncio = round(valor_medio_do_anuncio, 2)
        return valor_medio_do_anuncio

    @property
    def retorna_padrao_regex(self):
        padrao = "accessibilityData\":{\"label\":\"[\w \s \S \W]{1,400}visualizações\"}}}"
        return padrao


    def retorna_periodo_de_busca(self):
        periodo_em_dias = 10
        return periodo_em_dias

    def retorna_valor_do_anuncio_por_visualizacao(self):
        valor_do_anuncio = 0.01
        return valor_do_anuncio