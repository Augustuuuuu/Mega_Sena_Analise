from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__)

def ler_resultados():
    numeros = []
    with open('resultados.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            match = re.search(r'-\s*([\d,]+)', linha)
            if match:
                numeros_linha = match.group(1).split(',')
                numeros.extend(numeros_linha)
    return numeros

def analisar_numeros(quantidade, tipo_ordenacao):
    numeros = ler_resultados()
    contagem = Counter(numeros)
    
    if tipo_ordenacao == 'mais':
        # Ordena por frequência em ordem decrescente
        numeros_ordenados = sorted(contagem.items(), key=lambda x: int(x[1]), reverse=True)
    else:
        # Ordena por frequência em ordem crescente
        numeros_ordenados = sorted(contagem.items(), key=lambda x: int(x[1]))
    
    return {
        'todos_numeros': numeros_ordenados[:quantidade],
        'tipo_ordenacao': tipo_ordenacao
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        try:
            quantidade = int(request.form['quantidade'])
            tipo_ordenacao = request.form.get('tipo_ordenacao', 'mais')
            
            if 1 <= quantidade <= 60:
                resultado = analisar_numeros(quantidade, tipo_ordenacao)
            else:
                resultado = {'erro': 'Por favor, digite um número entre 1 e 60.'}
        except ValueError:
            resultado = {'erro': 'Por favor, digite um número válido.'}
    
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True) 