from anthropic import Anthropic
from dotenv import load_dotenv

# Charge les variables du fichier .env (notamment ANTHROPIC_API_KEY)
load_dotenv()

# Le client se connecte automatiquement avec la clé trouvée dans l'environnement
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Réponds juste par 'Connexion réussie !' si tu reçois ce message."}
    ]
)

print(response.content[0].text)