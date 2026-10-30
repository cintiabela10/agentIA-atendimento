#Tools relacionadas com manipulação e/ou visualização de dados dos pedidos.
from db import load_db

def get_order_history(customer_id: str):
    """Busca o histórico de pedidos de um cliente.
    """
    db = load_db()
    pedidos = db.get("pedido", {})
    pedido = pedidos.get(customer_id)
    if pedido is None:
        return {"error": f"Cliente com ID '{customer_id}' não encontrado."}
    return pedido

GET_ORDER_HISTORY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_order_history",
        "description": "Busca o histórico de pedidos de um cliente.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "ID do cliente"}
            },
            "required": ["customer_id"],
        },
    },
}