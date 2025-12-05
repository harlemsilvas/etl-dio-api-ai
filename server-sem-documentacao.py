# server.py
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 8080
DATA_FILE = "mock_data.json"

# Carrega ou inicializa o arquivo de dados
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({"users": []}, f, indent=2, ensure_ascii=False)

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, status, body=None, headers=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")  # Para testes locais
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        if body is not None:
            self.wfile.write(json.dumps(body, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_response(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

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
            content_len = int(self.headers.get("Content-Length", 0))
            try:
                post_body = self.rfile.read(content_len)
                new_user = json.loads(post_body.decode('utf-8'))

                # Validação mínima
                if "name" not in new_user:
                    self._send_response(400, {"error": "Missing 'name'"})
                    return

                data = load_data()
                # Gera novo ID
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
                updated_data = json.loads(body.decode('utf-8'))

                data = load_data()
                for i, user in enumerate(data["users"]):
                    if user["id"] == user_id:
                        # Mantém o ID original
                        updated_data["id"] = user_id
                        data["users"][i] = updated_data
                        save_data(data)
                        self._send_response(200, updated_data)
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
                before_len = len(data["users"])
                data["users"] = [u for u in data["users"] if u["id"] != user_id]
                after_len = len(data["users"])

                if after_len < before_len:
                    save_data(data)
                    self._send_response(204)  # No Content
                else:
                    self._send_response(404, {"error": "User not found"})
            except Exception as e:
                self._send_response(400, {"error": str(e)})
        else:
            self._send_response(404)

# Inicia o servidor
if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"✅ Servidor rodando em http://localhost:{PORT}")
        print(f"   Endpoints: GET/POST /users | GET/PUT/DELETE /users/<id>")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor encerrado.")