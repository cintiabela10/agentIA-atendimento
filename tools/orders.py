#Tools relacionadas com manipulação e/ou visualização de dados dos pedidos.
from db import load_db
from datetime import datetime

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

def check_refund_eligibility(customer_id: str, product_name: str, reason: str, order_id: str | None = None) -> dict:
    """Verifica se um cliente pode pedir reembolso de um produto.
    Padrões: 7 dias para arrependimento ou defeito; 30 dias para defeito oculto; Atrasos são sempre elegíveis.

    Args:
        customer_id: ID do cliente (ex.: 'C-0001').
        product_name: Nome do produto (ex.: 'Fone Bluetooth').
        reason: Motivo do reembolso (ex.: 'veio quebrado', 'desisti da compra').
        order_id: (Opcional) ID exato do pedido, se o cliente souber.
    """
    # 1. Busca o cliente e seus pedidos
    db = load_db()
    pedidos_cliente = db.get("pedido", {}).get(customer_id, [])
    if not pedidos_cliente:
        return {"error": f"Cliente '{customer_id}' não possui pedidos registrados."}

    # 2. Encontra o pedido (pelo ID exato ou pelo nome do produto)
    pedido = None
    if order_id:
        pedido = next((p for p in pedidos_cliente if p.get("id_pedido") == order_id), None)
    
    if not pedido:
        pedido = next((p for p in pedidos_cliente if product_name.lower() in p.get("item", "").lower()), None)

    # Se pedido for None, a função para.
    if not pedido:
        return {"error": f"Pedido do produto '{product_name}' não encontrado."}

    # 3. Aplica as regras de negócio
    motivo = reason.lower()
    status = pedido.get("status")
    item = pedido.get("item")

    # Regra: Atraso (Sempre elegível)
    if status == "atrasado":
        return {"eligible": True, "message": f"O pedido do '{item}' está atrasado. Reembolso autorizado."}

    # Regra: Só reembolsa se já foi entregue
    if status != "entregue":
        return {"eligible": False, "reason": f"Pedido com status '{status}'. Reembolso apenas para pedidos entregues ou atrasados."}

    # Cálculo de tempo desde a entrega (formato DD-MM-YYYY)
    data_entrega_str = pedido.get("data_entrega")
    if not data_entrega_str:
        return {"error": "Pedido entregue, mas sem data de entrega registrada no sistema."}
        
    dias_desde_entrega = (datetime.now() - datetime.strptime(data_entrega_str, "%d-%m-%Y")).days

    # Regra: Defeito (até 30 dias) / Arrependimento (até 7 dias)
    palavras_defeito = ["defeito", "quebrado", "quebrada", "rachado", "não funciona", "nao funciona", "avariado"]
    tem_defeito = any(p in motivo for p in palavras_defeito)

    if tem_defeito and dias_desde_entrega <= 30:
        return {"eligible": True, "message": f"Produto '{item}' com defeito dentro do prazo de 30 dias. Reembolso autorizado."}
    
    if dias_desde_entrega <= 7:
        return {"eligible": True, "message": f"Dentro do prazo de arrependimento de 7 dias para o '{item}'. Reembolso autorizado."}

    # Se chegou até aqui, não se encaixou em nenhuma regra de liberação
    motivo_recusa = "Prazo de 30 dias para defeito expirou." if tem_defeito else "O prazo de 7 dias para arrependimento expirou."
    return {"eligible": False, "reason": motivo_recusa}

CHECK_REFUND_ELIGIBILITY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "check_refund_eligibility",
        "description": "Chame sempre que o cliente pedir reembolso. Você DEVE fornecer o ID do cliente e o nome ou id do produto.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "ID do cliente, ex: 'C-0002'"},
                "product_name": {"type": "string", "description": "Nome do produto, ex: 'Teclado Gamer'"},
                "reason": {"type": "string", "description": "Motivo do reembolso dito pelo cliente"},
                "order_id": {"type": "string", "description": "Opcional. ID exato do pedido, ex: 'P-5521'."}
            },
            "required": ["customer_id", "product_name", "reason"]
        }
    }
}