import os
from groq import Groq
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import yagmail
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.getenv("api_key"))
conversation_history = []


load_dotenv()
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )


itinerary_prompt =  """Create a detailed multi-day travel itinerary based on the following details:
- User activity preferences: {user_activities}
- Number of days: {travel_days}
- Traveling with: {companions}
- Time of the year: {season}
- Location preference: {location}

For each day of the itinerary, provide the following details for each activity:
1. *Date*: Specify the date of the activity.
2. *Time*: Specify the time of day for the activity.
3. *Description of the Activity*: Provide a brief description.
4. *Type of Activity*: Indicate if it's cultural, adventure, relaxation, etc.
5. *Time Limit*: Specify how long the activity will take (e.g., 2 hours).
6. *Location*: Specify where the activity will take place.

Ensure the itinerary covers all {travel_days} days, with suggestions for morning, afternoon, and evening activities."""

conversation_history.append({"role": "system", "content": itinerary_prompt})
conversation_history.append({"role":"user", "content": "5-day travel itinerary for your family to Gandhinagar, Gujarat"})

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": """Create a detailed multi-day travel itinerary based on the following details:
# - User activity preferences: {user_activities}
# - Number of days: {travel_days}
# - Traveling with: {companions}
# - Time of the year: {season}
# - Location preference: {location}

# For each day of the itinerary, provide the following details for each activity:
# 1. *Date*: Specify the date of the activity.
# 2. *Time*: Specify the time of day for the activity.
# 3. *Description of the Activity*: Provide a brief description.
# 4. *Type of Activity*: Indicate if it's cultural, adventure, relaxation, etc.
# 5. *Time Limit*: Specify how long the activity will take (e.g., 2 hours).
# 6. *Location*: Specify where the activity will take place.

# Ensure the itinerary covers all {travel_days} days, with suggestions for morning, afternoon, and evening activities."""
#         },
#         {
#             "role": "user",
#             "content": '''
# 5-day travel itinerary for your family to Gujarat
# ''',
#         }
#     ],
#     model="meta-llama/Meta-Llama-3-8B-Instruct",
# )

# itinerary_text = chat_completion.choices[0].message.content

itinerary_output = ""
for message in client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=conversation_history,
        max_tokens=2048,
        stream=True,
    ):
    itinerary_output += message.choices[0].delta.content
        # Keep track of response for conversation continuity
    conversation_history.append({"role": "assistant", "content": itinerary_output})
print(itinerary_output)

# Function to generate a PDF itinerary
def generate_itinerary_pdf(itinerary_text, location):
    pdf_filename = f"itinerary_{location}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 50, "Travel Itinerary")

    # Add a horizontal line below the title
    c.line(40, height - 55, width - 40, height - 55)

    # Set starting position for text
    y_position = height - 80

    # Split the itinerary into lines for better formatting
    for line in itinerary_text.splitlines():
        # Check for day headers and format them
        if line.startswith("Day"):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y_position, line)
            y_position -= 20  # Move down for the next line
            c.setFont("Helvetica", 12)  # Reset font for normal text
        else:
            c.setFont("Helvetica", 12)
            # Add activity description
            text = c.beginText(40, y_position)
            text.setLeading(14)
            text.textLines(line)

            c.drawText(text)
            y_position -= 40  # Space between activities

        # positiing of page
        if y_position < 40:  # Reserve space for footer
            c.showPage()  # Create a new page
            y_position = height - 50  # Reset position for the new page

    # Save the PDF
    c.showPage()
    c.save()

    print(f"Itinerary PDF saved as {pdf_filename}")
    return pdf_filename


# Function to send PDF via email
def send_email(email, pdf_filename, title):
    yag = yagmail.SMTP(user=os.getenv("GMAIL_USER"), password=os.getenv("GMAIL_PASSWORD"))
    subject = f"Your {title} is Ready to Explore!"

    body = f"""
    Dear Traveler,

    We are thrilled to present to you your personalized {title.lower()} for your upcoming adventures! 🌍✈️

    Whether you are wandering through the vibrant streets of a bustling city or exploring the serene landscapes of nature, this guide/itinerary is crafted to enhance your experience. Inside, you will find a wealth of information designed to inspire and assist you on your journey.

    Here's what awaits you:
    - **Cultural Insights:** Immerse yourself in the local culture and understand the significance of the places you will visit.
    - **Exciting Activities:** Discover a variety of activities that cater to your interests, whether you seek adventure, relaxation, or exploration.
    - **Local Tips:** Get insider knowledge about the best spots to eat, drink, and unwind, along with handy phrases that will help you connect with the locals.
    - **Comprehensive Itinerary:** Enjoy a well-structured plan that ensures you make the most of your time, from morning till evening.

    As you embark on this journey, remember that the world is full of beautiful experiences waiting to be discovered. Take the time to savor each moment, meet new people, and create unforgettable memories.

    We hope you find this guide/itinerary helpful, and we are excited for the adventures that lie ahead! Should you have any questions or need further assistance, please don't hesitate to reach out.

    Safe travels and happy exploring! 🌟

    Best Regards,
    Your Travel Companion Team
    """

    # yag.send(to=email, subject=subject, contents=body, attachments=pdf_filename)
    print("Email sent successfully.")


location = "Gandhinagar, Gujarat"  # Specify the location for the itinerary
pdf_filename = generate_itinerary_pdf(itinerary_output, location)
email = "hariharpooja2007@gmail.com"  # Replace with the user's email address
send_email(email, pdf_filename, "Itinerary for your Trip to the Gujarat")

