from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, Query
from Lunch_Buddy import Lunch_Buddy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Lunch Buddy Crew API",
    description="Multi-agent system that suggests personalized lunch ideas based on mood, diet, and location.",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

buddy = Lunch_Buddy()

class MoodRequest(BaseModel):
    mood_text: str
    
class DietFilterRequest(BaseModel):
    preferences: List[str]
    options: List[str]
    
class RestaurantSearchRequest(BaseModel):
    query: Optional[str] = None
    country_code: str = "us"
    city: Optional[str] = ""
    location: Optional[str] = None
    dishes: Optional[List[str]] = None
    
# Routes
@app.post("/analyze-mood")
def analyze_mood(req: MoodRequest):
    result = buddy.analyze_mood(topic=req.mood_text)
    return result

@app.post("/filter-diet")
def filter_diet(req: DietFilterRequest):
    result = buddy.filter_diet_options(preferences=req.preferences, options=req.options)
    return result

@app.post("/find-restaurants")
def find_restaurants(req: RestaurantSearchRequest):
    # Handle both parameter styles
    if req.location and req.dishes:
        # Use the new parameter style directly
        result = buddy.get_nearby_restaurants(location=req.location, dishes=req.dishes)
    else:
        # Use the old parameter style, mapping to the function's expected parameters
        location = req.city if req.city else f"{req.country_code} region"
        dishes = [req.query] if req.query else ["local food"]
        result = buddy.get_nearby_restaurants(location=location, dishes=dishes)
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
    
    