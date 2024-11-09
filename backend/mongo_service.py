# mongo_service.py
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Any

load_dotenv()

mongodb_url = os.getenv('MONGODB_URL')
client = MongoClient(mongodb_url)
db = client['wanderer'] 

def store_user_preferences(user_id, dietary_restrictions, activity_level, interests):
    try:
        user_collection = db['user preference'] 
        user_data = {
            'user_id': user_id,
            'dietary_restrictions': dietary_restrictions,
            'activity_level': activity_level,
            'interests': interests,
            'interaction_history': []  
        }
        user_collection.update_one(
            {'user_id': user_id}, 
            {'$set': user_data}, 
            upsert=True
        )
    except Exception as e:
        return f"Error storing user preferences: {str(e)}"


def get_chat_history(user_id):
    chat_collection = db['chat_history']
    chat_history = list(chat_collection.find({'user_id': user_id}))
    return chat_history if chat_history else None


def serialize_mongo_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    serialized_data = []
    for item in data:
        item["_id"] = str(item["_id"])  # Convert ObjectId to str
        if isinstance(item.get("timestamp"), datetime):
            item["timestamp"] = item["timestamp"].isoformat()  # Convert datetime to ISO format
        serialized_data.append(item)
    return serialized_data


def store_chat_history(user_id, user_message, ai_response):
    """Store chat history in MongoDB."""
    chat_collection = db['chat_history']  
    chat_record = {
        'user_id': user_id,
        'user_message': user_message,
        'ai_response': ai_response,
        'timestamp': datetime.utcnow()
    }
    chat_collection.insert_one(chat_record)
    print(f"Chat history for {user_id} saved successfully.")



def get_user_preferences(user_id):
    try:
        user_collection = db['user preference']
        user = user_collection.find_one({'user_id': user_id})
        if user:
            return user
        else:
            return None
    except Exception as e:
        return f"Error getting user preferences: {str(e)}"



def update_user_preferences(user_id, updates):
    try:
        user_collection = db['user preference']
        user_collection.update_one({'user_id': user_id}, {'$set': updates})
    except Exception as e:
        return f"Error updating user preferences: {str(e)}"



def log_user_interaction(user_id, activity):
    try:
        user_collection = db['user preference']
        user_collection.update_one(
            {'user_id': user_id},
            {'$push': {'interaction_history': activity}} 
        )
        user_collection.update_one(
            {'user_id': user_id},
            {'$set': {'interests': {'$addToSet': activity}}} 
        )
    except Exception as e:
        return f"Error logging interaction for {user_id}: {str(e)}"



def delete_user_preferences(user_id):
    try:
        user_collection = db['user preference']
        user_collection.delete_one({'user_id': user_id})
    except Exception as e:
        return f"Error deleting user preferences: {str(e)}"
