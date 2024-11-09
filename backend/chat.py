import json
from groq import Groq
from mongo_service import (
    store_user_preferences,
    get_user_preferences,
    log_user_interaction,
)

def get_user_context(user_id,r):
    
    try:
        user_data = r.get(user_id)
        if user_data:
            return json.loads(user_data)
        else:
            preferences = get_user_preferences(user_id)
            return {"conversation_history": [], "preferences": preferences or {}}
    except Exception as e:
        return {"conversation_history": [], "preferences": {}}

def update_user_context(user_id, updated_context, r):
    try:
        r.set(user_id, json.dumps(updated_context))
        if 'preferences' in updated_context:
            store_user_preferences(
                user_id,
                updated_context['preferences'].get('dietary_restrictions', ''),
                updated_context['preferences'].get('activity_level', ''),
                updated_context['preferences'].get('interests', [])
            )
    except Exception as e:
        print(f"Error updating user context: {str(e)}")

def call_ai_model(personalized_prompt, groq_api_key):
    try:
        client = Groq(
            api_key=groq_api_key
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a personalized AI travel assistant. You provide detailed travel recommendations based on the user's input and preferences. Respond thoughtfully."
                },
                {
                    "role": "user",
                    "content": personalized_prompt, 
                }
            ],
            model="llama3-groq-8b-8192-tool-use-preview",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error calling AI model: {str(e)}"

def generate_personalized_prompt(message, context):
    try:
        history = "\n".join([f"User: {msg['user']}" if "user" in msg else f"AI: {msg['model']}" 
                            for msg in context['conversation_history']])

        preferences = context.get('preferences', {})
        personalized_prompt = (
            f"Conversation history:\n{history}\n\n"
            f"User's message: {message}\n\n"
            f"User preferences: {preferences}\n"
            f"Create a detailed multi-day travel itinerary based on the following details:\n"
            f"- User activity preferences: {preferences.get('interests', 'N/A')}\n"
            f"- Number of days: (add logic to calculate days)\n"
            f"- Time of the year: (add logic to calculate season)\n"
            f"- Location preference: (extract location from message)\n"
        )
        
        return personalized_prompt
    except Exception as e:
        return f"Error generating personalized prompt: {str(e)}"

def get_chat_response(user_id, user_message, groq_api_key, r):
    try: 
        user_context = get_user_context(user_id, r)
        log_user_interaction(user_id, user_message)
        user_context['conversation_history'].append({"user": user_message})
        personalized_prompt = generate_personalized_prompt(user_message, user_context)

        ai_response = call_ai_model(personalized_prompt, groq_api_key)
        user_context['conversation_history'].append({"model": ai_response})

        update_user_context(user_id, user_context, r)
        return {"response": ai_response}
    except Exception as e:
        return f"Error getting chat response: {str(e)}"