import httpx


async def get_pizzerias(topping: str):
    """피자 가게 API 호출 (Mock Data)"""
    # TODO: Replace with real API call
    # Mock data for demonstration
    mock_pizzerias = {
        "Margherita": [
            {"name": "Pizzeria Napoli", "address": "123 Main St", "rating": 4.5, "lat": 40.7128, "lng": -74.0060},
            {"name": "Italian Corner", "address": "456 Oak Ave", "rating": 4.8, "lat": 40.7580, "lng": -73.9855},
            {"name": "Roma Pizza House", "address": "789 Elm Rd", "rating": 4.3, "lat": 40.7489, "lng": -73.9680},
        ],
        "Pepperoni": [
            {"name": "Pepperoni Paradise", "address": "321 Pine St", "rating": 4.7, "lat": 40.7614, "lng": -73.9776},
            {"name": "Classic Pizza Co", "address": "654 Maple Dr", "rating": 4.4, "lat": 40.7306, "lng": -73.9352},
        ],
        "Hawaiian": [
            {"name": "Tropical Pizza", "address": "987 Beach Blvd", "rating": 4.2, "lat": 40.7282, "lng": -74.0776},
            {"name": "Island Slice", "address": "147 Ocean Ave", "rating": 4.6, "lat": 40.7589, "lng": -73.9851},
        ],
    }
    
    # Return pizzerias for the requested topping, or generic list
    pizzerias = mock_pizzerias.get(topping, [
        {"name": f"{topping} Pizzeria", "address": "100 Demo St", "rating": 4.5, "lat": 40.7128, "lng": -74.0060},
        {"name": f"Best {topping} Pizza", "address": "200 Test Ave", "rating": 4.7, "lat": 40.7580, "lng": -73.9855},
    ])
    
    return pizzerias

