from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

tools = [
    {
        "name": "calculatrice",
        "description": "Effectue une opération arithmétique simple entre deux nombres.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["addition", "soustraction", "multiplication", "division"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "compter_caracteres",
        "description": "Compte le nombre de caractères dans un texte donné.",
        "input_schema": {
            "type": "object",
            "properties": {
                "texte": {"type": "string"}
            },
            "required": ["texte"]
        }
    }
]

def executer_calculatrice(operation, a, b):
    if operation == "addition": return a + b
    elif operation == "soustraction": return a - b
    elif operation == "multiplication": return a * b
    elif operation == "division": return a / b

def executer_compter_caracteres(texte):
    return len(texte)

# Registre qui relie le nom d'un outil à sa vraie fonction Python
outils_disponibles = {
    "calculatrice": executer_calculatrice,
    "compter_caracteres": executer_compter_caracteres
}

def executer_outil(nom_outil, input_outil):
    """Point d'entrée générique : appelle la bonne fonction selon le nom demandé."""
    fonction = outils_disponibles[nom_outil]
    return fonction(**input_outil)

def agent_boucle(question_utilisateur, max_iterations=5):
    messages = [{"role": "user", "content": question_utilisateur}]

    for i in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            tools=tools,
            messages=messages
        )

        print(f"\n--- Itération {i+1} — stop_reason: {response.stop_reason} ---")

        messages.append({"role": "assistant", "content": response.content})

        # Condition d'arrêt : le modèle a fini de raisonner, il a une réponse finale
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Sinon, on traite TOUS les appels d'outils demandés dans cette réponse
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  -> Appel outil: {block.name}({block.input})")
                    resultat = executer_outil(block.name, block.input)
                    print(f"  -> Résultat: {resultat}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(resultat)
                    })
            messages.append({"role": "user", "content": tool_results})

    return "Nombre maximum d'itérations atteint sans réponse finale."

# Test avec une question qui nécessite les deux outils
reponse = agent_boucle(
    "Combien font 47 multiplié par 12 ? Et combien de caractères contient le mot 'multiplication' ?"
)
print("\n=== RÉPONSE FINALE ===")
print(reponse)