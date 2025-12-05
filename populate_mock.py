# populate_mock.py
import json
import os

# Caminho do arquivo
DATA_FILE = "mock_data.json"

# Carrega os dados existentes (ou inicializa)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"users": []}

users = data["users"]

# Encontra o próximo ID disponível
existing_ids = {u["id"] for u in users}
next_id = max(existing_ids, default=0) + 1

# Novos usuários (3 registros)
new_users = [
    {
        "id": next_id,
        "name": "Carlos Mendes",
        "account": {
            "id": next_id,
            "number": "03.456789-1",
            "agency": "5060",
            "balance": 3200.75,
            "limit": 3000.0
        },
        "card": {
            "id": next_id,
            "number": "xxxx xxxx xxxx 3333",
            "limit": 8000.0
        },
        "features": [
            {"id": 1, "icon": "💸", "description": "PIX Instantâneo"},
            {"id": 2, "icon": "📱", "description": "App Mobile"},
            {"id": 3, "icon": "🏦", "description": "Conta Digital"}
        ],
        "news": [
            {"id": 1, "icon": "📈", "description": "Invista com poupança programada e cresça seu patrimônio."},
            {"id": 2, "icon": "🛡️", "description": "Seguro viagem: proteja suas férias por menos de R$5/dia."}
        ]
    },
    {
        "id": next_id + 1,
        "name": "Juliana Alves",
        "account": {
            "id": next_id + 1,
            "number": "04.987654-3",
            "agency": "7080",
            "balance": 890.50,
            "limit": 1200.0
        },
        "card": {
            "id": next_id + 1,
            "number": "xxxx xxxx xxxx 4444",
            "limit": 2500.0
        },
        "features": [
            {"id": 1, "icon": "💳", "description": "Cartão Virtual"},
            {"id": 2, "icon": "🔁", "description": "Transferências Ilimitadas"},
            {"id": 3, "icon": "📊", "description": "Relatórios Financeiros"}
        ],
        "news": [
            {"id": 1, "icon": "🎓", "description": "Crédito estudantil com condições especiais até dezembro."},
            {"id": 2, "icon": "🎁", "description": "Indique um amigo e ganhe R$30 em cashback!"}
        ]
    },
    {
        "id": next_id + 2,
        "name": "Roberto Lima",
        "account": {
            "id": next_id + 2,
            "number": "05.112233-9",
            "agency": "9010",
            "balance": 12500.00,
            "limit": 10000.0
        },
        "card": {
            "id": next_id + 2,
            "number": "xxxx xxxx xxxx 5555",
            "limit": 15000.0
        },
        "features": [
            {"id": 1, "icon": "💼", "description": "Conta PJ Simples"},
            {"id": 2, "icon": "🌐", "description": "Pagamentos Internacionais"},
            {"id": 3, "icon": "📅", "description": "Agendamento Recorrente"}
        ],
        "news": [
            {"id": 1, "icon": "🚀", "description": "Nova linha de crédito para empreendedores. Taxas a partir de 1.99%."},
            {"id": 2, "icon": "🤖", "description": "Assistente financeiro com IA: acompanhe seus gastos em tempo real."}
        ]
    }
]

# Adiciona os novos usuários
for user in new_users:
    users.append(user)

# Salva de volta no JSON
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ {len(new_users)} novos usuários adicionados ao '{DATA_FILE}'.")
print("IDs criados:", [u["id"] for u in new_users])