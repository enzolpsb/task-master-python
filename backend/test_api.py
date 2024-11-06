import requests

# URL base da API
BASE_URL = "http://127.0.0.1:5000"

# Credenciais para login
CREDENTIALS = {
    "username": "admin",
    "password": "senha123"
}

def get_jwt_token():
    """Autentica e retorna o token JWT."""
    response = requests.post(f"{BASE_URL}/login", json=CREDENTIALS)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Autenticação bem-sucedida. Token obtido:", token)
        return token
    else:
        print("Falha na autenticação:", response.status_code, response.text)
        return None

def make_headers(token):
    """Gera os cabeçalhos de autorização."""
    return {"Authorization": f"Bearer {token}"}

def list_tasks(token):
    """Lista todas as tarefas."""
    headers = make_headers(token)
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    print("Listando Tarefas:", response.status_code, response.json())

def add_task(token, title):
    """Adiciona uma nova tarefa."""
    headers = make_headers(token)
    task_data = {"title": title}
    response = requests.post(f"{BASE_URL}/tasks", headers=headers, json=task_data)
    print("Tarefa Adicionada:", response.status_code, response.json())

def update_task(token, task_id, status):
    """Atualiza o status de uma tarefa."""
    headers = make_headers(token)
    task_data = {"status": status}
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", headers=headers, json=task_data)
    print("Tarefa Atualizada:", response.status_code, response.json())

def delete_task(token, task_id):
    """Exclui uma tarefa."""
    headers = make_headers(token)
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    print("Tarefa Excluída:", response.status_code, response.json())

def main():
    # Passo 1: Obter o token JWT
    token = get_jwt_token()
    if not token:
        return  # Encerra o script se a autenticação falhar

    # Passo 2: Operações na API
    print("\nExecutando operações na API:")
    list_tasks(token)         # Listar todas as tarefas
    add_task(token, "Estudar Python")  # Adicionar uma nova tarefa
    update_task(token, 1, "completa")  # Atualizar a tarefa com ID 1
    delete_task(token, 1)     # Excluir a tarefa com ID 1

if __name__ == "__main__":
    main()