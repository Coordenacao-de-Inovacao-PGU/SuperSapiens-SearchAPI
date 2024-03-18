SEARCH_UNITY_ROUTE = {
    "tags": ["Search"],
    "description": "Endpoint para pesquisa de unidades.",
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
            "description": "Consulta para a pesquisa da unidade."
        }
    ],
    "responses": {
        "200": {
            "description": "Sucesso ao pesquisar a unidade.",
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
                                "unity_id": {
                                    "type": "integer",
                                    "description": "ID da unidade."
                                },
                                "unity_name": {
                                    "type": "string",
                                    "description": "Nome da unidade."
                                }
                            }
                        },
                        "description": "Lista de unidades correspondentes à consulta."
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
