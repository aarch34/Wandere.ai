from groq import Groq

def generate_local_guide(location, groq_api_key):
    try:
        client = Groq(
            api_key=groq_api_key,
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a knowledgeable local guide for {location}. \n Provide a comprehensive guide that includes the historical context, cultural significance, key attractions, useful phrases in the local language, recommended restaurants, and transportation tips for travelers."
                },
                {
                    "role": "user",
                    "content": f"Please generate a detailed local guide for {location}."
                }
            ],
            model="llama3-groq-8b-8192-tool-use-preview",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    


if __name__ == "__main__":
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    location = "Red Fort, Delhi."
    guide_info = generate_local_guide(location, os.environ.get("GROQ_API_KEY"))
    print(guide_info)
