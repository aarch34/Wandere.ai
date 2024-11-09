import json
from groq import Groq
from typing import Dict, List
import datetime
import re
from huggingface_hub import InferenceClient
from iternary import json_to_pdf, upload_temp_file_to_idrive

def clean_and_parse_json(json_string: str) -> dict:
    json_string = re.sub(r'```json\s*', '', json_string)
    json_string = re.sub(r'```\s*$', '', json_string)
    json_string = re.sub(r'^[^{]*', '', json_string)
    json_string = re.sub(r'[^}]*$', '', json_string)
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise f"Failed to parse JSON: {str(e)}"

def generate_travel_itinerary(
    user_id: str,
    destination: str,
    start_date: str,
    end_date: str,
    interests: List[str],
    budget_category: str = "medium",
    num_travelers: int = 1,
    api_key: str = None
) -> Dict:
    if not api_key:
        raise "Error: API key is required"

    client = InferenceClient(api_key=api_key)

    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    num_days = (end - start).days + 1
    prompt = f"""Generate a detailed travel itinerary for {destination} in JSON format. 
        Trip details:
        - Destination: {destination}
        - Start date: {start_date}
        - End date: {end_date}
        - Duration: {num_days} days
        - Number of travelers: {num_travelers}
        - Interests: {', '.join(interests)}
        - Budget level: {budget_category}

        Please provide a detailed JSON response with the following structure:
        {{
            "trip_summary": {{
                "destination": string,
                "country": string,
                "start_date": string,
                "end_date": string,
                "duration": number,
                "travelers": number,
                "budget_category": string,
                "total_estimated_cost": number
            }},
            "essential_info": {{
                "timezone": string,
                "currency": string,
                "language": string,
                "visa_requirements": string,
                "best_season": string,
                "local_customs": [string],
                "emergency_contacts": {{
                    "police": string,
                    "ambulance": string,
                    "tourist_police": string
                }}
            }},
            "daily_schedule": [
                {{
                    "day_number": number,
                    "date": string,
                    "weather_forecast": string,
                    "activities": [
                        {{
                            "time": string,
                            "activity": string,
                            "location": {{
                                "name": string,
                                "address": string,
                                "coordinates": {{
                                    "lat": number,
                                    "lng": number
                                }}
                            }},
                            "duration": string,
                            "cost": number,
                            "booking_required": boolean,
                            "booking_link": string,
                            "notes": string
                        }}
                    ],
                    "meals": [
                        {{
                            "type": string,
                            "time": string,
                            "suggestion": string,
                            "cuisine": string,
                            "estimated_cost": number,
                            "notes": string
                        }}
                    ],
                    "transport": {{
                        "morning": string,
                        "evening": string,
                        "estimated_cost": number,
                        "notes": string
                    }}
                }}
            ],
            "budget_breakdown": {{
                "accommodation": {{
                    "total": number,
                    "per_day": number,
                    "category": string,
                    "suggestions": [string]
                }},
                "food": {{
                    "total": number,
                    "per_day": number,
                    "notes": string
                }},
                "transport": {{
                    "total": number,
                    "per_day": number,
                    "notes": string
                }},
                "activities": {{
                    "total": number,
                    "notes": string
                }},
                "miscellaneous": {{
                    "total": number,
                    "notes": string
                }}
            }},
            "packing_list": {{
                "essentials": [string],
                "clothing": [string],
                "electronics": [string],
                "documents": [string],
                "destination_specific": [string]
            }},
            "travel_tips": [
                {{
                    "category": string,
                    "tips": [string]
                }}
            ],
            "local_phrases": [
                {{
                    "phrase": string,
                    "pronunciation": string,
                    "meaning": string
                }}
            ]
        }}

        Provide realistic costs, actual locations, and practical recommendations. Include specific details about local attractions, restaurants, and transport options.
        WARNING: Do not add any comment or markdown in json just a simple json response. Dont add // or # or any other comment in json.Also dont write extra lines other then details
        DONT WRITE ANYTHING ELSE OTHER THEN JSON NO COMMENTS OR ANYTHING ELSE. DONT ADD THE REMAINING DAYS ETC IN THE SAME FORMAT
        CONSIDER the number of days mentoined i need details for all the days starting from the start date to the end date
        Always put time as string like this "1:00 PM"
        make it perferctly formatted json never miss any "" or , or : or []
    """
    itinerary_output = ""
    for message in client.chat_completion(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages= [
                {
                    "role": "system",
                    "content": "You are a knowledgeable travel planner. Provide detailed, accurate travel itineraries with practical recommendations and realistic cost estimates."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
                temperature=0.6,
                max_tokens=4096,
                stream=True,
            ):
        itinerary_output += message.choices[0].delta.content
    itinerary = clean_and_parse_json(itinerary_output)
    required_fields = ["trip_summary", "essential_info", "daily_schedule", "budget_breakdown"]
    missing_fields = [field for field in required_fields if field not in itinerary]
    if missing_fields:
        print( f"Missing required fields in response: {missing_fields}")

    output_filename = json_to_pdf(itinerary, f"{user_id}_itinerary.pdf")
    url = upload_temp_file_to_idrive(output_filename, os.getenv("S3_BUCKET_NAME"), output_filename, os.getenv("ACCESS_KEY_S3_ID"), os.getenv("SECRET_ACCESS_KEY_S3"), os.getenv("S3_ENDPOINT_URL"))
    return url
    # try:
    #     itinerary_output = ""
    #     for message in client.chat_completion(
    #             model="meta-llama/Meta-Llama-3-8B-Instruct",
    #             messages= [
    #             {
    #                 "role": "system",
    #                 "content": "You are a knowledgeable travel planner. Provide detailed, accurate travel itineraries with practical recommendations and realistic cost estimates."
    #             },
    #             {
    #                 "role": "user",
    #                 "content": prompt
    #             }
    #         ],
    #             temperature=0.6,
    #             max_tokens=4096,
    #             stream=True,
    #         ):
    #         itinerary_output += message.choices[0].delta.content
    #     itinerary = clean_and_parse_json(itinerary_output)
    #     required_fields = ["trip_summary", "essential_info", "daily_schedule", "budget_breakdown"]
    #     missing_fields = [field for field in required_fields if field not in itinerary]
    #     if missing_fields:
    #         raise f"Missing required fields in response: {missing_fields}"

    #     output_filename = json_to_pdf(itinerary, f"{user_id}_itinerary.pdf")
    #     url = upload_temp_file_to_idrive(output_filename, os.getenv("S3_BUCKET_NAME"), output_filename, os.getenv("ACCESS_KEY_S3_ID"), os.getenv("SECRET_ACCESS_KEY_S3"), os.getenv("S3_ENDPOINT_URL"))
    #     return url

    # except Exception as e:
    #     raise f"Failed to generate itinerary: {str(e)}"

def save_itinerary(itinerary: Dict, filename: str):
    """Save the itinerary to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(itinerary, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    itinerary = generate_travel_itinerary(
        user_id="user123",
            destination="Japan",
            start_date="2024-06-15",
            end_date="2024-06-20",
            interests=["history", "food", "culture"],
            budget_category="medium",
            num_travelers=2,
            api_key=os.environ.get("API_KEY")
        )
    save_itinerary(itinerary, "japan_itinerary.json") 
    print("\nFirst Day Schedule:")
    print(json.dumps(itinerary["daily_schedule"][0], indent=2))
    print(f"\nTotal Estimated Cost: {itinerary['trip_summary']['total_estimated_cost']}")
