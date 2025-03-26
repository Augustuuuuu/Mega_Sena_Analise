import re
from collections import Counter
import os
from datetime import datetime

class QAMegaSena:
    def __init__(self):
        self.jogos = []  # Lista para armazenar todos os jogos
        self.numeros_frequencia = {}  # Dicionário para armazenar a frequência dos números
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do arquivo de resultados"""
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_atual, 'resultados.txt')
        
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
        for linha in linhas:
            # Procura por número do sorteio e números sorteados
            match = re.search(r'(\d+)\s*-\s*([\d,]+)', linha)
            
            if match:
                sorteio = int(match.group(1))
                numeros = [num.strip() for num in match.group(2).split(',')]
                
                # Armazena o jogo
                self.jogos.append({
                    'sorteio': sorteio,
                    'numeros': numeros
                })
                
                # Atualiza a frequência dos números
                for num in numeros:
                    self.numeros_frequencia[num] = self.numeros_frequencia.get(num, 0) + 1
    
    def obter_frequencia_numero(self, numero):
        """Retorna a frequência de um número específico"""
        numero = str(numero).zfill(2)  # Garante que o número tenha 2 dígitos
        if numero in self.numeros_frequencia:
            return f"O número {numero} foi sorteado {self.numeros_frequencia[numero]} vezes."
        return f"O número {numero} nunca foi sorteado."
    
    def primeiro_sorteio_numero(self, numero):
        """Retorna informações sobre o primeiro sorteio de um número específico"""
        numero = str(numero).zfill(2)  # Garante que o número tenha 2 dígitos
        for jogo in self.jogos:
            if numero in jogo['numeros']:
                return f"O número {numero} apareceu pela primeira vez no sorteio {jogo['sorteio']}."
        return f"O número {numero} nunca foi sorteado."
    
    def primeiro_sorteio(self):
        """Retorna informações sobre o primeiro sorteio realizado"""
        if self.jogos:
            primeiro = self.jogos[0]
            numeros_formatados = ', '.join(primeiro['numeros'])
            return f"O primeiro sorteio (sorteio {primeiro['sorteio']}) teve os números: {numeros_formatados}."
        return "Não há dados de sorteios disponíveis."
    
    def evolucao_frequencia(self, numero, intervalo=100):
        """Analisa a evolução da frequência de um número ao longo do tempo"""
        numero = str(numero).zfill(2)  # Garante que o número tenha 2 dígitos
        total_jogos = len(self.jogos)
        
        if total_jogos == 0:
            return "Não há dados de sorteios disponíveis."
            
        if numero not in self.numeros_frequencia:
            return f"O número {numero} nunca foi sorteado."
        
        # Divide os jogos em intervalos e conta a frequência em cada um
        evolucao = []
        for i in range(0, total_jogos, intervalo):
            jogos_intervalo = self.jogos[i:i+intervalo]
            freq = sum(1 for jogo in jogos_intervalo if numero in jogo['numeros'])
            inicio = jogos_intervalo[0]['sorteio']
            fim = jogos_intervalo[-1]['sorteio']
            evolucao.append(f"Do sorteio {inicio} ao {fim}: {freq} vezes")
        
        return f"Evolução da frequência do número {numero} (por períodos de {intervalo} jogos):\n" + "\n".join(evolucao)
    
    def responder_pergunta(self, pergunta):
        """Processa a pergunta do usuário e retorna a resposta apropriada"""
        pergunta = pergunta.lower()
        
        # Extrai o número da pergunta, se houver
        match_numero = re.search(r'(\d+)', pergunta)
        numero = match_numero.group(1) if match_numero else None
        
        # Verifica frequência de um número específico
        if 'frequencia' in pergunta or 'frequência' in pergunta:
            if numero:
                return self.obter_frequencia_numero(numero)
        
        # Verifica primeiro sorteio de um número específico
        if 'primeiro' in pergunta and numero:
            return self.primeiro_sorteio_numero(numero)
        
        # Verifica primeiro sorteio geral
        if 'primeiro sorteio' in pergunta:
            return self.primeiro_sorteio()
        
        # Verifica evolução da frequência
        if ('evolucao' in pergunta or 'evolução' in pergunta) and numero:
            return self.evolucao_frequencia(numero)
        
        return ("Desculpe, não entendi sua pergunta. Você pode perguntar sobre:\n"
                "- Frequência de um número específico (ex: 'Qual a frequência do número 10?')\n"
                "- Primeiro sorteio de um número específico (ex: 'Quando foi o primeiro sorteio do número 25?')\n"
                "- Primeiro sorteio realizado (ex: 'Qual foi o primeiro sorteio?')\n"
                "- Evolução da frequência de um número (ex: 'Como foi a evolução do número 15?')") 