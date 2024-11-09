from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from setp_router import generate_navigation_guide
from trip_json_gen import generate_travel_itinerary
from local_guide import generate_local_guide
from chat import get_chat_response
from mongo_service import get_user_preferences, get_chat_history, serialize_mongo_data
import redis

load_dotenv()
app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0)

class UserInput(BaseModel):
    user_id: str
    message: str

class LocationInput(BaseModel):
    location: str

class DestinationInput(BaseModel):
    user_id: str
    destination: str
    start_date: str
    end_date: str
    budget_category: str
    number_of_travelers: int

class RouteGuideInput(BaseModel):
    destination: str
    longitude: float
    latitude: float

class GetHistoryInput(BaseModel):
    user_id: str

@app.post("/chat")
async def chat_with_ai(user_input: UserInput):
    if not user_input.user_id:
        raise HTTPException(status_code=400, detail="Error: User ID field is required for chat")
    user_id = user_input.user_id
    if not user_input.message:
        raise HTTPException(status_code=400, detail="Error: Message field is required for chat")
    user_message = user_input.message
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="Error: Groq API key not found in environment variables")
    try:
        chat_response = get_chat_response(user_id, user_message,  os.environ.get("GROQ_API_KEY"), r)
        return chat_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/get_history")
async def get_history(user_input: GetHistoryInput):
    if not user_input.user_id:
        raise HTTPException(status_code=400, detail="User ID is required to get chat history")
    
    chat_history = get_chat_history(user_input.user_id)
    if not chat_history:
        raise HTTPException(status_code=404, detail="No chat history found for this user")
    
    return serialize_mongo_data(chat_history)


@app.post("/local_guide")
async def local_guide(location_input: LocationInput):
    if not location_input.location:
        raise HTTPException(status_code=400, detail="Error: Location field is required for generating local guide")
    location = location_input.location
    try:
        guide_info = generate_local_guide(location)
        return {"response": guide_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/get_itienary")
async def get_itienary(user_input: DestinationInput):
    if not user_input.user_id:
        raise HTTPException(status_code=400, detail="Error: User ID field is required for generating itinerary")
    user_id = user_input.user_id
    if not user_input.destination:
        raise HTTPException(status_code=400, detail="Error: Destination field is required for generating itinerary")
    destination = user_input.destination
    if not user_input.start_date or not user_input.end_date:
        raise HTTPException(status_code=400, detail="Error: Start and end dates are required for generating itinerary")
    start_date = user_input.start_date
    end_date = user_input.end_date
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Error: Start date cannot be after end date")
    if start_date == end_date:
        raise HTTPException(status_code=400, detail="Error: Start and end dates cannot be the same")
    budget_category = user_input.budget_category
    if not budget_category:
        budget_category = "medium"
    number_of_travelers = user_input.number_of_travelers
    if not number_of_travelers:
        number_of_travelers = 1
    if not user_input.user_id:
        raise HTTPException(status_code=400, detail="Error: User ID field is required for generating itinerary")
    interests = get_user_preferences(user_input.user_id)
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="Error: Groq API key not found in environment variables")
    try:
        groq_api_key = os.environ.get("GROQ_API_KEY")
        itinerary = generate_travel_itinerary(user_id, destination, start_date, end_date, interests, budget_category, number_of_travelers, groq_api_key)
        return itinerary
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_route_guide")
async def get_route_guide(user_input: RouteGuideInput):
    if not user_input.destination:
        raise HTTPException(status_code=400, detail="Error: Destination field is required for generating route guide")
    if not user_input.longitude or not user_input.latitude:
        raise HTTPException(status_code=400, detail="Error: Start coordinates are required for generating route guide")
    if not os.environ.get("API_KEY") or not os.environ.get("ORS_API_KEY"):
        raise HTTPException(status_code=500, detail="Error: API keys not found in environment variables")
    try:
        groq_api_key = os.environ.get("API_KEY")
        ors_api_key = os.environ.get("ORS_API_KEY")
        start_coords = user_input.start_coords
        destination = user_input.destination
        route_guide, route_info = generate_navigation_guide(start_coords, destination, groq_api_key, ors_api_key)
        return {"response": route_guide, "route": route_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))