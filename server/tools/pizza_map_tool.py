from config.base_widget import BaseWidget
from pydantic import BaseModel, Field
from typing import Dict, Any
from ..api.pizzeria_api import get_pizzerias


class PizzaMapInput(BaseModel):
    pizza_topping: str = Field(..., alias="pizzaTopping")
    
    class Config:
        populate_by_name = True


class PizzaMapTool(BaseWidget):
    identifier = "pizza-map"
    title = "Show Pizza Map"
    input_schema = PizzaMapInput
    invoking = "Hand-tossing a map..."
    invoked = "Served a fresh map!"
    
    widget_csp = {
        "connect_domains": ["https://api.mapbox.com"],
        "resource_domains": ["https://persistent.oaistatic.com"]
    }
    widget_prefers_border = True
    
    async def execute(self, input_data: PizzaMapInput) -> Dict[str, Any]:
        pizzerias = await get_pizzerias(input_data.pizza_topping)
        return {
            "pizzaTopping": input_data.pizza_topping,
            "places": pizzerias
        }

