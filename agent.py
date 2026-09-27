import os
import json
import ferramentas
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() #carrega o que tiver no .env para o ambiente

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

#Define a personalidade, escopo e regras do agente. O mesmo prompt do workshop foi usado nessa versão de testes, porém em pt-br.
system_prompt = """
Você é um agente de atendimento ao cliente de uma loja de eletrônicos online.

Seja prestativo, profissional e conciso. Utilize as ferramentas disponíveis para consultar informações do cliente e processar solicitações.

Diretrizes importantes:
- Sempre verifique o cliente utilizando a ferramenta de consulta de clientes (lookup_customer) antes de tomar qualquer providência.

- Utilize os dados da ferramenta para responder às perguntas - não solicite informações que você já possui.

- Seja cordial, mas eficiente.
"""

def executar_agente(mensagem_usuario):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": mensagem_usuario}
    ]

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        tools=ferramentas.TOOLS_SCHEMA, #type: ignore
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        messages.append(response_message)
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name #type: ignore
            function_args = json.loads(tool_call.function.arguments) #type: ignore
            function_to_call = ferramentas.FERRAMENTAS_DISPONIVEIS[function_name]
            function_response = function_to_call(**function_args)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })

        second_response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            tool_choice="auto"
        )
        return second_response.choices[0].message.content
    return response_message.content

if __name__ == "__main__":
    print("Protótipo 001 do Agente de Atendimento ao Cliente iniciado. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ("sair", "exit", "quit", "fechar"):
            print("Até logo! Obrigado por testar o protótipo 001 do Agente de Atendimento ao Cliente.")
            break

        if not pergunta.strip():
            continue

        resposta = executar_agente(pergunta)
        print(f"Agente: {resposta}\n")