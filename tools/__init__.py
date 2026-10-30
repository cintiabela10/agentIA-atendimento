from .customers import get_customer, GET_CUSTOMER_SCHEMA
from .orders import get_order_history, GET_ORDER_HISTORY_SCHEMA
from .support import open_support_ticket, OPEN_TICKET_SCHEMA

TOOLS = {
    "get_customer": get_customer,
    "get_order_history": get_order_history,
    "open_support_ticket": open_support_ticket,
}

TOOL_SCHEMAS = [
    GET_CUSTOMER_SCHEMA,
    GET_ORDER_HISTORY_SCHEMA,
    OPEN_TICKET_SCHEMA,
]