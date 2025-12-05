# server.py
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from pathlib import Path

PORT = 8080
DATA_FILE = "mock_data.json"

# --- DADOS INICIAIS (se mock_data.json não existir) ---
INITIAL_DATA = {
    "users": [
        {
            "id": 1,
            "name": "Devweekerson",
            "account": {
                "id": 1,
                "number": "01.097954-4",
                "agency": "2030",
                "balance": 624.12,
                "limit": 1000.0
            },
            "card": {
                "id": 1,
                "number": "xxxx xxxx xxxx 1111",
                "limit": 2000.0
            },
            "features": [
                {"id": 1, "icon": "💸", "description": "PIX"},
                {"id": 2, "icon": "📱", "description": "Pagar"},
                {"id": 3, "icon": "🔄", "description": "Transferir"},
                {"id": 4, "icon": "🏦", "description": "Conta Corrente"},
                {"id": 5, "icon": "💳", "description": "Cartões"}
            ],
            "news": [
                {
                    "id": 2,
                    "icon": "🛡️",
                    "description": "Santander Seguro Casa, seu faz-tudo. Mais de 50 serviços pra você. Confira!"
                },
                {
                    "id": 1,
                    "icon": "💰",
                    "description": "O Santander tem soluções de crédito sob medida pra você. Confira!"
                }
            ]
        }
    ]
}

# --- INICIALIZA O ARQUIVO DE DADOS ---
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(INITIAL_DATA, f, indent=2, ensure_ascii=False)

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- HTML DO SWAGGER UI (EMBEDADO) ---
SWAGGER_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Swagger UI - SDW2023 Local API</title>
  <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
  <style> body { margin: 0; } </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      const spec = {
        openapi: "3.0.3",
        info: {
          title: "Santander Dev Week 2023 — API Local (Python)",
          description: "✨ Réplica local da API da Santander Dev Week 2023. Feita em Python puro, 100% offline.\\nBaseada no repositório oficial da DIO.",
          version: "1.0.0",
          contact: { name: "Harlem Silva", url: "https://github.com/harlemsilvas/etl-dio-api-ai" }
        },
        servers: [{ url: "http://localhost:8080", description: "Localhost" }],
        tags: [{ name: "users", description: "CRUD de usuários" }],
        paths: {
          "/users": {
            get: {
              tags: ["users"],
              summary: "Lista todos os usuários",
              responses: { 200: { description: "OK", content: { "application/json": { schema: { type: "array", items: { $ref: "#/components/schemas/User" } } } } } }
            },
            post: {
              tags: ["users"],
              summary: "Cria um novo usuário",
              requestBody: { required: true, content: { "application/json": { schema: { $ref: "#/components/schemas/UserInput" } } } },
              responses: {
                201: { description: "Criado", content: { "application/json": { schema: { $ref: "#/components/schemas/User" } } } },
                400: { description: "Requisição inválida" }
              }
            }
          },
          "/users/{id}": {
            get: {
              tags: ["users"],
              summary: "Retorna um usuário pelo ID",
              parameters: [{ name: "id", in: "path", required: true, schema: { type: "integer" } }],
              responses: {
                200: { description: "OK", content: { "application/json": { schema: { $ref: "#/components/schemas/User" } } } },
                404: { description: "Não encontrado" }
              }
            },
            put: {
              tags: ["users"],
              summary: "Atualiza um usuário",
              parameters: [{ name: "id", in: "path", required: true, schema: { type: "integer" } }],
              requestBody: { required: true, content: { "application/json": { schema: { $ref: "#/components/schemas/UserInput" } } } },
              responses: {
                200: { description: "Atualizado", content: { "application/json": { schema: { $ref: "#/components/schemas/User" } } } },
                400: { description: "Requisição inválida" },
                404: { description: "Não encontrado" }
              }
            },
            delete: {
              tags: ["users"],
              summary: "Remove um usuário",
              parameters: [{ name: "id", in: "path", required: true, schema: { type: "integer" } }],
              responses: {
                204: { description: "Removido com sucesso" },
                404: { description: "Não encontrado" }
              }
            }
          }
        },
        components: {
          schemas: {
            User: {
              type: "object",
              required: ["id", "name", "account", "card", "features", "news"],
              properties: {
                id: { type: "integer" },
                name: { type: "string" },
                account: { $ref: "#/components/schemas/Account" },
                card: { $ref: "#/components/schemas/Card" },
                features: { type: "array", items: { $ref: "#/components/schemas/Feature" } },
                news: { type: "array", items: { $ref: "#/components/schemas/News" } }
              }
            },
            UserInput: {
              type: "object",
              required: ["name", "account", "card"],
              properties: {
                name: { type: "string" },
                account: { $ref: "#/components/schemas/AccountInput" },
                card: { $ref: "#/components/schemas/CardInput" },
                features: { type: "array", items: { $ref: "#/components/schemas/Feature" }, default: [] },
                news: { type: "array", items: { $ref: "#/components/schemas/News" }, default: [] }
              }
            },
            Account: {
              type: "object",
              required: ["id", "number", "agency", "balance", "limit"],
              properties: {
                id: { type: "integer" },
                number: { type: "string" },
                agency: { type: "string" },
                balance: { type: "number" },
                limit: { type: "number" }
              }
            },
            AccountInput: {
              type: "object",
              required: ["number", "agency", "balance", "limit"],
              properties: {
                number: { type: "string" },
                agency: { type: "string" },
                balance: { type: "number" },
                limit: { type: "number" }
              }
            },
            Card: {
              type: "object",
              required: ["id", "number", "limit"],
              properties: {
                id: { type: "integer" },
                number: { type: "string" },
                limit: { type: "number" }
              }
            },
            CardInput: {
              type: "object",
              required: ["number", "limit"],
              properties: {
                number: { type: "string" },
                limit: { type: "number" }
              }
            },
            Feature: {
              type: "object",
              required: ["id", "icon", "description"],
              properties: {
                id: { type: "integer" },
                icon: { type: "string" },
                description: { type: "string" }
              }
            },
            News: {
              type: "object",
              required: ["id", "icon", "description"],
              properties: {
                id: { type: "integer" },
                icon: { type: "string" },
                description: { type: "string" }
              }
            }
          }
        }
      };
      SwaggerUIBundle({
        spec: spec,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, status, body=None, content_type="application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        if body is not None:
            if isinstance(body, str):
                self.wfile.write(body.encode('utf-8'))
            else:
                self.wfile.write(json.dumps(body, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_response(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # ✅ SWAGGER UI embutido
        if path in ("/", "/docs", "/swagger", "/swagger.html"):
            self._send_response(200, SWAGGER_HTML, "text/html; charset=utf-8")
            return

        # 📋 Usuários
        if path == "/users":
            data = load_data()
            self._send_response(200, data["users"])
        elif path.startswith("/users/"):
            try:
                user_id = int(path.split("/")[2])
                data = load_data()
                user = next((u for u in data["users"] if u["id"] == user_id), None)
                if user:
                    self._send_response(200, user)
                else:
                    self._send_response(404, {"error": "User not found"})
            except (IndexError, ValueError):
                self._send_response(400, {"error": "Invalid user ID"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if self.path == "/users":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                new_user = json.loads(body.decode('utf-8'))

                if "name" not in new_user:
                    self._send_response(400, {"error": "Missing 'name'"})
                    return

                data = load_data()
                max_id = max([u["id"] for u in data["users"]], default=0)
                new_user["id"] = max_id + 1
                data["users"].append(new_user)
                save_data(data)
                self._send_response(201, new_user)
            except Exception as e:
                self._send_response(400, {"error": str(e)})
        else:
            self._send_response(404)

    def do_PUT(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split("/")[2])
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                updated_user = json.loads(body.decode('utf-8'))

                data = load_data()
                for i, user in enumerate(data["users"]):
                    if user["id"] == user_id:
                        updated_user["id"] = user_id  # mantém o ID
                        data["users"][i] = updated_user
                        save_data(data)
                        self._send_response(200, updated_user)
                        return
                self._send_response(404, {"error": "User not found"})
            except Exception as e:
                self._send_response(400, {"error": str(e)})
        else:
            self._send_response(404)

    def do_DELETE(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split("/")[2])
                data = load_data()
                before = len(data["users"])
                data["users"] = [u for u in data["users"] if u["id"] != user_id]
                after = len(data["users"])
                if after < before:
                    save_data(data)
                    self._send_response(204)
                else:
                    self._send_response(404, {"error": "User not found"})
            except Exception as e:
                self._send_response(400, {"error": str(e)})
        else:
            self._send_response(404)

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
        print(f"✅ Servidor rodando em http://localhost:{PORT}")
        print(f"   • API:      http://localhost:{PORT}/users")
        print(f"   • Swagger:  http://localhost:{PORT}/docs  (ou /swagger)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor encerrado.")