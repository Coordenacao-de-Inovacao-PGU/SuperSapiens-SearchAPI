from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from services.settings import APP_VERSION, JWT_SECRET_KEY, SECRET_KEY
from services.SuperSapiens.super_sapiens import SuperSapiensService
import re

# Docs imports
from flasgger import Swagger, swag_from
from documentation.login_docs import LOGIN_ROUTE
from documentation.search_user_docs import SEARCH_USER_BY_NAME_ROUTE
from documentation.search_unity_docs import SEARCH_UNITY_ROUTE
from documentation.search_sector_docs import SEARCH_SECTOR_ROUTE
from documentation.search_document_type_docs import SEARCH_DOCUMENT_TYPE_ROUTE
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


# Rota de autenticacao
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
                expiration_token = user_sapiens_data['dados']['expiration_token']

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
                    "expiration": expiration_token
                })

    # Caso autenticação falhe
    session["is_logged_in"] = False
    return jsonify({
        "status": 401,
        "mensagem": "Autenticação do usuário no SAPIENS falhou.",
        "valores": login_request.get("mensagem") or "",
    })


# Rotas para filtros
@app.route('/search_document_type', methods=['GET'])
@jwt_required()
@swag_from(SEARCH_DOCUMENT_TYPE_ROUTE)
def search_document_type_route():
    '''Define a rota de pesquisa de tipos documentos'''

    try:
        query = request.args.get('q')
        if query:
            result = super_sapiens_service.search_document_type(query)
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "message": f"Query nao encontrada!"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao buscar Pasta: {e}"}), 500


@app.route('/search_user_by_name', methods=['GET'])
@jwt_required()
@swag_from(SEARCH_USER_BY_NAME_ROUTE)
def search_user_by_name_route():
    '''Define a rota de pesquisa de usuario pelo nome'''

    try:
        query = request.args.get('q')
        if query:
            result = super_sapiens_service.search_user_by_name(query)
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "message": f"Query nao encontrada!"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao buscar Pasta: {e}"}), 500


@app.route('/search_unity', methods=['GET'])
@jwt_required()
@swag_from(SEARCH_UNITY_ROUTE)
def search_unity_route():
    '''Define a rota de pesquisa de unidades'''

    try:
        query = request.args.get('q')
        if query:
            result = super_sapiens_service.search_unity(query)
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "message": f"Query nao encontrada!"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao buscar Pasta: {e}"}), 500


@app.route('/search_sector', methods=['GET'])
@jwt_required()
@swag_from(SEARCH_SECTOR_ROUTE)
def search_sector_route():
    '''Define a rota de pesquisa de setores'''

    try:
        query = request.args.get('q')
        unity_id = request.args.get('unity_id')
        if query and unity_id:
            result = super_sapiens_service.search_sector(unity_id, query)
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "message": f"Query ou ID da unidade nao encontrada!"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao buscar Pasta: {e}"}), 500


# Rota de pesquisa de documentos
@app.route('/search_all', methods=['POST'])
@jwt_required()
@swag_from(SEARCH_ALL_ROUTE)
def search_all():
    '''Define a rota de pesquisa de documentos'''

    try:
        data = request.get_json()

        year = data.get("year")
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

        result = super_sapiens_service.search_all_data(content, year, extension, unity, document_type, created_at, created_on,
                                                       created_by, sector)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao buscar Pasta: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
