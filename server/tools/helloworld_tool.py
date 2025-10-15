from config.base_widget import BaseWidget
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any


class HelloWorldInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    # No required inputs - just a simple hello world


class HelloWorldTool(BaseWidget):
    identifier = "helloworld"
    title = "Hello World"
    input_schema = HelloWorldInput
    invoking = "Preparing hello world..."
    invoked = "Hello world ready!"
    
    widget_csp = {
        "connect_domains": [],
        "resource_domains": []
    }
    
    async def execute(self, input_data: HelloWorldInput) -> Dict[str, Any]:
        return {
            "message": "Hello World!",
            "timestamp": "2025-10-15"
        }

