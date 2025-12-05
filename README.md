# etl-dio-api-ai
# Santander Dev Week 2023 — API Local (Mock + Servidor REST)

> ✨ **Uma implementação local e offline da API da Santander Dev Week 2023**, com suporte a operações **CRUD completas** e dados simulados em JSON. Ideal para desenvolvedores que desejam continuar explorando, aprendendo e integrando soluções mesmo após o encerramento do ambiente oficial.

Este projeto é uma **réplica funcional e autocontida** da [API original](https://github.com/digitalinnovationone/santander-dev-week-2023-api), desenvolvida durante a Santander Dev Week 2023 pela [Digital Innovation One](https://digitalinnovation.one/), mas agora **totalmente executável em `localhost`**, sem dependência de serviços externos.

---

## 🎯 Objetivo

- Permitir o uso contínuo dos exercícios propostos (ex: integração com OpenAI para geração de notícias personalizadas) mesmo após o desligamento do endpoint oficial (`https://sdw-2023-prd.up.railway.app`);
- Oferecer um ambiente de desenvolvimento local com **persistência em JSON** e **servidor REST em Python**;
- Servir como base para estudos em integração de APIs, automação e arquitetura de microsserviços.

---

## 🧱 Estrutura do Projeto
```bash
sdw2023-local/
├── mock_data.json          # "Banco de dados" em JSON (persistência local)
├── server.py               # Servidor REST com CRUD (GET/POST/PUT/DELETE)
├── populate_mock.py        # Script para adicionar +3 usuários com ícones em emoji (💸📈🤖)
├── SDW2023.csv             # Lista de IDs (ex: UserID) para processamento em lote
├── .gitignore              # Ignora arquivos temporários (ex: *.pyc, __pycache__)
├── README.md               # Este arquivo 📄
└── LICENSE                 # Licença MIT (opcional)
```

---

## 🚀 Como Rodar Localmente

### 1. Pré-requisitos

- [Python 3.8+](https://www.python.org/)
- (Opcional) WSL, macOS ou Linux — funciona também no Windows nativo

```bash
python --version
# Saída esperada: Python 3.10.12 (ou similar)
```

---

### 2. Clone este repositório
```bash
git clone https://github.com/harlemsilvas/etl-dio-api-ai.git
cd etl-dio-api-ai

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/WSL/macOS
# venv\Scripts\activate   # Windows (PowerShell/CMD)
```

---
### 3. Inicie o servidor

```bash
python server.py
```

➡️ Servidor rodando em: http://localhost:8080

✅ Escuta em 0.0.0.0, então é acessível tanto do WSL quanto do navegador do Windows.

---

### 4. Teste os endpoints

### ✅ Endpoints Suportados

| Método   | Endpoint         | Descrição                     | Exemplo de Uso                          |
|----------|------------------|-------------------------------|------------------------------------------|
| `GET`    | `/users`         | Lista todos os usuários       | `GET /users`                             |
| `GET`    | `/users/{id}`    | Retorna um usuário pelo ID    | `GET /users/1`                           |
| `POST`   | `/users`         | Cria um novo usuário          | `POST /users` + JSON no corpo            |
| `PUT`    | `/users/{id}`    | Atualiza um usuário existente | `PUT /users/1` + JSON atualizado         |
| `DELETE` | `/users/{id}`    | Remove um usuário             | `DELETE /users/1`                        |

> 📝 **Observações**  
> - Todos os endpoints retornam/consomem `application/json`.  
> - IDs inválidos (`/users/999`) retornam `404 Not Found`.  
> - Corpo de requisição malformado retorna `400 Bad Request`.

Exemplo com curl:

```bash
# Listar todos
curl http://localhost:8080/users

# Buscar usuário 1
curl http://localhost:8080/users/1

# Criar novo usuário
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria Souza","account":{"number":"00.000000-0","agency":"9999","balance":0,"limit":500}}'
```

---

### 5. (Opcional) Popule com +3 usuários

```bash
python populate_mock.py
```

→ Adiciona 3 novos registros com ícones em emoji (ex: 📈, 🛡️, 🤖), mantendo a estrutura do domínio original.

---

## 🔗 Integração com Seus Projetos

Esta API local é compatível **100% com o contrato da API original da Santander Dev Week 2023**, o que permite reutilizá-la como *drop-in replacement* em qualquer projeto existente — especialmente os desenvolvidos durante o evento.

✅ **Use para**:
- Executar scripts de automação (ex: integração com OpenAI para geração de notícias personalizadas);
- Desenvolver ou testar frontends (Angular, React, Flutter, Android, iOS) usando `http://localhost:8080` como base;
- Substituir o endpoint oficial (`https://sdw-2023-prd.up.railway.app`) em demos, apresentações ou entrevistas técnicas;
- Estudar padrões REST, CRUD, serialização JSON e arquitetura de domínio.

🔧 Basta atualizar a variável de URL no seu código:
```python
sdw2023_api_url = 'http://localhost:8080'  # ✅ Funciona offline, sem dependência externa
```


## 📦 Integração com Seus Projetos
✅ **Você pode reutilizar este servidor como backend para**:

- Scripts de automação com OpenAI (ex: geração de notícias personalizadas);
- Aplicações frontend (Angular, React, Flutter, etc.);
- Testes de integração, pipelines CI/CD locais ou demos.
- Basta apontar sua URL para:
---
```python
sdw2023_api_url = 'http://localhost:8080'
```
---

## 📚 Referências Oficiais do projeto Dio Santander

| Recurso | Link | Descrição |
|--------|------|-----------|
| **Repositório Oficial (Java 17 + Spring Boot 3)** | [`github.com/digitalinnovationone/santander-dev-week-2023-api`](https://github.com/digitalinnovationone/santander-dev-week-2023-api) | Código-fonte aberto da API original, com OpenAPI/Swagger integrado |
| **Endpoint de Produção (desativado)** | `https://sdw-2023-prd.up.railway.app` | ⚠️ Serviço temporário no Railway — fora do ar desde o encerramento do evento |
| **Mock de Backup (JSON estático)** | [`digitalinnovationone.github.io/.../find_one.json`](https://digitalinnovationone.github.io/santander-dev-week-2023-api/mocks/find_one.json) | Versão estática do usuário exemplo — útil para validação de contrato |
| **Figma (UI/UX do App Santander)** | [Figma — Santander Dev Week 2023](https://www.figma.com/file/89Lwew6J8dK5JzVJc4J6Zq/Santander-Dev-Week-2023) | Projeto de interface utilizado na abstração do domínio da API |
| **Tecnologias Utilizadas (Oficiais)** | — | Java 17 • Spring Boot 3 • Spring Data JPA • OpenAPI (Swagger) • Railway |

> 💡 *"Este é um código-fonte aberto. Sintam-se à vontade para cloná-lo, modificá-lo e executar localmente ou onde acharem mais interessante!"*  
> — [Digital Innovation One](https://digitalinnovation.one/)


###📜 Licença
Este projeto é open-source e inspirado no trabalho da Digital Innovation One.
Sinta-se livre para copiar, modificar e compartilhar — só não esqueça de dar os devidos créditos! 😊

✨ “A inovação nasce da colaboração. Compartilhe seu aprendizado.”

