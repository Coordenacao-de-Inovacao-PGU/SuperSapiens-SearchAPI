SEARCH_DOCUMENT_TYPE_ROUTE = {
    "tags": ["Search"],
    "description": "Endpoint para pesquisa de tipos de documentos.",
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
            "description": "Consulta para a pesquisa de tipos de documentos."
        }
    ],
    "responses": {
        "200": {
            "description": "Sucesso ao pesquisar tipos de documentos.",
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
                                "document_type_id": {
                                    "type": "integer",
                                    "description": "ID do tipo de documento."
                                },
                                "document_type_name": {
                                    "type": "string",
                                    "description": "Nome do tipo de documento."
                                }
                            }
                        },
                        "description": "Lista de tipos de documentos correspondentes à consulta."
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
