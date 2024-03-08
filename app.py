from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from services.settings import APP_VERSION, JWT_SECRET_KEY, SECRET_KEY
from services.SuperSapiens.super_sapiens import SuperSapiensService
import re

from flasgger import Swagger, swag_from
from documentation.login_docs import LOGIN_ROUTE
from documentation.search_all_docs import SEARCH_ALL_ROUTE
from documentation.headers_config import SWAGGER_TEMPLATE

# Inicializa Flask
app = Flask(__name__)

# Config das Docs
Swagger(app, template=SWAGGER_TEMPLATE)


# Config JWT
app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ALGORITHM"] = "HS256"

# Habilita CORS em todas as rotas e origens
CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})

# Inicializa service do SuperSapiens
super_sapiens_service = SuperSapiensService()

jwt = JWTManager(app)

def is_valid_date_format(date_str):
    # Expressão regular para verificar o formato da data
    date_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    return bool(re.match(date_pattern, date_str))


@app.route('/', methods=['GET'])
def home():
    '''Define a rota inicial'''
    return jsonify({
        "status": 200,
        "mensagem": f"Search-Sapiens-API versão {APP_VERSION} operando normalmente.",
        "valores": {}
    })


@app.route('/login', methods=['POST'])
@swag_from(LOGIN_ROUTE)
def sapiens_login_post():
    '''Define a rota: API para requisitar Login no SUPER SAPIENS '''

    # Prepara as credenciais
    if "loginSapiens" in request.get_json() or "senhaSapiens" in request.get_json():
        session['loginSapiens'] = request.get_json().get("loginSapiens")
        session['senhaSapiens'] = request.get_json().get("senhaSapiens")

        # Processa a autenticação
        login_request = super_sapiens_service.login(
            username=session['loginSapiens'], password=session['senhaSapiens'])

        if "status" in login_request and login_request.get("status") == 200:
            user_sapiens_data = super_sapiens_service.get_usuario()
            if user_sapiens_data.get("sucesso"):
                session["is_logged_in"] = True

                nome_usuario = user_sapiens_data['dados']['nome']
                split = nome_usuario.split(" ")
                nome_usuario_f = f"{split[0]} {split[len(split) - 1]}".title()
                user_id = user_sapiens_data['dados']['id']

                access_token = create_access_token(identity={
                    "id": str(user_id),
                    "dados": user_sapiens_data['dados']})

                return jsonify({
                    "status": 200,
                    "mensagem": "Usuário autenticado com sucesso no SuperSAPIENS.",
                    "valores": {
                        "id": user_id or "",
                        "nome": nome_usuario_f or "",
                    },
                    "token": access_token,
                })

    # Caso autenticação falhe
    session["is_logged_in"] = False
    return jsonify({
        "status": 401,
        "mensagem": "Autenticação do usuário no SAPIENS falhou.",
        "valores": login_request.get("mensagem") or "",
    })


@app.route('/search_all', methods=['POST'])
@jwt_required()
@swag_from(SEARCH_ALL_ROUTE)
def search_all():
    '''Define a rota de pesquisa de documentos'''

    try:
        data = request.get_json()

        content = data.get("content")
        extension = data.get("extension")
        unity = data.get("unity")
        document_type = data.get("document_type")
        created_at = data.get("created_at")
        created_on = data.get("created_on")
        created_by = data.get("created_by")
        sector = data.get("sector")

        # Verifica se a data está no formato correto
        if created_at is not None and not is_valid_date_format(created_at):
            return jsonify({"success": False, "message": "A data 'created_at' não está no formato correto."}), 400
        if created_on is not None and not is_valid_date_format(created_on):
            return jsonify({"success": False, "message": "A data 'created_on' não está no formato correto."}), 400

        # TESTEEE --->>
        user_sapiens_dataTEST = get_jwt_identity()
        print('TEST user SapiensData --', user_sapiens_dataTEST)

        result = super_sapiens_service.search_all_data(content, extension, unity, document_type, created_at, created_on, created_by, sector)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao buscar Pasta: {e}"}), 500
