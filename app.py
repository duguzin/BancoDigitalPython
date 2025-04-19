from flask import Flask, request, jsonify
from Backend.utils import carregar_usuarios, salvar_usuarios
from flask_cors import CORS  # Importa o CORS
import os

app = Flask(__name__)

#Habilitar o CORS para o Front-end
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

#Rota Cadastrar novo Usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        data = request.get_json()
        cpf = data.get('cpf')
        nome = data.get('nome')
        senha = data.get('senha')

        usuarios = carregar_usuarios()

        if cpf in usuarios:
            return jsonify({"message": "Usuário já existe!"}), 400

        usuarios[cpf] = {
            "nome": nome,
            "senha": senha,
            "saldo": 0.0,
            "extrato": ["Cadastro realizado com sucesso."]
        }

        salvar_usuarios(usuarios)
        return jsonify({"message": "Cadastro realizado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

#Rota Login Usuário
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  #Receber Dados via POST
    cpf = data.get('cpf')
    senha = data.get('senha')

    usuarios = carregar_usuarios()

    if cpf not in usuarios:
        return jsonify({"message": "Usuário não encontrado!"}), 404

    if usuarios[cpf]['senha'] != senha:
        return jsonify({"message": "Senha incorreta!"}), 401

    #Retornar Dados do Usuário
    usuario = usuarios[cpf]
    return jsonify({
        "message": "Login bem-sucedido!",
        "nome": usuario["nome"],
        "cpf": cpf,
        "saldo": usuario["saldo"],
        "extrato": usuario["extrato"]
    }), 200

#Rota Dashboard (Informações Usuário)
@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        usuarios = carregar_usuarios()
        #Retornar Dados como JSON
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

#Rota SACAR
@app.route('/sacar', methods=['POST'])
def sacar():
    data = request.get_json()
    cpf = data.get('cpf')
    valor = data.get('valor')

    usuarios = carregar_usuarios()

    if cpf not in usuarios:
        return jsonify({"message": "Usuário não encontrado!"}), 404

    if usuarios[cpf]['saldo'] < valor:
        return jsonify({"message": "Saldo insuficiente!"}), 400

    usuarios[cpf]['saldo'] -= valor
    usuarios[cpf]['extrato'].append(f"Saque de R${valor:.2f}")

    salvar_usuarios(usuarios)

    return jsonify({"message": f"Saque de R${valor:.2f} realizado com sucesso!", "saldo": usuarios[cpf]['saldo']}), 200

#Rota DEPOSITAR
@app.route('/depositar', methods=['POST'])
def depositar():
    data = request.get_json()
    cpf = data.get('cpf')
    valor = data.get('valor')

    usuarios = carregar_usuarios()

    if cpf not in usuarios:
        return jsonify({"message": "Usuário não encontrado!"}), 404

    usuarios[cpf]['saldo'] += valor
    usuarios[cpf]['extrato'].append(f"Depósito de R${valor:.2f}")

    salvar_usuarios(usuarios)

    return jsonify({"message": f"Depósito de R${valor:.2f} realizado com sucesso!", "saldo": usuarios[cpf]['saldo']}), 200

#Rota TRANSFERIR
@app.route('/transferir', methods=['POST'])
def transferir():
    data = request.get_json()
    cpf_origem = data.get('cpf_origem')
    cpf_destino = data.get('cpf_destino')
    valor = data.get('valor')

    usuarios = carregar_usuarios()

    if cpf_origem not in usuarios:
        return jsonify({"message": "Usuário de origem não encontrado!"}), 404

    if cpf_destino not in usuarios:
        return jsonify({"message": "Usuário de destino não encontrado!"}), 404

    if usuarios[cpf_origem]['saldo'] < valor:
        return jsonify({"message": "Saldo insuficiente!"}), 400

    #Realizar transferência
    usuarios[cpf_origem]['saldo'] -= valor
    usuarios[cpf_destino]['saldo'] += valor

    #Registrar no Extrato dos Dois Usuários
    usuarios[cpf_origem]['extrato'].append(f"Transferência de R${valor:.2f} para {usuarios[cpf_destino]['nome']}")
    usuarios[cpf_destino]['extrato'].append(f"Recebimento de R${valor:.2f} de {usuarios[cpf_origem]['nome']}")

    print(f"Dados antes de salvar: {usuarios}")  # Log para Depuração

    salvar_usuarios(usuarios)

    return jsonify({
            "message": f"Transferência de R${valor:.2f} realizada com sucesso!",
            "saldo_origem": usuarios[cpf_origem]['saldo'],
            "saldo_destino": usuarios[cpf_destino]['saldo'],
            "nome_destino": usuarios[cpf_destino]['nome']
    }), 200



if __name__ == '__main__':
    #Exibir o Caminho Absoluto usuarios.json
    caminho_usuarios_json = os.path.abspath("Backend/usuarios.json")
    print("Caminho absoluto do arquivo usuarios.json:", caminho_usuarios_json)

    app.run(debug=True)
