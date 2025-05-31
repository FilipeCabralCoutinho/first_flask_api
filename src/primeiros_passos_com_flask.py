from flask import Flask, url_for, request

app = Flask(__name__)

@app.route("/home")
def hello_world():
    return {
        'Message': "<h1>Hello, World!!!</h1>",
        }

#endpoint ou rota que nós podemos passar parâmetros pela url
@app.route("/pessoa/<nome>/<int:idade>/<float:altura>")
def pessoa(nome, idade, altura):
    return f"<h1>Nome: {nome}, Idade: {idade}, Altura: {altura}</h1>"

#mais uma rota criada apenas para ter mais uma pro próximo exemplo
@app.route("/terceira")
def terceira():
    return "<h1>Esta é a terceira página!!!</h1>"

#o exemplo abaixo usa url_for para trazer dinamismo às url das rotas: (necessário import)
nome = "Maria"
idade = 50
altura = 1.52


with app.test_request_context():
    print(url_for("hello_world"))
    #usando url for, conseguiremos passar os parâmetros para a url por meio de variáveis. veja abaixo:
    print(url_for("pessoa", nome="Filipe", idade=29, altura=1.69))
    url_pessoa = url_for("pessoa", nome=nome, idade=idade, altura=altura)
    print(url_for("terceira"))

#rota, página criada para demonstrar a montagem dinâmica de url usando a variável url_pessoa
@app.route("/principal")
def links():
    return f'<h1><a href="http://127.0.0.1:5000{url_pessoa}" target="_blank" rel="noopener noreferrer">Visite a página pessoa</a></h1>'

#rota, página para demonstrar a utilização de diferentes requisições HTTP
@app.route("/methods", methods=["GET", "POST"])
def methods():
    if request.method == 'GET':
        return "<h1>Foi usado o método GET!<h1>"
    else:
        return "<h1>Foi usado o método POST!<h1>"
