from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from .services.settings import APP_VERSION, JWT_SECRET_KEY, SECRET_KEY
from services.SuperSapiens.super_sapiens import SuperSapiensService

# Inicializa Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

# Habilita CORS em todas as rotas e origens
CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})

# Inicializa service do SuperSapiens
super_sapiens_service = SuperSapiensService()

jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def home():
    '''Define a rota inicial'''
    return jsonify({
        "status": 200,
        "mensagem": f"Bumblebee versão {APP_VERSION} operando normalmente.",
        "valores": {}
    })


@app.route('/login', methods=['POST'])
def sapiens_login_post():
    '''Define a rota: API para requisitar Login no SUPER SAPIENS '''

    # Prepara as credenciais
    if ("loginSapiens" in request.get_json() or "senhaSapiens" in request.get_json()):
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

                # TESTEEE --->>
                user_sapiens_dataTEST = get_jwt_identity()
                print('TEST user SapiensData --', user_sapiens_dataTEST)

                return jsonify({
                    "status": 200,
                    "mensagem": "Usuário autenticado com sucesso no SAPIENS.",
                    "valores": {
                        "id": user_id or "",
                        "nome": nome_usuario_f or "",
                    }
                })

    # Caso autenticação falhe
    session["is_logged_in"] = False
    return jsonify({
        "status": 401,
        "mensagem": "Autenticação do usuário no SAPIENS falhou.",
        "valores": login_request.get("mensagem") or "",
    })


@app.route('/search_all', methods=['GET'])
@jwt_required()
def search_all():
    '''Define a rota de pesquisa de documentos'''
