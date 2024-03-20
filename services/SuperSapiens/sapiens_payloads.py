def search_all_query_string(limit, offset, data_search):
    # Construcao da QueryString
    querystring = {
        "where": "{\"andX\":[",
        "limit": limit,
        "offset": str(offset),
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
    if data_search['content']:
        conditions.append("{\"conteudo\":\"like:%" + data_search['content'] + "%\"}")

    if data_search['extension']:
        conditions.append("{\"extensao\":\"like:%" + data_search['extension'] + "%\"}")

    if data_search['document_type']:
        conditions.append("{\"documento.tipoDocumento.id\":\"eq:" + data_search['document_type'] + "\"}")

    if data_search['created_at']:
        conditions.append("{\"criadoEm\":\"gte:" + data_search['created_at'] + "\"}")

    if data_search['created_on']:
        conditions.append("{\"criadoEm\":\"lte:" + data_search['created_on'] + "\"}")

    if data_search['user_id']:
        conditions.append("{\"criadoPor.id\":\"eq:" + data_search['user_id'] + "\"}")

    if data_search['sector_id']:
        conditions.append("{\"documento.setorOrigem.id\":\"eq:" + data_search['sector_id'] + "\"}")

    # Adicionando as condições à query string
    if conditions:
        querystring["where"] += ",".join(conditions)
    querystring["where"] += "]}"

    return querystring


def search_sector_querystring(query, unity_id, limit, offset):
    querystring = {
        "where":
            "{\"parent\":\"isNotNull\","
            "\"unidade.id\":\"eq:" + str(unity_id) + "\","
                                                     "\"orX\":[{\"andX\":"
                                                     "[{\"nome\":\"like:%" + str(query) + "%\"}]},"
                                                                                          "{\"andX\":[{\"sigla\":\"like:%" + str(
                query) + "%\"}]}]}",
        "limit": str(limit), "offset": str(offset), "order": "{}", "populate": "[\"unidade\",\"parent\"]",
        "context": "{}"}
    return querystring


def search_unity_querystring(query, limit, offset):
    querystring = {
        "where":
            "{\"parent\":\"isNull\","
            "\"orX\":[{\"andX\":"
            "[{\"nome\":\"like:%" + str(query) + "%\"}]},"
                                                 "{\"andX\":"
                                                 "[{\"sigla\":\"like:%" + str(query) + "%\"}]}]}",
        "limit": str(limit), "offset": str(offset), "order": "{}", "populate": "[]", "context": "{}"}
    return querystring


def search_user_by_name_querystring(query, limit, offset):
    querystring = {"where":
                       "{\"andX\":"
                       "[{\"nome\":\"like:%" + str(query) + "%\"}]}",
                   "limit": str(limit),
                   "offset": str(offset),
                   "order": "{}",
                   "populate": "[\"populateAll\",\"colaborador\",\"colaborador.cargo\","
                               "\"colaborador.modalidadeColaborador\"]",
                   "context": "{}"}
    return querystring


def search_document_type_querystring(query, limit, offset):
    querystring = {"where":
                       "{\"andX\":"
                       "[{\"nome\":\"like:%" + str(query) + "%\"}]}",
                   "limit": str(limit),
                   "offset": str(offset),
                   "order": "{}",
                   "populate": "[]", "context": "{}"}
    return querystring
