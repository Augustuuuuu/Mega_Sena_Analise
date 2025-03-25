import re
from collections import Counter

class MegaSenaQA:
    def __init__(self):
        self.total_jogos = 0
        self.numeros_frequencia = {}
        self.carregar_dados()
        
    def carregar_dados(self):
        """Carrega os dados do arquivo de resultados"""
        with open('resultados.txt', 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
        for linha in linhas:
            match = re.search(r'-\s*([\d,]+)', linha)
            if match:
                self.total_jogos += 1
                numeros = match.group(1).split(',')
                for num in numeros:
                    num = num.strip()
                    self.numeros_frequencia[num] = self.numeros_frequencia.get(num, 0) + 1
    
    def responder_pergunta(self, pergunta):
        """Responde perguntas sobre a Mega Sena"""
        pergunta = pergunta.lower()
        
        # Pergunta sobre total de jogos
        if any(palavra in pergunta for palavra in ['quantos jogos', 'total de jogos', 'número de jogos']):
            return f"Foram analisados {self.total_jogos} jogos da Mega Sena."
        
        # Pergunta sobre números mais sorteados
        if any(palavra in pergunta for palavra in ['mais sorteado', 'mais frequente', 'aparece mais']):
            mais_sorteados = sorted(self.numeros_frequencia.items(), key=lambda x: x[1], reverse=True)[:5]
            resposta = "Os números mais sorteados são:\n"
            for num, freq in mais_sorteados:
                resposta += f"Número {num}: {freq} vezes\n"
            return resposta
        
        # Pergunta sobre números menos sorteados
        if any(palavra in pergunta for palavra in ['menos sorteado', 'menos frequente', 'aparece menos']):
            menos_sorteados = sorted(self.numeros_frequencia.items(), key=lambda x: x[1])[:5]
            resposta = "Os números menos sorteados são:\n"
            for num, freq in menos_sorteados:
                resposta += f"Número {num}: {freq} vezes\n"
            return resposta
        
        # Pergunta sobre frequência de um número específico
        match = re.search(r'número (\d+)', pergunta)
        if match:
            num = match.group(1)
            if num in self.numeros_frequencia:
                return f"O número {num} foi sorteado {self.numeros_frequencia[num]} vezes."
            else:
                return f"Não encontrei informações sobre o número {num}."
        
        # Pergunta sobre números pares e ímpares
        if any(palavra in pergunta for palavra in ['par', 'ímpar', 'impar']):
            pares = sum(1 for num in self.numeros_frequencia.keys() if int(num) % 2 == 0)
            impares = len(self.numeros_frequencia) - pares
            return f"Dos números sorteados, {pares} são pares e {impares} são ímpares."
        
        return "Desculpe, não entendi sua pergunta. Tente perguntar sobre:\n" + \
               "- Quantidade total de jogos\n" + \
               "- Números mais ou menos sorteados\n" + \
               "- Frequência de um número específico\n" + \
               "- Quantidade de números pares e ímpares" 