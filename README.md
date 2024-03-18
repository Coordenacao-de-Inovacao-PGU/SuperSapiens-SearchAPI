# Projeto Flask API de Pesquisa

Este projeto é uma API desenvolvida com Flask para realizar pesquisas em um sistema chamado Super Sapiens. O Super Sapiens é uma plataforma administrativa que oferece diversas funcionalidades, incluindo pesquisa de documentos, usuários e unidades.

## Funcionalidades

### Autenticação ◀️
- A API permite que os usuários façam login utilizando o LDAP.
- O serviço de autenticação é fornecido pelo endpoint `auth/ldap_get_token`.

### Pesquisa 🔦
- A API fornece endpoints para pesquisar documentos, usuários, unidades e setores.
- Os tipos de pesquisa incluem pesquisa por nome de usuário, tipo de documento, unidade, setor, etc.

### Requisitos 📁

Este projeto requer as seguintes dependências Python:

- Flask
- Requests

Você pode instalar essas dependências executando:

```bash
pip install -r requirements.txt
```

Você pode rodar o servidor com o seguinte comando:

```bash
python app.py || flask run
```

## Documentacao 
A documentacao desse projeto pode ser acessada assim que o mesmo estiver no ar. Lembre-se de colocar o /apidocs ao final da URL
```bash
http://localhost:5000/apidocs
```

### Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações
