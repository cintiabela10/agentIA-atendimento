import json
from config import client, MODEL, SYSTEM_PROMPT
from tools import TOOLS, TOOL_SCHEMAS
from typing import cast
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionFunctionToolParam

MAX_STEPS = 8 #evita q rode infinitamente

def run_agent(messages: list[dict]) -> str:
    """
    Executa o loop de tool calls até o modelo dar a resposta final.
    """
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=cast(list[ChatCompletionMessageParam], messages),
            tools=cast(list[ChatCompletionFunctionToolParam], TOOL_SCHEMAS),
            tool_choice="auto",
            max_tokens=800
        )
        msg = response.choices[0].message
        if not msg.tool_calls:
            return msg.content or ""
        
        messages.append(msg.model_dump(exclude_none=True))

        for call in msg.tool_calls:
            if call.type == "function":
                name = call.function.name
                args = json.loads(call.function.arguments or "{}")
                fn = TOOLS.get(name)
                result = fn(**args) if fn else {"error": f"Tool '{name}' não existe"}
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
    return "Ops! Desculpe, não consigo concluir a solicitação :("

def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Agente de atendimento. Digite 'sair' para encerrar.\n")
    while True:
        user = input("Você: ").strip()
        if user.lower() in {"sair", "exit", "quit", "fechar"}:
            break
        messages.append({"role": "user", "content": user})
        answer = run_agent(messages)
        print(f"Agente: {answer}\n")
        messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()