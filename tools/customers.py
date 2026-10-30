#Tools relacionadas com manipulação e/ou visualização de dados dos clientes
from db import load_db

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
