from __future__ import annotations

from db import purchase_history

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "get_purchase_history",
        "description": (
            "Return the purchase history for a customer. Use this when answering "
            "questions about orders, purchases, delivery status, or spending."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The numeric customer ID whose purchases should be retrieved.",
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def get_purchase_history(customer_id: int, *, logged_in_customer_id: int) -> dict:
    if customer_id != logged_in_customer_id:
        return {
            "customer_id": customer_id,
            "purchases": [],
            "access_denied": True,
            "message": (
                "ACCESS DENIED: This tool may only return purchase records for the user currently logged in."
            ),
        }

    return {
        "customer_id": customer_id,
        "purchases": purchase_history(customer_id, logged_in_customer_id=logged_in_customer_id),
    }


def dispatch_tool(name: str, arguments: dict, *, logged_in_customer_id: int) -> dict:
    if name == "get_purchase_history":
        return get_purchase_history(
            customer_id=int(arguments["customer_id"]),
            logged_in_customer_id=logged_in_customer_id,
        )
    raise ValueError(f"Unknown tool: {name}")
