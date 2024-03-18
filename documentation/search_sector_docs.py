SEARCH_SECTOR_ROUTE = {
    "tags": ["Search"],
    "description": "Endpoint para pesquisa de setores.",
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
            "description": "Consulta para a pesquisa do setor."
        },
        {
            "in": "query",
            "name": "unity_id",
            "required": True,
            "type": "string",
            "description": "ID da unidade para a qual o setor está sendo pesquisado."
        }
    ],
    "responses": {
        "200": {
            "description": "Sucesso ao pesquisar o setor.",
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
                                "sector_id": {
                                    "type": "integer",
                                    "description": "ID do setor."
                                },
                                "sector_name": {
                                    "type": "string",
                                    "description": "Nome do setor."
                                }
                            }
                        },
                        "description": "Lista de setores correspondentes à consulta."
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
