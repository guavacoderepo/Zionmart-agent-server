from src.schema.agent_schemes import AgentState
from src.services.routers_service import route_handler


async def create_order(state: AgentState):
    question = state.get("refine_question", "")
    user_id = state.get("user_id", "")

    task_prompt = f"""
        You are an intelligent agent specialized in handling Zion Mart e-commerce orders.

        User Query: {question}
        User ID: {user_id}

        Instructions - If all items are available, proceed to:
            - Use 'retrieve_product_by_name' to fetch single product.
            - Use 'create_order' to start an order.
            - Use 'add_order_item' for each product. price = (product price * quantity).
            - Update order quantity and total price using 'update_order' as needed.
            - After successfully creating the order, instruct the user to proceed to payment.
        Return a short summary of the order, including items, quantities, prices, and the payment instruction.
        """
    # Call the generic route handler
    return await route_handler(state, task_prompt)

# --- Node: Edit Order ---
async def edit_order(state: AgentState):
    question = state.get("refine_question", "")
    user_id = state.get("user_id", "")

    task_prompt = f"""
    You are an intelligent agent for Zion Mart e-commerce order management.

    User Query: {question}
    User ID: {user_id}

    Objectives:
    1. Fetch existing orders with 'get_orders_by_user_id'.
    2. Retrieve order items using 'get_order_items_by_order_id'.
    3. Update or delete items using 'edit_order_item' or 'delete_order'.
    4. Update the order status and total price using 'update_order'.
    5. Return a summary of the updated order.
    """
    return await route_handler(state, task_prompt) 

# --- Node: Cancel Order ---
async def cancel_order(state: AgentState):
    question = state.get("refine_question", "")
    user_id = state.get("user_id", "")

    task_prompt = f"""
    You are an intelligent agent specialized in handling Zion Mart e-commerce orders.

    User Query: {question}
    User ID: {user_id}

    Your objectives:
        - Use 'retrieve_order' to locate the order to cancel.
        - Use 'update_order' tool to update status to cancel.
        - Return a confirmation message to the user.
    """
    return await route_handler(state, task_prompt)

# --- Node: Retrieve Items ---
async def retrieve_items(state: AgentState):
    question = state.get("refine_question", "")
    user_id = state.get("user_id", "")

    task_prompt = f"""
    You are an intelligent agent specialized in handling Zion Mart e-commerce queries.

    User Query: {question}
    User ID: {user_id}

    Your objectives:
    - Use 'retrieve_product_by_name' to fetch requested product(s) information.
    - Provide prices, descriptions, and availability.
    - Return a clear summary of the items to the user.
    """
    return await route_handler(state, task_prompt)
    