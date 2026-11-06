import gradio as gr
from agent import run_agent
from config import SYSTEM_PROMPT

#função q o gradio vai chamar qnd o usuário digitar algo + o histórico das msg
def chat_fn(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in history:
        # Filtra apenas role e content, ignorando metadata e outros campos do Gradio
        clean_msg = {
            "role": msg.get("role"),
            "content": msg.get("content")
        }
        messages.append(clean_msg)
    
    messages.append({"role": "user", "content": message})
    
    return run_agent(messages)

demo = gr.ChatInterface(
    fn=chat_fn,
    title="Agente de Atendimento",
    description="Tire dúvidas sobre clientes e pedidos."
)

if __name__ == "__main__":
    demo.launch()