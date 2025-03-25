# Importação das bibliotecas necessárias
from flask import Flask, render_template, request  # Flask para criar a aplicação web
from collections import Counter  # Counter para contar frequência de números
import re  # Expressões regulares para processamento de texto

# Inicialização da aplicação Flask
app = Flask(__name__)

def ler_resultados():
    # Lista para armazenar todos os números lidos
    numeros = []
    total_jogos = 0
    # Abre o arquivo de resultados em modo leitura com codificação UTF-8
    with open('resultados.txt', 'r', encoding='utf-8') as arquivo:
        # Itera sobre cada linha do arquivo
        for linha in arquivo:
            # Procura por padrões de números após um hífen
            match = re.search(r'-\s*([\d,]+)', linha)
            if match:
                # Incrementa o contador de jogos
                total_jogos += 1
                # Extrai os números da linha e os separa por vírgula
                numeros_linha = match.group(1).split(',')
                # Adiciona os números à lista principal
                numeros.extend(numeros_linha)
    return numeros, total_jogos

def analisar_numeros(quantidade, tipo_ordenacao):
    # Lê todos os números do arquivo
    numeros, total_jogos = ler_resultados()
    # Conta a frequência de cada número
    contagem = Counter(numeros)
    
    if tipo_ordenacao == 'mais':
        # Ordena por frequência em ordem decrescente (mais frequentes primeiro)
        numeros_ordenados = sorted(contagem.items(), key=lambda x: int(x[1]), reverse=True)
    else:
        # Ordena por frequência em ordem crescente (menos frequentes primeiro)
        numeros_ordenados = sorted(contagem.items(), key=lambda x: int(x[1]))
    
    # Conta números pares e ímpares
    numeros_selecionados = numeros_ordenados[:quantidade]
    pares = sum(1 for num, _ in numeros_selecionados if int(num) % 2 == 0)
    impares = quantidade - pares
    
    # Retorna um dicionário com os números ordenados, tipo de ordenação e contagem de pares/ímpares
    return {
        'todos_numeros': numeros_selecionados,
        'tipo_ordenacao': tipo_ordenacao,
        'pares': pares,
        'impares': impares,
        'total_jogos': total_jogos
    }

# Rota principal da aplicação que aceita métodos GET e POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializa a variável de resultado como None
    resultado = None
    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':
        try:
            # Obtém a quantidade e o tipo de ordenação do formulário
            quantidade = int(request.form['quantidade'])
            tipo_ordenacao = request.form.get('tipo_ordenacao', 'mais')
            
            # Valida se a quantidade está entre 1 e 60
            if 1 <= quantidade <= 60:
                resultado = analisar_numeros(quantidade, tipo_ordenacao)
            else:
                resultado = {'erro': 'Por favor, digite um número entre 1 e 60.'}
        except ValueError:
            resultado = {'erro': 'Por favor, digite um número válido.'}
    
    # Renderiza o template index.html com o resultado
    return render_template('index.html', resultado=resultado)

# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug
    app.run(debug=True) 