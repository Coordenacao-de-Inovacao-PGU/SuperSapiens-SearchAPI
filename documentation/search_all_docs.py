SEARCH_ALL_ROUTE = {
    "tags": ["Search"],
    "description": "Endpoint para pesquisa de documentos.",
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
            "name": "limit",
            "required": False,
            "type": "integer",
            "description": "Limite de documentos por página"
        },
        {
            "in": "query",
            "name": "page",
            "required": False,
            "type": "integer",
            "description": "Número da página"
        },
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "id": "Search",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Conteúdo para pesquisa"
                    },
                    "year": {
                        "type": "string",
                        "description": "Ano de pesquisa PARAMETRO OBRIGATORIO"
                    },
                    "extension": {
                        "type": "string",
                        "description": "Extensão do documento"
                    },
                    "unity": {
                        "type": "string",
                        "description": "Unidade"
                    },
                    "document_type": {
                        "type": "string",
                        "description": "Tipo de documento"
                    },
                    "created_at": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Data de criação do documento"
                    },
                    "created_on": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Data de criação do documento"
                    },
                    "created_by": {
                        "type": "string",
                        "description": "Criado por"
                    },
                    "sector": {
                        "type": "string",
                        "description": "Setor"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Documentos encontrados com sucesso.",
            "schema": {
                "id": "SearchResponse",
                "properties": {
                    "dados": {
                        "type": "object",
                        "description": "Dados dos documentos encontrados",
                        "properties": {
                            "entities": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "@context": {
                                            "type": "string",
                                            "description": "Contexto"
                                        },
                                        "@id": {
                                            "type": "string",
                                            "description": "ID"
                                        },
                                        "@type": {
                                            "type": "string",
                                            "description": "Tipo"
                                        },
                                        "assinado": {
                                            "type": "boolean",
                                            "description": "Documento assinado"
                                        },
                                        "atualizadoEm": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Data de atualização"
                                        },
                                        "criadoEm": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Data de criação"
                                        },
                                        "editavel": {
                                            "type": "boolean",
                                            "description": "Editável"
                                        },
                                        "extensao": {
                                            "type": "string",
                                            "description": "Extensão"
                                        },
                                        "fileName": {
                                            "type": "string",
                                            "description": "Nome do arquivo"
                                        },
                                        "hash": {
                                            "type": "string",
                                            "description": "Hash do arquivo"
                                        },
                                        "highlights": {
                                            "type": "string",
                                            "description": "Destaques"
                                        },
                                        "id": {
                                            "type": "integer",
                                            "description": "ID"
                                        },
                                        "interacoes": {
                                            "type": "integer",
                                            "description": "Interactions"
                                        },
                                        "mimetype": {
                                            "type": "string",
                                            "description": "Tipo MIME"
                                        },
                                        "nivelComposicao": {
                                            "type": "integer",
                                            "description": "Nível de composição"
                                        },
                                        "numeracaoSequencial": {
                                            "type": "integer",
                                            "description": "Numeração sequencial"
                                        },
                                        "tamanho": {
                                            "type": "integer",
                                            "description": "Tamanho do arquivo"
                                        },
                                        "uuid": {
                                            "type": "string",
                                            "description": "UUID"
                                        }
                                    }
                                }
                            },
                            "total": {
                                "type": "integer",
                                "description": "Total de documentos encontrados"
                            }
                        }
                    },
                    "mensagem": {
                        "type": "string",
                        "description": "Mensagem"
                    },
                    "sucesso": {
                        "type": "boolean",
                        "description": "Indicação de sucesso na operação"
                    }
                }
            }
        },
        "400": {
            "description": "Erro nos parâmetros da requisição",
            "schema": {
                "id": "ErrorResponse",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Indicação de sucesso na operação"
                    },
                    "message": {
                        "type": "string",
                        "description": "Mensagem de erro"
                    }
                }
            }
        },
        "401": {
            "description": "Não autorizado. O token de autenticação é inválido ou ausente."
        },
        "500": {
            "description": "Erro interno do servidor",
            "schema": {
                "id": "ErrorResponse",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Indicação de sucesso na operação"
                    },
                    "message": {
                        "type": "string",
                        "description": "Mensagem de erro"
                    }
                }
            }
        }
    }
}
