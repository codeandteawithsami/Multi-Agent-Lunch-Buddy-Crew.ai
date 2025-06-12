import os 
import json 
from typing import List, Dict 
from dotenv import load_dotenv
from tavily import TavilyClient
from tools import serper_search_tool
from utils import parse_json_response
from crewai import Agent, Task, Crew, Process

# Load Configuration
load_dotenv()

# Keys
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI_KEY:",OPENAI_KEY)
TAVILY_API = os.getenv("TAVILY_API_KEY")

class Lunch_Buddy:
    def __init__(self):
        self.tavily_client = TavilyClient(api_key = TAVILY_API)
        self.setup_agents()
        
    def setup_agents(self):
        self.Mood_Analyzer_Agent = Agent (
            role = "Mood Analyzer Agent",
            goal = "Understand the user's current mood and cravings.",
            backstory = """You are a Mood Analyzer Agent. Your goal is to analyze the user's text input and identify their current emotional and mental state. 

                            Analyze the user's input and categorize their mood into one or more of the following predefined moods:
                            [
                            "happy",
                            "sad",
                            "excited",
                            "tired",
                            "anxious",
                            "angry",
                            "calm",
                            "bored",
                            "stressed",
                            "nostalgic",
                            "romantic",
                            "celebratory",
                            "craving_sweets",
                            "craving_spicy",
                            "craving_comfort_food"
                            ]""",
            allow_delegation = False,
            # verbose = True
        )
        
        self.Diet_Filter_Agent = Agent (
            role = "Diet Filter Agent",
            goal='Filter suggestions based on dietary restrictions.',
            backstory='You are a nutrition expert focused on dietary needs.',
            memory = True,
            allow_delegation = True,
            # verbose = True
        )
        self.Local_Scout_Agent = Agent(
        role="Local Scout Agent",
        goal="Discover top nearby restaurants based on the user's dish preferences and location.",
        backstory=(
            "You are a well-informed foodie scout who uses tool that's Serper"
            "to find the most suitable, top-rated restaurants for any dish, anywhere in the asked location. "
            "You evaluate results by checking ratings, relevance to preferences, and locality."
        ),
        tools=[serper_search_tool], 
        allow_delegation=True,
        # verbose=True
        )
    
    def analyze_mood(self, topic : str) -> Dict:
        task = Task(
            description = f"Access the user's Mood for: {topic} return the results in JSON format",
            agent=self.Mood_Analyzer_Agent,
            expected_output="""A JSON string in the format
            {
                "Mood": ["<mood1>", "<mood2>", ...],
                "Confidence": "<low/medium/high>",
                "Notes": "<brief explanation of the interpretation>"
            }
            Be concise, and do not include any text outside the JSON.
            """
        )
        crew = Crew(
            agents = [self.Mood_Analyzer_Agent],
            tasks = [task],
            process = Process.sequential
        )
        
        results = crew.kickoff()
        return parse_json_response(str(results))
    
    def filter_diet_options(self, preferences: List[str], options: List[str]) -> Dict:
        task_description = f"""
        You are given a user's dietary preferences and a list of food options.
        
        Your job is to:
        - Remove any food item that violates the preferences.
        - Explain why items are excluded.
        
        Dietary Preferences: {preferences}
        Food Options: {options}

        Return the output as a JSON object like this:
        {{
        "filtered_options": [...],
        "excluded_items": [...],
        "reasoning": "..."
        }}
        """

        task = Task(
            description=task_description,
            agent=self.Diet_Filter_Agent,
            expected_output="A JSON object with 'filtered_options', 'excluded_items', and 'reasoning'."
        )

        crew = Crew(
            agents=[self.Diet_Filter_Agent],
            tasks=[task],
            process=Process.sequential
        )

        result = crew.kickoff()
        return parse_json_response(str(result))
    
    def get_nearby_restaurants(self, location: str, dishes: List[str]) -> Dict:
        # Create a search query from location and dishes
        dishes_str = ", ".join(dishes)
        
        task_description = f"""
        You are given the user's location: **{location}**
        and a list of desired dishes: **{dishes_str}**.

        Your job:
        1. Use the serper_search_tool to search for the best local restaurants that serve these dishes near {location}.
        2. For each dish in {dishes}, perform a search using the tool and compile the results.
        3. Include for each result:
            - Restaurant name
            - Website or review link
            - Recommended dishes
            - A short explanation of why this restaurant is a good choice
        4. Return your answer in the following JSON format:
        ```json
        [
        {{
            "name": "Green Garden",
            "link": "https://greengarden.pk",
            "recommended_dishes": ["paneer tikka"],
            "reason": "Popular vegetarian spot with great paneer reviews."
        }},
        ...
        ]
        ```
        """
        
        task = Task(
        description=task_description,
        agent=self.Local_Scout_Agent,
        expected_output="A JSON list of restaurants with details and reasoning."
        )
        
        crew = Crew(
        agents=[self.Local_Scout_Agent],
        tasks=[task],
        process=Process.sequential
        )
        
        result = crew.kickoff()
        return parse_json_response(str(result))
        
if __name__ == "__main__":
    buddy = Lunch_Buddy()
    results = buddy.analyze_mood(topic="I am feeling very happy I got my laptop today and I want to eat some good luxurious food")
    print(results)
    
    preferences = ["vegetarian", "gluten-free"]
    options = [
        "Grilled chicken sandwich",
        "Vegan tofu curry",
        "Gluten-free pasta with pesto",
        "Beef burger with cheese"
    ]
    results = buddy.filter_diet_options(preferences, options)
    print(results)
    
    
    results = buddy.get_nearby_restaurants(location="wahcantt", dishes=["butter chicken", "biryani"])
    print(results)