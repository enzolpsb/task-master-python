const BASE_URL = 'http://127.0.0.1:5000'; // URL base da API

// Carregar as tarefas ao iniciar
// script.js

document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem("token");
    console.log("tokn",token)
    print(token)
    if (!token) {
        // Redireciona diretamente para a página de login se o token não estiver disponível
        window.location.href = "login.html";
    } else {
        // Caso o usuário tenha um token, tente carregar as tarefas
        fetchTasks();
    }
});

// Função para buscar todas as tarefas
async function fetchTasks() {
    try {
        const token = localStorage.getItem("token"); // Confirma que a variável está definida
        if (!token) {
            window.location.href = "login.html"; // Redireciona se não houver token
            return; // Evita chamada desnecessária
        }
        const response = await fetch(`${BASE_URL}/tasks`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error(`Erro: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(data);
        // Faça algo com os dados recebidos, como renderizar as tarefas na página
    } catch (error) {
        console.error("Erro ao buscar tarefas:", error);
        // Exibir erro para o usuário ou tomar alguma ação apropriada
    }
}

// Função para exibir as tarefas na interface
function displayTasks(tasks) {
  const taskList = document.getElementById('task-list');
  taskList.innerHTML = ''; // Limpar a lista

  tasks.forEach(task => {
    const taskItem = document.createElement('li');
    taskItem.classList.add('task-item');
    if (task.status === 'completa') taskItem.classList.add('completed');
    
    taskItem.innerHTML = `
      <span>${task.title}</span>
      <div>
        <button class="update-btn" onclick="updateTask(${task.id}, '${task.status === 'pendente' ? 'completa' : 'pendente'}')">
          ${task.status === 'pendente' ? 'Completar' : 'Reabrir'}
        </button>
        <button class="delete-btn" onclick="deleteTask(${task.id})">Remover</button>
      </div>
    `;
    taskList.appendChild(taskItem);
  });
}

// Função para adicionar uma nova tarefa
// script.js

async function addTask() {
    const inputElement = document.getElementById("taskInput");
    if (inputElement) {
        const taskTitle = inputElement.value;
        if (taskTitle) {
            try {
                const response = await fetch("http://127.0.0.1:5000/tasks", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("token")}`
                    },
                    body: JSON.stringify({ title: taskTitle }) // JSON correto com "title"
                });

                if (!response.ok) {
                    throw new Error(`Erro ao adicionar tarefa: ${response.statusText}`);
                }

                const data = await response.json();
                console.log("Tarefa adicionada com sucesso:", data);
                fetchTasks(); // Atualiza a lista de tarefas após adicionar
            } catch (error) {
                console.error("Erro ao adicionar tarefa:", error);
            }
        } else {
            console.error("O título da tarefa está vazio.");
        }
    } else {
        console.error("Elemento de input não encontrado.");
    }
}
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
           
            localStorage.setItem("token", "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMDg5OTY2NiwianRpIjoiMWE0YmNlNTMtZjM0OS00N2Q2LWI2YzctNzdiN2Q3MTVmNzQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzMwODk5NjY2LCJleHAiOjE3MzA5MDMyNjZ9.wkiODA-Prksgws9aOw5Oe4nJwbWi09buw6X-UEqoCJk"); // Salva o token no Local Storage
            alert("Login bem-sucedido!");
            window.location.href = "index.html"; // Redireciona para a página principal
        } else {
            alert("Erro no login: " + data.message);
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro no login.");
    }
}

// Função para atualizar o status da tarefa
async function updateTask(taskId, newStatus) {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    },
    body: JSON.stringify({ status: newStatus })
  });

  if (response.ok) {
    fetchTasks(); // Atualiza a lista de tarefas
  } else {
    alert('Erro ao atualizar tarefa.');
  }
}

// Função para remover uma tarefa
async function deleteTask(taskId) {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
  });

  if (response.ok) {
    fetchTasks(); // Atualiza a lista de tarefas
  } else {
    alert('Erro ao remover tarefa.');
  }
}