LOGIN_ROUTE = {
    "tags": ["Login"],
    "description": "Endpoint para requisitar Login no SUPER SAPIENS.",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "id": "Login",
                "required": ["loginSapiens", "senhaSapiens"],
                "properties": {
                    "loginSapiens": {
                        "type": "string",
                        "description": "Login do usuário no Super Sapiens"
                    },
                    "senhaSapiens": {
                        "type": "string",
                        "description": "Senha do usuário no Super Sapiens"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Usuário autenticado com sucesso no SuperSAPIENS.",
            "schema": {
                "id": "LoginResponse",
                "properties": {
                    "status": {
                        "type": "integer",
                        "description": "Código de status da resposta"
                    },
                    "mensagem": {
                        "type": "string",
                        "description": "Mensagem de sucesso"
                    },
                    "valores": {
                        "type": "object",
                        "description": "Valores retornados",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "ID do usuário"
                            },
                            "nome": {
                                "type": "string",
                                "description": "Nome do usuário"
                            }
                        }
                    },
                    "token": {
                        "type": "string",
                        "description": "Token de acesso"
                    }
                }
            }
        },
        "401": {
            "description": "Autenticação do usuário no SAPIENS falhou.",
            "schema": {
                "id": "ErrorResponse",
                "properties": {
                    "status": {
                        "type": "integer",
                        "description": "Código de status da resposta"
                    },
                    "mensagem": {
                        "type": "string",
                        "description": "Mensagem de erro"
                    },
                    "valores": {
                        "type": "string",
                        "description": "Detalhes do erro"
                    }
                }
            }
        }
    }
}
