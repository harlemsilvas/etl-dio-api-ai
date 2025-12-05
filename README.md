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
.
├── mock_data.json # Banco de dados em JSON (usuários, contas, features, notícias)
├── server.py # Servidor REST com CRUD (GET/POST/PUT/DELETE)
├── populate_mock.py # Script para adicionar +3 usuários com ícones em emoji 💸📈
├── SDW2023.csv # Lista de IDs para processamento (ex: UserID)
└── README.md # Este arquivo 📄


---

## 🚀 Como Rodar Localmente

### 1. Pré-requisitos
- [Python 3.8+](https://www.python.org/)
- (Opcional) WSL, macOS ou Linux — funciona também no Windows nativo

### 2. Clone este repositório
```bash
git clone https://github.com/seu-usuario/sdw2023-local.git
cd sdw2023-local

3. Inicie o servidor

python server.py

➡️ Servidor rodando em: http://localhost:8080

✅ Escuta em 0.0.0.0, então é acessível tanto do WSL quanto do navegador do Windows.

4. Teste os endpoints

Método	Endpoint	Descrição
`GET`	`/users`	Lista todos os usuários
`GET`	`/users/1`	Retorna usuário com ID = 1
`POST`	`/users`	Cria novo usuário
`PUT`	`/users/1`	Atualiza usuário com ID = 1
`DELETE`	`/users/1`	Remove usuário com ID = 1

Exemplo com curl:

curl http://localhost:8080/users/1

5. (Opcional) Popule com +3 usuários

python populate_mock.py

→ Adiciona 3 novos registros com ícones em emoji (ex: 📈, 🛡️, 🤖), mantendo a estrutura do domínio original.


📦 Integração com Seus Projetos
Você pode reutilizar este servidor como backend para:

Scripts de automação com OpenAI (ex: geração de notícias personalizadas);
Aplicações frontend (Angular, React, Flutter, etc.);
Testes de integração, pipelines CI/CD locais ou demos.
Basta apontar sua URL para:

sdw2023_api_url = 'http://localhost:8080'

🔗 Referências Oficiais
📚 Repositório Original (DIO)
🖼️ Mock Backup (GitHub Pages)
🎨 Figma do App (Santander Dev Week)
📜 Licença
Este projeto é open-source e inspirado no trabalho da Digital Innovation One.
Sinta-se livre para copiar, modificar e compartilhar — só não esqueça de dar os devidos créditos! 😊

✨ “A inovação nasce da colaboração. Compartilhe seu aprendizado.”

