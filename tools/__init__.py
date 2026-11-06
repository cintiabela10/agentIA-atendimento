from .customers import get_customer, update_account_status, GET_CUSTOMER_SCHEMA, UPDATE_ACCOUNT_STATUS_SCHEMA
from .orders import get_order_history, check_refund_eligibility, GET_ORDER_HISTORY_SCHEMA, CHECK_REFUND_ELIGIBILITY_SCHEMA
from .support import open_support_ticket, list_open_tickets, OPEN_TICKET_SCHEMA, LIST_OPEN_TICKETS_SCHEMA

TOOLS = {
    "get_customer": get_customer,
    "update_account_status": update_account_status,
    "get_order_history": get_order_history,
    "check_refund_eligibility": check_refund_eligibility,
    "open_support_ticket": open_support_ticket,
    "list_open_tickets": list_open_tickets,
}

TOOL_SCHEMAS = [
    GET_CUSTOMER_SCHEMA,
    UPDATE_ACCOUNT_STATUS_SCHEMA,
    GET_ORDER_HISTORY_SCHEMA,
    CHECK_REFUND_ELIGIBILITY_SCHEMA,
    OPEN_TICKET_SCHEMA,
    LIST_OPEN_TICKETS_SCHEMA,
]