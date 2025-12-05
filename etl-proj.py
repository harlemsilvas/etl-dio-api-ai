import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Configuração - URL da API local pois a do bottcamp não está acessível
sdw2023_api_url = 'http://localhost:8080/'

# Carregar IDs
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print("IDs carregados:", user_ids)

# Obter usuários
def get_user(user_id):
    try:
        response = requests.get(f'{sdw2023_api_url}/users/{user_id}', timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ Erro ao buscar usuário {user_id}: {e}")
        return None

users = [user for uid in user_ids if (user := get_user(uid)) is not None]
print(f"✅ {len(users)} usuários carregados.")

# Salvar em JSON
with open('extracted_users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=2, ensure_ascii=False)
print("Dados salvos em 'extracted_users.json'.")

# Configurar OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or 'chave-da-sua-api-aqui'
if not api_key or api_key == 'chave-da-sua-api-aqui':
    raise ValueError("❌ Chave da API não encontrada. Verifique seu arquivo .env")
print("✅ Chave da API carregada com sucesso!")

client = OpenAI(api_key=api_key)

def generate_ai_news(user_name: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em marketing bancário."},
                {"role": "user", "content": f"Crie uma mensagem para {user_name} sobre a importância dos investimentos (máximo de 100 caracteres)."}
            ],
            max_tokens=30,
            temperature=0.7
        )
        return completion.choices[0].message.content.strip('"')
    except Exception as e:
        print(f"⚠️ Erro ao gerar notícia para {user_name}: {e}")
        return "Invista com sabedoria para construir seu futuro financeiro."

# Função para atualizar usuário
def update_user(user):
    try:
        response = requests.put(
            f'{sdw2023_api_url}/users/{user["id"]}',
            json=user,
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro ao atualizar usuário {user.get('id', '?')}: {e}")
        return False

# Processar (ex: só os 2 primeiros para teste)
for user in users[:2]:  # 👈 limite explícito
    user_id = user.get('id')
    user_name = user.get('name', 'Usuário')
    
    if user_id is None:
        print(f"⚠️ Usuário sem 'id': {user_name}")
        continue

    # Garante que 'news' seja uma lista
    if 'news' not in user or user['news'] is None:
        user['news'] = []

    # Gera e adiciona notícia
    news_text = generate_ai_news(user_name)
    user['news'].append({
        "icon": "🤖",
        "description": news_text
    })
    print(f"📝 Nova notícia para {user_name}: {news_text}")

    # Atualiza na API
    success = update_user(user)
    print(f"{'✅' if success else '❌'} Usuário {user_name} (ID: {user_id}) atualizado: {success}")