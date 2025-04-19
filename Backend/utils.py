import json
import os

#Caminho Absoluto do Arquivo
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'usuarios.json')

def carregar_usuarios():
    if not os.path.exists(caminho_arquivo) or os.path.getsize(caminho_arquivo) == 0:
        return {}

    with open(caminho_arquivo, 'r') as f:
        try:
            usuarios = json.load(f)
            print("Usuários carregados:", usuarios)
            return usuarios
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON.")
            return {}

def salvar_usuarios(usuarios):
    try:
        with open(caminho_arquivo, 'w') as f:
            json.dump(usuarios, f, indent=4)
            print("Usuários salvos:", usuarios)
    except Exception as e:
        print(f"Erro ao salvar usuários: {str(e)}")
