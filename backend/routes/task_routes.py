from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.task import Task
from redis import Redis

# Inicializando o cliente Redis
redis_client = Redis(host='localhost', port=6379, db=0)

class TaskList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # Obtém o ID ou nome de usuário do token JWT
        redis_key = f"tasks:{user_id}"  # Chave única para cada usuário

        # Verifica se as tarefas do usuário estão no cache Redis
        cached_tasks = redis_client.get(redis_key)
        if cached_tasks:
            return jsonify({"tasks": eval(cached_tasks)})

        # Se não estiver em cache, consulta o banco de dados
        tasks = Task.query.filter_by(user_id=user_id).all()
        tasks_list = [task.to_dict() for task in tasks]

        # Armazena no cache Redis para futuras consultas
        redis_client.set(redis_key, str(tasks_list))
        return jsonify({"tasks": tasks_list})

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()  # Obtém o ID ou nome de usuário do token JWT
        data = request.get_json()
        title = data.get("title")

        if not title:
            return {"error": "Título da tarefa é obrigatório"}, 400

        # Cria uma nova tarefa para o usuário atual
        new_task = Task(title=title, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        # Limpa o cache do Redis para garantir que a nova tarefa apareça na próxima consulta
        redis_key = f"tasks:{user_id}"
        redis_client.delete(redis_key)

        return new_task.to_dict(), 201

class Task(Resource):
    @jwt_required()
    def put(self, task_id):
        data = request.get_json()
        task = Task.query.get(task_id)

        if not task:
            return {"error": "Tarefa não encontrada"}, 404

        task.status = data.get("status", task.status)
        db.session.commit()

        redis_client.delete("tasks")  # Limpar cache
        return task.to_dict(), 200

    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get(task_id)
        
        if not task:
            return {"error": "Tarefa não encontrada"}, 404

        db.session.delete(task)
        db.session.commit()

        redis_client.delete("tasks")  # Limpar cache
        return {"message": "Tarefa removida com sucesso"}, 200

def initialize_routes(api):
    api.add_resource(TaskList, '/tasks')
    api.add_resource(Task, '/tasks/<int:task_id>')