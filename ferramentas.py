#Lista de ferramentas que o agente pode usar.
from pathlib import Path
import json

#carregar o banco de dados (base_dados.json) e deixa-lo disponível até o programa encerrar. O caminho_base é pra evitar que quebre caso rode o script num arquivo diferente.
CAMINHO_BASE = Path(__file__).parent / "base_dados.json"

def _ler_base():
    with open(CAMINHO_BASE, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar_base(dados):
    with open(CAMINHO_BASE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# ---------------------------------------------------------------
# FUNÇÕES DAS FERRAMENTAS
# ---------------------------------------------------------------

def buscar_cliente(id_cliente: str) -> str:
    dados = _ler_base()
    clientes = dados.get("cliente", {}).get(id_cliente)

    if clientes is None:
        return f"Cliente {id_cliente} não encontrado :("
    return(
        f"""
        Cliente: {clientes['nome']}
        Email: {clientes['email']}
        Telefone: {clientes['telefone']}
        Status da Conta: {clientes['status_conta']}
        """
    )

def obter_historico_pedido(id_cliente: str) -> str:
    dados = _ler_base()
    pedidos = dados.get("pedido", {}).get(id_cliente)

    if not pedidos:
        return f"Nenhum pedido encontrado para o cliente {id_cliente}."
    lista_pedidos = []
    for pedido in pedidos:
        info_pedido = (
            f"Pedido {pedido['id_pedido']}: {pedido['item']} - R$ {pedido['preco']:.2f}"
            f"[{pedido['status']}] Data de Compra: {pedido['data_pedido']}"
        )
        if pedido.get("data_entrega"):
            info_pedido += f"Entrega: {pedido['data_entrega']}"
        elif pedido.get("entrega_estimada"):
            info_pedido += f"Entrega Estimada: {pedido['entrega_estimada']}"
        info_pedido += f"Código de Rastreio: {pedido['codigo_rastreio']}"
        lista_pedidos.append(info_pedido)
    return "\n".join(lista_pedidos)

def abrir_chamado_suporte(motivo: str) -> str:
    dados = _ler_base()
    dados.setdefault("chamado", [])
    protocolo = f"#{len(dados['chamado']) + 1:06d}"
    dados["chamado"].append({"protocolo": protocolo, "motivo": motivo})
    _salvar_base(dados)
    return f"Chamado aberto. Protocolo: {protocolo}"

# ---------------------------------------------------------------
# MAPEAMENTO (nome da tool → função real)
# ---------------------------------------------------------------
FERRAMENTAS_DISPONIVEIS = {
    "buscar_cliente": buscar_cliente,
    "obter_historico_pedido": obter_historico_pedido,
    "abrir_chamado_suporte": abrir_chamado_suporte,
}

# ---------------------------------------------------------------
# SCHEMA (descrição para o modelo)
# ---------------------------------------------------------------

TOOLS_SCHEMA = [
    {
    "type": "function",
    "function": {
        "name": "buscar_cliente",
        "description": "Busca dados de um cliente pelo seu ID",
        "parameters": {
            "type": "object",
            "properties": {
                "id_cliente": {"type": "string", "description": "ID do cliente"}
            },
            "required": ["id_cliente"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "obter_historico_pedido",
            "description": "Obtém o histórico de pedidos de um cliente pelo seu ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_cliente": {"type": "string", "description": "ID do cliente"}
                },
                "required": ["id_cliente"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "abrir_chamado_suporte",
            "description": "Abre um chamado de suporte técnico",
            "parameters": {
                "type": "object",
                "properties": {
                    "motivo": {"type": "string", "description": "Motivo do chamado"}
                },
                "required": ["motivo"]
            }
        }
    }
]