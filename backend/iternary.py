import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import yagmail
from jinja2 import Template
import json
import pdfkit
import datetime
import os
import boto3
from botocore.client import Config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition
import base64
import os 
from dotenv import load_dotenv
load_dotenv()

# HTML template with CSS styling
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .section {
            margin-bottom: 25px;
        }
        .day-schedule {
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            background: #f9f9f9;
        }
        .activity {
            margin: 10px 0;
            padding-left: 20px;
        }
        .essential-info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
        }
        .emergency-contacts {
            background: #fff3f3;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #ff6b6b;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f5f5f5;
        }
        .phrases-table {
            width: 100%;
            margin-top: 20px;
        }
        .weather {
            color: #666;
            font-style: italic;
        }
        .budget {
            background: #f9f9f9;
            padding: 15px;
            margin: 10px 0;
        }
        @media print {
            .page-break { page-break-before: always; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Travel Itinerary: {{ trip_summary.destination }}</h1>
        <p>{{ trip_summary.start_date }} to {{ trip_summary.end_date }} ({{ trip_summary.duration }} days)</p>
        <p>Number of Travelers: {{ trip_summary.travelers }}</p>
        <p>Total Estimated Cost: {{ "{:,}".format(trip_summary.total_estimated_cost) }}</p>
    </div>

    <div class="section essential-info">
        <h2>Essential Information</h2>
        <p><strong>Timezone:</strong> {{ essential_info.timezone }}</p>
        <p><strong>Currency:</strong> {{ essential_info.currency }}</p>
        <p><strong>Language:</strong> {{ essential_info.language }}</p>
        <p><strong>Visa Requirements:</strong> {{ essential_info.visa_requirements }}</p>
        <p><strong>Best Season to Visit:</strong> {{ essential_info.best_season }}</p>
        
        <div class="emergency-contacts">
            <h3>Emergency Contacts</h3>
            <p>Police: {{ essential_info.emergency_contacts.police }}</p>
            <p>Ambulance: {{ essential_info.emergency_contacts.ambulance }}</p>
            <p>Tourist Police: {{ essential_info.emergency_contacts.tourist_police }}</p>
        </div>
    </div>

    <div class="page-break"></div>

    <div class="section">
        <h2>Daily Schedule</h2>
        {% for day in daily_schedule %}
        <div class="day-schedule">
            <h3>Day {{ day.day_number }}: {{ day.date }}</h3>
            <p class="weather">Weather: {{ day.weather_forecast }}</p>
            
            <h4>Activities:</h4>
            {% for activity in day.activities %}
            <div class="activity">
                <p><strong>{{ activity.time }}</strong> - {{ activity.activity }}</p>
                <p>Location: {{ activity.location.name }}</p>
                <p>Address: {{ activity.location.address }}</p>
                <p>Duration: {{ activity.duration }}</p>
                <p>Cost: {{ activity.cost }}</p>
                {% if activity.notes %}
                <p>Notes: {{ activity.notes }}</p>
                {% endif %}
            </div>
            {% endfor %}

            <h4>Transport:</h4>
            <p>Morning: {{ day.transport.morning }}</p>
            <p>Evening: {{ day.transport.evening }}</p>
            <p>Cost: {{ day.transport.estimated_cost }}</p>
        </div>
        {% if loop.index % 2 == 0 %}
        <div class="page-break"></div>
        {% endif %}
        {% endfor %}
    </div>

    <div class="section budget">
        <h2>Budget Breakdown</h2>
        <table>
            <tr>
                <th>Category</th>
                <th>Total Cost</th>
                <th>Per Day</th>
            </tr>
            <tr>
                <td>Accommodation</td>
                <td>{{ "{:,}".format(budget_breakdown.accommodation.total) }}</td>
                <td>{{ "{:,}".format(budget_breakdown.accommodation.per_day) }}</td>
            </tr>
            <tr>
                <td>Food</td>
                <td>{{ "{:,}".format(budget_breakdown.food.total) }}</td>
                <td>{{ "{:,}".format(budget_breakdown.food.per_day) }}</td>
            </tr>
            <tr>
                <td>Transport</td>
                <td>{{ "{:,}".format(budget_breakdown.transport.total) }}</td>
                <td>{{ "{:,}".format(budget_breakdown.transport.per_day) }}</td>
            </tr>
            <tr>
                <td>Activities</td>
                <td>{{ "{:,}".format(budget_breakdown.activities.total) }}</td>
                <td>-</td>
            </tr>
            <tr>
                <td>Miscellaneous</td>
                <td>{{ "{:,}".format(budget_breakdown.miscellaneous.total) }}</td>
                <td>-</td>
            </tr>
        </table>
    </div>

    <div class="page-break"></div>

    <div class="section">
        <h2>Packing List</h2>
        <h3>Essentials</h3>
        <ul>
        {% for item in packing_list.essentials %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>

        <h3>Clothing</h3>
        <ul>
        {% for item in packing_list.clothing %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>

        <h3>Electronics</h3>
        <ul>
        {% for item in packing_list.electronics %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    </div>

    <div class="section">
        <h2>Useful Local Phrases</h2>
        <table class="phrases-table">
            <tr>
                <th>Phrase</th>
                <th>Pronunciation</th>
                <th>Meaning</th>
            </tr>
            {% for phrase in local_phrases %}
            <tr>
                <td>{{ phrase.phrase }}</td>
                <td>{{ phrase.pronunciation }}</td>
                <td>{{ phrase.meaning }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

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
    
    yag.send(to=email, subject=subject, contents=body, attachments=pdf_filename)
    print("Email sent successfully.")

def send_email_with_sendgrid(email, pdf_filename, title):
    subject = f"Your {title} is Ready to Explore!"
    
    body_html = """
    <html>
    <body>
        <p>Dear Traveler,</p>

        <p>We are thrilled to present to you your personalized itinerary for your trip to <strong>China</strong> for your upcoming adventures! 🌍✈️</p>

        <p>Whether you are wandering through the vibrant streets of a bustling city or exploring the serene landscapes of nature, this guide/itinerary is crafted to enhance your experience. Inside, you will find a wealth of information designed to inspire and assist you on your journey.</p>

        <p><strong>Here's what awaits you:</strong></p>
        <ul>
            <li><strong>Cultural Insights:</strong> Immerse yourself in the local culture and understand the significance of the places you will visit.</li>
            <li><strong>Exciting Activities:</strong> Discover a variety of activities that cater to your interests, whether you seek adventure, relaxation, or exploration.</li>
            <li><strong>Local Tips:</strong> Get insider knowledge about the best spots to eat, drink, and unwind, along with handy phrases that will help you connect with the locals.</li>
            <li><strong>Comprehensive Itinerary:</strong> Enjoy a well-structured plan that ensures you make the most of your time, from morning till evening.</li>
        </ul>

        <p>As you embark on this journey, remember that the world is full of beautiful experiences waiting to be discovered. Take the time to savor each moment, meet new people, and create unforgettable memories.</p>

        <p>We hope you find this guide/itinerary helpful, and we are excited for the adventures that lie ahead! Should you have any questions or need further assistance, please don't hesitate to reach out.</p>

        <p>Safe travels and happy exploring! 🌟</p>

        <p>Best Regards,<br>Your Travel Companion Team</p>
    </body>
    </html>
    """
    
    # Read PDF encode in  base64
    with open(pdf_filename, "rb") as pdf_file:
        encoded_pdf = base64.b64encode(pdf_file.read()).decode()

    # Create attachment for SendGrid
    attachment = Attachment(
        FileContent(encoded_pdf),
        FileName(pdf_filename),
        FileType("application/pdf"),
        Disposition("attachment")
    )

    to_emails = [email]  
    from_email = os.getenv("SENDER_EMAIL") 

    #SendGrid Mail object
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,  
        subject=subject,
        html_content=body_html  
    )

    # Adding attachment
    message.add_attachment(attachment)

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email sent successfully with status code {response.status_code}")
        print(f"Response Body: {response.body}")
        print(f"Response Headers: {response.headers}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        if hasattr(e, 'body'):
            print(f"Error Body: {e.body}")

def convert_json_to_pdf(json_data, output_filename):
    """
    Convert JSON travel itinerary to PDF
    
    Args:
        json_data (dict): The JSON data containing travel itinerary
        output_filename (str): The name of the output PDF file
    """
    template = Template(html_template)
    html_content = template.render(**json_data)
    
    temp_html = 'temp_itinerary.html'
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdfkit.from_file(temp_html, output_filename, configuration=config)
    
    os.remove(temp_html)



def json_to_pdf(itinerary):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'travel_itinerary_{timestamp}.pdf'
    convert_json_to_pdf(itinerary, output_filename)
    return output_filename


def upload_temp_file_to_idrive(temp_file_path, bucket_name, object_name, 
                             access_key, secret_key, 
                             endpoint_url): 
    try:
        client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        client.upload_file(temp_file_path, bucket_name, object_name)
        url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name}
        )
        return url
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return None


if __name__ == "__main__":
    # file_name = json_to_pdf()
    # url = upload_temp_file_to_idrive(file_name, os.getenv("S3_BUCKET_NAME"), file_name, os.getenv("ACCESS_KEY_S3_ID"), os.getenv("SECRET_ACCESS_KEY_S3"), os.getenv("S3_ENDPOINT_URL"))
    # print(url)
    # send_email(os.getenv("RECIPIENT_EMAIL"), file_name, "Travel Itinerary") 
    # print(file_name)
    send_email_with_sendgrid("tempmail112003@gmail.com", "travel_itinerary_20241109_210217.pdf", "Travel Itinerary")