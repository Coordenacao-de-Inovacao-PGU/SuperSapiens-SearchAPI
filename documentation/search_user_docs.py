SEARCH_USER_BY_NAME_ROUTE = {
    "tags": ["Search"],
    "description": "Endpoint para pesquisa de usuário por nome.",
    "parameters": [
        {
            "in": "header",
            "name": "Authorization",
            "required": True,
            "type": "string",
            "description": "Token JWT de autenticação. Utilize o prefixo Bearer <JWT> !"

        },
        {
            "in": "query",
            "name": "q",
            "required": True,
            "type": "string",
            "description": "Consulta para a pesquisa do usuário por nome."
        }
    ],
    "responses": {
        "200": {
            "description": "Sucesso ao pesquisar o usuário por nome.",
            "schema": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Indica se a solicitação foi bem-sucedida."
                    },
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "user_id": {
                                    "type": "integer",
                                    "description": "ID do usuário."
                                },
                                "user_name": {
                                    "type": "string",
                                    "description": "Nome do usuário."
                                }
                            }
                        },
                        "description": "Lista de usuários correspondentes à consulta."
                    }
                }
            }
        },
        "400": {
            "description": "Erro de solicitação inválida.",
            "schema": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Indica se a solicitação foi bem-sucedida."
                    },
                    "message": {
                        "type": "string",
                        "description": "Descrição do erro."
                    }
                }
            }
        },
        "500": {
            "description": "Erro interno do servidor.",
            "schema": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Indica se a solicitação foi bem-sucedida."
                    },
                    "message": {
                        "type": "string",
                        "description": "Descrição do erro."
                    }
                }
            }
        }
    }
}
