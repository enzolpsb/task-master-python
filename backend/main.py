from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from models import db
from models.user import User
from routes.task_routes import initialize_routes
from routes.auth_routes import auth_bp
from redis import Redis
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
CORS(app)
# Configurações do banco de dados e Redis
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'  # Use uma chave segura em produção
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expira em 1 hora
redis_client = Redis(host='localhost', port=6379, db=0)

# Inicializar extensões
db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)
jwt = JWTManager(app)

# Defina um usuário e senha para login (simplificado)
USUARIO = "admin"
SENHA = "senha123"

# Rota de Login para gerar o token JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Verifica se o usuário e senha estão corretos
    if username == USUARIO and password == SENHA:
        # Cria um token JWT
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Usuário ou senha incorretos"}), 401

# Inicializar rotas de tarefas
initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True)