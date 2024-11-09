from groq import Groq
from geopy.geocoders import Nominatim
import openrouteservice as ors
from datetime import datetime

def get_coordinates(location_name, ors_client):
    geolocator = Nominatim(user_agent="navigation_guide")
    try:
        location_add = geolocator.geocode(location_name)
        client = ors.Client(key=ors_client)
        location = client.pelias_search(text=location_name)
        if location['features']:
            coordinates = location['features'][0]['geometry']['coordinates']
            latitude = coordinates[0]
            longitude = coordinates[1]
        else:
            return f"Location Not Found: {location_name}"
        
        return {
            'name': location_add.address,
            'latitude': latitude,
            'longitude': longitude
        }
    except Exception as e:
        return f"Error getting coordinates: {str(e)}"

def get_route_directions(start_coords, end_coords, ors_client):
    coords = [[start_coords['lon'], start_coords['lat']], 
                 [end_coords['longitude'], end_coords['latitude']]]
        
    route = ors_client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson',
            instructions='true',
            language='en'
        )
        
    print(route)
    try:
        coords = [[start_coords['lon'], start_coords['lat']], 
                 [end_coords['longitude'], end_coords['latitude']]]
        
        route = ors_client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson',
            instructions='true',
            language='en'
        )
        
        if route and 'features' in route and len(route['features']) > 0:
            steps = route['features'][0]['properties']['segments'][0]['steps']
            distance = route['features'][0]['properties']['segments'][0]['distance']
            duration = route['features'][0]['properties']['segments'][0]['duration']
            return {
                'steps': steps,
                'total_distance': distance,
                'total_duration': duration
            }
        return None
    except Exception as e:
        return f"Error getting route: {str(e)}"

def enhance_instruction_with_ai(instruction, groq_client):
    prompt = f"""Convert this navigation instruction into a natural, detailed driving direction:
    Original: "{instruction}"
    Make it conversational and clear, including landmarks or cardinal directions when present.
    Keep it concise but informative. Focus on essential details for navigation."""
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-groq-8b-8192-tool-use-preview",
            messages=[
                {"role": "system", "content": "You are a helpful navigation assistant. Provide clear, concise driving directions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error enhancing instruction: {str(e)}"

def format_duration(seconds):
    try: 
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if hours > 0:
            return f"{int(hours)} hour{'s' if hours != 1 else ''} {int(minutes)} minute{'s' if minutes != 1 else ''}"
        else:
            return f"{int(minutes)} minute{'s' if minutes != 1 else ''}"
    except:
        return "Error: While Converting Duration Error"

def format_distance(meters):
    try:
        meters = float(meters)
        if meters >= 1000:
            return f"{meters/1000:.1f} km"
        else:
            return f"{int(meters)} meters"
    except:
        return "Error: While Converting Distance Error"

def generate_navigation_guide(start_coords, destination, groq_api_key=None, ors_api_key=None):
    if not groq_api_key or not ors_api_key:
        return "Error: API keys not found in environment variables"
    
    groq_client = Groq(api_key=groq_api_key)
    ors_client = ors.Client(key=ors_api_key)

    lat, lon = start_coords['latitude'], start_coords['longitude']
    start_coords = {'name': 'Current Location', 'lat': lat, 'lon': lon}
    end_coords = get_coordinates(destination, ors_api_key)
    
    if not start_coords or not end_coords:
        return "Error: Could not find one or both locations"
    if start_coords == end_coords:
        return "Error: Start and end locations are the same"
    
    try:
        route_info = get_route_directions(start_coords, end_coords, ors_client)
    except Exception as e:
        return f"Error: {str(e)}"
        
    guide = f"""
        🚗 NAVIGATION GUIDE
        From: {start_coords['name']}
        To: {end_coords['name']}
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

        📊 TRIP OVERVIEW
        Total Distance: {format_distance(route_info['total_distance'])} 
        Estimated Duration: {format_duration(route_info['total_duration'])}

        🗺️ TURN-BY-TURN DIRECTIONS
    """
    for i, step in enumerate(route_info['steps'], 1):
        original_instruction = step['instruction']
        enhanced_instruction = enhance_instruction_with_ai(original_instruction, groq_client)
        distance = format_distance(step['distance'])
        
        guide += f"""
            {i}. {enhanced_instruction}
            Distance: {distance}
        """
    

    guide += f"""
        🔗 VIEW ON GOOGLE MAPS
        https://www.google.com/maps/dir/?api=1&origin={start_coords['lat']},{start_coords['lon']}&destination={end_coords['lat']},{end_coords['lon']}&travelmode=driving
    """
    
    return guide, route_info

if __name__ == "__main__":
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    print("🚗 Welcome to AI Navigation Guide!")
    destination = input("Enter destination: ")
    print("\nGenerating your personalized navigation guide...")
    start_coords = get_coordinates("IIT Delhi, Delhi", os.environ.get("ORS_API_KEY"))
    guide = generate_navigation_guide(start_coords, destination, os.environ.get("GROQ_API_KEY"), os.environ.get("ORS_API_KEY"))
    print("\n" + guide)