# app.py

from mongo_service import (
    store_user_preferences,
    get_user_preferences,
    update_user_preferences,
    delete_user_preferences,
    log_user_interaction
)

def main():
    user_id = 'user_123'  

   
    store_user_preferences(
        user_id=user_id,
        dietary_restrictions='vegetarian',
        activity_level='hiking',
        interests=['history', 'art', 'nature']
    )

   
    log_user_interaction(user_id, 'attended cultural event')
    log_user_interaction(user_id, 'went hiking')

   
    user_preferences = get_user_preferences(user_id)
    if user_preferences:
        print(f"Retrieved Preferences: {user_preferences}")

   
    update_user_preferences(user_id, {'activity_level': 'relaxing'})


if __name__ == '__main__':
    main()
