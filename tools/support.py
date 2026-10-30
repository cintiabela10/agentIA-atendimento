#Tools relacionadas ao suporte
import uuid
from datetime import datetime
from db import load_db, save_db

def open_support_ticket(customer_id: str, description: str) -> dict:
    """Abre um chamado de suporte para um cliente.
    Args:
        customer_id: ID do cliente.
        description: Descrição do problema.
    Returns:
        {"protocol": "...", "status": "aberto"} ou {"error": "..."}.
    """
    db = load_db()
    #Vê se o cliente existe primeiro
    clientes = db.get("cliente", {})
    if customer_id not in clientes:
        return {"error": f"Cliente com ID '{customer_id}' não encontrado."}
    #gera o protocolo
    protocol = f"TK-{uuid.uuid4().hex[:8].upper()}"
    
    if "chamado" not in db:
        db["chamado"] = {}
    
    db["chamado"][protocol] = {
        "customer_id": customer_id,
        "description": description,
        "status": "aberto",
        "created_at": datetime.utcnow().isoformat(),
    }

    save_db(db)
    return {"protocolo": protocol, "status": "aberto"}

OPEN_TICKET_SCHEMA = {
    "type": "function",
    "function": {
        "name": "open_support_ticket",
        "description": "Abre um chamado de suporte para um cliente.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "ID do cliente"},
                "description": {"type": "string", "description": "Descrição do problema"}
                },
            "required": ["customer_id", "description"],
        },
    },
}