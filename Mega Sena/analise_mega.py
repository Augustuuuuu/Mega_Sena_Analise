from collections import Counter
import re

def ler_resultados():
    numeros = []
    with open('resultados.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            # Extrai apenas os números após o traço
            match = re.search(r'-\s*([\d,]+)', linha)
            if match:
                # Divide os números e adiciona à lista
                numeros_linha = match.group(1).split(',')
                numeros.extend(numeros_linha)
    return numeros

def analisar_numeros(arquivo, quantidade, tipo_ordenacao='mais'):
    """
    Analisa os números da Mega Sena a partir de um arquivo de resultados.
    
    Args:
        arquivo (str): Caminho do arquivo com os resultados
        quantidade (int): Quantidade de números a retornar
        tipo_ordenacao (str): 'mais' para mais sorteados, 'menos' para menos sorteados
    
    Returns:
        dict: Dicionário com os números e suas frequências
    """
    # Lista para armazenar todos os números sorteados
    todos_numeros = []
    
    try:
        # Abre o arquivo no modo de leitura
        with open(arquivo, 'r', encoding='utf-8') as f:
            # Itera sobre cada linha do arquivo
            for linha in f:
                # Remove espaços em branco e quebras de linha
                linha = linha.strip()
                # Verifica se a linha não está vazia
                if linha:
                    # Divide a linha em partes usando o caractere '|'
                    partes = linha.split('|')
                    # Verifica se a linha tem pelo menos 2 partes (data e números)
                    if len(partes) >= 2:
                        # Pega a parte dos números (segunda parte)
                        numeros_str = partes[1].strip()
                        # Divide a string dos números em uma lista
                        numeros = numeros_str.split()
                        # Converte cada número para inteiro e adiciona à lista
                        todos_numeros.extend([int(n) for n in numeros])
        
        # Verifica se foram encontrados números
        if not todos_numeros:
            return {'erro': 'Nenhum número encontrado no arquivo.'}
        
        # Conta a frequência de cada número usando Counter
        contagem = Counter(todos_numeros)
        
        # Ordena os números com base no tipo de ordenação
        if tipo_ordenacao == 'mais':
            # Ordena do mais frequente para o menos frequente
            numeros_ordenados = sorted(contagem.items(), key=lambda x: (-x[1], x[0]))
        else:
            # Ordena do menos frequente para o mais frequente
            numeros_ordenados = sorted(contagem.items(), key=lambda x: (x[1], x[0]))
        
        # Limita a quantidade de números retornados
        numeros_ordenados = numeros_ordenados[:quantidade]
        
        # Retorna um dicionário com os resultados
        return {
            'todos_numeros': numeros_ordenados,
            'tipo_ordenacao': tipo_ordenacao
        }
        
    except FileNotFoundError:
        # Retorna erro se o arquivo não for encontrado
        return {'erro': f'Arquivo {arquivo} não encontrado.'}
    except ValueError:
        # Retorna erro se houver problema na conversão dos números
        return {'erro': 'Erro ao processar os números no arquivo.'}
    except Exception as e:
        # Retorna erro genérico para outras exceções
        return {'erro': f'Erro ao processar o arquivo: {str(e)}'}

# Bloco principal que será executado quando o script for rodado diretamente
if __name__ == '__main__':
    # Define o caminho do arquivo de resultados
    arquivo = 'resultados.txt'
    
    try:
        # Solicita ao usuário a quantidade de números a mostrar
        quantidade = int(input('Quantos números você deseja ver? '))
        
        # Verifica se a quantidade é válida
        if quantidade < 1 or quantidade > 60:
            print('Por favor, insira um número entre 1 e 60.')
        else:
            # Realiza a análise dos números
            resultado = analisar_numeros(arquivo, quantidade)
            
            # Verifica se houve erro na análise
            if 'erro' in resultado:
                print(resultado['erro'])
            else:
                # Imprime os resultados formatados
                print(f'\nNúmeros mais sorteados:')
                for numero, frequencia in resultado['todos_numeros']:
                    print(f'Número {numero}: {frequencia} vezes')
                    
    except ValueError:
        # Trata erro se o usuário não inserir um número válido
        print('Por favor, insira um número válido.') 
