import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
print(f"Chave lida: {os.environ.get('GROQ_API_KEY')}") #temporário só p testar

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "qwen/qwen3.8-27b"

SYSTEM_PROMPT = """Você é um agente de atendimento ao cliente de uma loja online.
Regras:
- Use as ferramentas disponíveis; nunca invente dados.
- Sempre consulte o cliente pelo ID antes de responder sobre pedidos.
- Se não encontrar o cliente, peça o ID novamente.
- Ao abrir um chamado, informe o protocolo gerado.
Seja cordial e objetivo.
"""