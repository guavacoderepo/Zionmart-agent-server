from typing import List
from .departments_tools import get_department
from .orders_tools import create_order, edit_order_item, delete_order, delete_order_item, add_order_item, update_order, get_order_items_by_order_id, get_orders_by_user_id
from .products_tools import retrieve_product_by_name
from .tickets_tools import create_ticket, edit_ticket, delete_ticket
from .users_tools import retrieve_user_by_id, retrieve_user_name

# Combine all tools in a single list
tools: List = [
    # Department tools
    get_department,

    # Order tools
    create_order,
    edit_order_item,
    delete_order,
    delete_order_item,
    add_order_item,
    update_order,
    get_orders_by_user_id,
    get_order_items_by_order_id,


    # Product tools
    retrieve_product_by_name,

    # Ticket tools
    create_ticket,
    edit_ticket,
    delete_ticket,

    # Users tools
    retrieve_user_by_id,
    retrieve_user_name,
]
