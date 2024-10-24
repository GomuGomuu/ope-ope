import requests
from requests.auth import HTTPBasicAuth

# Configurações da API
url = "http://127.0.0.1:5000/upload"  # URL do endpoint de upload
username = "admin"  # Nome de usuário para autenticação
password = "password"  # Senha para autenticação
image_path = "placa1.jpg"  # Caminho da imagem a ser enviada


# Função para enviar a imagem
def upload_image(image_path):
    try:
        # Abrindo o arquivo de imagem
        with open(image_path, "rb") as image_file:
            # Definindo o payload e cabeçalhos
            files = {"file": image_file}

            # Fazendo a requisição POST com autenticação básica
            response = requests.post(
                url, files=files, auth=HTTPBasicAuth(username, password)
            )

            # Verificando o status da resposta
            if response.status_code == 201:
                print(f"Upload realizado com sucesso: {response.json()}")
            else:
                print(f"Falha no upload: {response.status_code} - {response.text}")
    except FileNotFoundError:
        print(f"Arquivo {image_path} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    upload_image(image_path)
