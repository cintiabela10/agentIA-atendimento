#Tools relacionadas com manipulação e/ou visualização de dados dos clientes
from db import load_db, save_db

def get_customer(customer_id: str) -> dict:
    """Busca um cliente pelo ID.
    Args:
        customer_id: ID do cliente (ex.: 'C-0001').
    Returns:
        Dados do cliente ou {'error': 'Cliente não encontrado}.
    """
    db = load_db()
    clientes = db.get("cliente", {})
    cliente = clientes.get(customer_id)
    if cliente is None:
        return {"error": f"Cliente com ID '{customer_id}' não encontrado."}
    return cliente

GET_CUSTOMER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_customer",
        "description": "Busca os dados de um cliente pelo ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "ID do cliente"}
            },
            "required": ["customer_id"],
        },
    },
}

def update_account_status(customer_id: str, new_status: str) -> dict:
    """
    Atualiza o status da conta de um cliente.
    Args:
    customer_id: ID do cliente (ex: 'C-0001').
    new_status: Novo status. Valores aceitos: 'ativa', 'suspensa', 'bloqueada'.
    """
    db = load_db()
    clientes = db.get("cliente", {})
    if customer_id not in clientes:
        return {"error": f"Cliente '{customer_id}' não encontrado."}
        
    if new_status.lower() not in ["ativa", "suspensa", "bloqueada"]:
        return {"error": "Status inválido. Use apenas 'ativa', 'suspensa' ou 'bloqueada'."}

    clientes[customer_id]["status_conta"] = new_status.lower()
    save_db(db)
    
    return {"message": f"Status da conta de {customer_id} atualizado para '{new_status}' com sucesso."}

UPDATE_ACCOUNT_STATUS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "update_account_status",
        "description": "Atualiza o status da conta de um cliente (ativa, suspensa, bloqueada).",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "new_status": {"type": "string", "enum": ["ativa", "suspensa", "bloqueada"]}
            },
            "required": ["customer_id", "new_status"]
        }
    }
}