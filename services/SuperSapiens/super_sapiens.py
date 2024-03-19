import requests
import json, re, base64
from typing import Optional
from datetime import datetime, timedelta


def validate_string(query):
    if query is not None:
        str_query = str(query)
        return str_query
    return ""


class SuperSapiensService():
    def __init__(self, r_session=None) -> None:
        self.token = None
        self.expiration = None
        self.baseurl = "https://supersapiensbackend.agu.gov.br"
        if self.token is not None:
            self.get_usuario()

        # Inicializa uma session do requests
        if r_session is not None:
            self.r_session = r_session
        else:
            self.r_session = self.get_session()

        self.r_session.headers.update({'Authorization': f'Bearer {self.token}'})

        # variaveis de caixa de selecao
        self.unity = None
        self.user_id_searched = None
        self.document_id = None
        self.sector_id = None

    def get_session(self):
        self.r_session = requests.session()
        return self.r_session

    def url(self, url: Optional[str] = None):
        return re.sub(r'^/?(.*)$', f'{self.baseurl}/\\1', url or '')

    def get_usuario(self):
        data_user = None
        try:
            perfil = self.get("/profile")
            data_user = json.loads(perfil.text)
            mensagem = "Usuário obtido com sucesso"
            data_user["expiration_token"] = self.expiration
        except Exception:
            data_user = None
            mensagem = "Erro ao buscar usuário"

        return {
            "sucesso": True if (data_user is not None) else False,
            "dados": data_user,
            "mensagem": mensagem
        }

    def post(self, resource, body, **kwargs):
        jbody = body if isinstance(body, (dict, list)) else None
        body = body if jbody is None else None
        return self.r_session.post(url=self.url(resource), data=body, json=jbody, **self.prepare_params(**kwargs))

    def get(self, resource, **kwargs):
        return self.r_session.get(url=self.url(resource), **self.prepare_params(**kwargs))

    def prepare_params(self, **kwargs):
        headers = kwargs.pop('headers', {})
        self.__check_expiration()
        if self.token:
            authkey = next((k for k in kwargs.keys() if k.casefold() == 'authorization'), 'Authorization')
            headers[authkey] = f'Bearer {self.token}'
        params = kwargs.pop('params', {})
        self.__check_expiration()
        if 'limit' in kwargs:
            params['limit'] = str(kwargs.pop('limit'))
        if 'offset' in kwargs:
            params['offset'] = str(kwargs.pop('offset'))
        if 'order' in kwargs:
            params['order'] = json.dumps(kwargs.pop('order'))
        if 'context' in kwargs:
            params['context'] = json.dumps(kwargs.pop('context'))
        if 'where' in kwargs:
            params['where'] = json.dumps(kwargs.pop('where'))
        if 'populate' in kwargs:
            params['populate'] = json.dumps(kwargs.pop('populate'))

        # @FIX: Adiciona política de requisições do Super Sapiens para este robô
        headers['X-Rate-Limit-API'] = 'SearchAPI'

        kwargs.update(headers=headers, params=params)
        return kwargs

    def __refresh_token(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        resp = self.r_session.get(self.url('auth/refresh_token'), headers=headers)
        if resp.status_code == 200:
            body = resp.json()
            self.token = body.get('token', '')
            self.expiration = datetime.fromtimestamp(body['exp'])

    def __check_expiration(self):

        # Se não tem token, sai
        if not self.token:
            return

        # Se não tem expiração, pega a partir do token
        if not self.expiration:
            self.expiration = self.__get_expiration_from_token()

        # Se ainda não tem expiração, é porque não tem token
        if not self.expiration:
            return

        # Atualiza o token se for vencer nos próximos 5 minutos
        if self.expiration < datetime.now() + timedelta(minutes=5):
            self.__refresh_token()

        if self.expiration < datetime.now():
            raise f"Token expirado em {self.expiration.strftime('%d/%m/%Y %H:%M:%S')}, não é possível continuar"

    def __get_expiration_from_token(self):
        if not self.token:
            return
        parts = self.token.split(".")
        if len(parts) != 3:
            raise "Token inválido!"
        payload = parts[1]
        dados = json.loads(base64.b64decode(payload.encode('utf-8') + b'==').decode('utf-8'))
        return datetime.fromtimestamp(dados.get('exp', 0))

    def login(self, username: str, password: str) -> dict:
        retorno = ''

        if username is None:
            retorno = 'Usuário ausente'
        if password is None:
            retorno = 'Senha ausente'

        self.token = None
        resp = self.post('auth/ldap_get_token', {'username': username, 'password': password})
        result = {'success': False}

        try:
            resp_body = resp.json()
        except ValueError as value_error:
            resp_body = {'message': str(value_error)}
        result.update(resp_body)
        if 'token' in resp_body:
            self.token = resp_body['token']
            self.expiration = datetime.fromtimestamp(resp_body['exp'])
            result['success'] = True
            retorno = "Login realizado com sucesso"

        if result.get("success", False):
            return {
                "status": 200,
                "mensagem": str(retorno)
            }
        else:
            return {
                "status": 401,
                "mensagem": "Erro ao fazer login"
            }

    def search_document_type(self, query):
        data = None
        url = "/v1/administrativo/tipo_documento"

        querystring = {"where":
                           "{\"andX\":"
                           "[{\"nome\":\"like:%" + str(query) + "%\"}]}",
                       "limit": "10",
                       "offset": "0",
                       "order": "{}",
                       "populate": "[]", "context": "{}"}

        payload = ""

        try:
            req: object = self.get(
                url,
                data=payload,
                params=querystring
            )
            data = json.loads(req.text)

            # Atribuindo valor que sera usado na busca
            self.document_id = data["entities"][0]['id']

        except Exception:
            print("Erro ao buscar Pasta")
            print('PAYLOAD: ', payload)

        return {
            "sucesso": True if (data is not None) else False,
            "data": data,
        }

    def search_user_by_name(self, query):
        data = None
        url = "/v1/administrativo/usuario"

        querystring = {"where":
                           "{\"andX\":"
                           "[{\"nome\":\"like:%" + str(query) + "%\"}]}",
                       "limit": "10",
                       "offset": "0",
                       "order": "{}",
                       "populate": "[\"populateAll\",\"colaborador\",\"colaborador.cargo\",\"colaborador.modalidadeColaborador\"]",
                       "context": "{}"}

        payload = ""

        try:
            req: object = self.get(
                url,
                data=payload,
                params=querystring
            )
            data = json.loads(req.text)

            # Atribuindo valor que sera usado na busca
            self.user_id_searched = data["entities"][0]['id']

        except Exception:
            print("Erro ao buscar Pasta")
            print('PAYLOAD: ', payload)

        return {
            "sucesso": True if (data is not None) else False,
            "data": data,
        }

    def search_unity(self, query):
        data = None
        url = "/v1/administrativo/setor"
        querystring = {
            "where":
                "{\"parent\":\"isNull\","
                "\"orX\":[{\"andX\":"
                "[{\"nome\":\"like:%" + str(query) + "%\"}]},"
                                                     "{\"andX\":"
                                                     "[{\"sigla\":\"like:%" + str(query) + "%\"}]}]}",
            "limit": "10", "offset": "0", "order": "{}", "populate": "[]", "context": "{}"}
        payload = ""

        try:
            req: object = self.get(
                url,
                data=payload,
                params=querystring
            )
            data = json.loads(req.text)

            # Atribuindo valor que sera usado na busca
            self.unity = data["entities"][0]['id']

        except Exception:
            print("Erro ao buscar Pasta")
            print('PAYLOAD: ', payload)

        return {
            "sucesso": True if (data is not None) else False,
            "data": data,
        }

    def search_sector(self, unity_id, query):
        data = None
        url = "/v1/administrativo/setor"

        querystring = {
            "where":
                "{\"parent\":\"isNotNull\","
                "\"unidade.id\":\"eq:" + str(unity_id) + "\","
                                                         "\"orX\":[{\"andX\":"
                                                         "[{\"nome\":\"like:%" + str(query) + "%\"}]},"
                                                                                              "{\"andX\":[{\"sigla\":\"like:%" + str(
                    query) + "%\"}]}]}",
            "limit": "10", "offset": "0", "order": "{}", "populate": "[\"unidade\",\"parent\"]", "context": "{}"}

        payload = ""

        try:
            req: object = self.get(
                url,
                data=payload,
                params=querystring
            )
            data = json.loads(req.text)

            # Atribuindo valor que sera usado na busca
            self.sector_id = data["entities"][0]['id']

        except Exception:
            print("Erro ao buscar Pasta")
            print('PAYLOAD: ', payload)

        return {
            "sucesso": True if (data is not None) else False,
            "data": data,
        }

    def search_all_data(self, content, year, extension, unity, document_type, created_at, created_on, created_by,
                        sector):

        # TODO: Fazer paginacao, utilizando ofset, valor anterior da pesquisa e continuacao
        # TODO: Se passar parametro todos mandar todos os documentos de uma vez - BOTAR LIMITE
        data = None
        url = "/v1/administrativo/componente_digital/search"

        if document_type:
            self.search_document_type(document_type)
        if created_by:
            self.search_user_by_name(created_by)

        # NOTE: Para pesquisar o setor e necessaria a Unidade antes #
        if unity:
            self.search_unity(unity)
            unity_id = self.unity
            if sector:
                self.search_sector(unity_id, sector)

        if created_at is None:
            created_at = f'{year}-01-01T00:00:00'
        if created_on is None:
            created_on = f'{year}-12-31T23:59:00'

        # Formatando variaveis
        content_formated = validate_string(content)
        extension_formated = validate_string(extension)
        document_type_formated = validate_string(self.document_id)
        created_at_formated = validate_string(created_at)
        created_on_formated = validate_string(created_on)
        user_id_formated = validate_string(self.user_id_searched)
        sector_id_formated = validate_string(self.sector_id)

        # Construcao da QueryString
        querystring = {
            "where": "{\"andX\":[",
            "limit": 10,
            "offset": "0",
            "order": "{}",
            "populate": "[\"populateAll\",\"documento\","
                        "\"documento.tipoDocumento\","
                        "\"documento.juntadaAtual\","
                        "\"documento.juntadaAtual.volume\","
                        "\"documento.juntadaAtual.volume.processo\","
                        "\"documento.juntadaAtual.criadoPor\","
                        "\"documento.setorOrigem\","
                        "\"documento.setorOrigem.unidade\"]",
            "context": "{}"
        }

        # Adicionando as linhas de pesquisa condicionalmente
        conditions = []

        # Construindo as condições
        if content_formated:
            conditions.append("{\"conteudo\":\"like:%" + content_formated + "%\"}")

        if extension_formated:
            conditions.append("{\"extensao\":\"like:%" + extension_formated + "%\"}")

        if document_type_formated:
            conditions.append("{\"documento.tipoDocumento.id\":\"eq:" + document_type_formated + "\"}")

        if created_at_formated:
            conditions.append("{\"criadoEm\":\"gte:" + created_at_formated + "\"}")

        if created_on_formated:
            conditions.append("{\"criadoEm\":\"lte:" + created_on_formated + "\"}")

        if user_id_formated:
            conditions.append("{\"criadoPor.id\":\"eq:" + user_id_formated + "\"}")

        if sector_id_formated:
            conditions.append("{\"documento.setorOrigem.id\":\"eq:" + sector_id_formated + "\"}")

        # Adicionando as condições à query string
        if conditions:
            querystring["where"] += ",".join(conditions)
        querystring["where"] += "]}"
        payload = ""

        try:
            req: object = self.get(
                url,
                data=payload,
                params=querystring
            )
            data = json.loads(req.text)
            message = "Pasta obtida com sucesso"

        except Exception as e:
            print(f"Erro ao buscar Pasta: {e}")
            data = None
            message = "Erro ao buscar Pasta"

        return {
            "sucesso": True if (data is not None) else False,
            "dados": data,
            "mensagem": message
        }
