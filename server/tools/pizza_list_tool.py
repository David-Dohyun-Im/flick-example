from config.base_widget import BaseWidget
from pydantic import BaseModel, Field
from typing import Dict, Any
from ..api.pizzeria_api import get_pizzerias


class PizzaListInput(BaseModel):
    pizza_topping: str = Field(..., alias="pizzaTopping")
    
    class Config:
        populate_by_name = True


class PizzaListTool(BaseWidget):
    identifier = "pizza-list"
    title = "Show Pizza List"
    input_schema = PizzaListInput
    invoking = "Preparing pizza list..."
    invoked = "Pizza list ready!"
    
    widget_csp = {
        "connect_domains": [],
        "resource_domains": ["https://persistent.oaistatic.com"]
    }
    
    async def execute(self, input_data: PizzaListInput) -> Dict[str, Any]:
        pizzerias = await get_pizzerias(input_data.pizza_topping)
        return {
            "pizzaTopping": input_data.pizza_topping,
            "places": pizzerias
        }

