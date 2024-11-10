# Wandere.ai-Backend

This folder contains the backend services for the AI Meets Wanderlust project. The backend generates customized travel itineraries, handles user authentication, and manages data storage. It is built using Python and Flask, with MongoDB Atlas for database management and Auth0 for secure authentication.

## Key Components

1. **User Authentication**: 
   - **Auth0 Integration** for secure user login and registration.
   - Supports social logins (Google, GitHub) and passwordless login via OTP.

2. **Database**:
   - **MongoDB Atlas** for robust data storage and management.
   - Stores user profiles, travel preferences, chat history, itinerary details, and other essential information.

3. **APIs and AI Integration**:
   - **Hugging Face API** for generating personalized travel recommendations.
   - **OpenRouteService (ORS)** for real-time location and route mapping.

4. **Email Service**:
   - **SendGrid** for sending personalized itinerary PDFs directly to users’ email.
   - Configurable SMTP setup with Gmail as an alternative.

5. **File Storage**:
   - **AWS S3** for managing document storage, ensuring easy access to generated itineraries.

## Tech Stack

- **Language**: Python
- **Frameworks**: FastAPI, Flask
- **Database**: MongoDB Atlas
- **Other Tools**: Hugging Face, OpenRouteService, Auth0, AWS S3, SendGrid



### Installation
1. **Clone the repository**:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. **Install dependencies:**
  ```
  pip install -r requirements.txt
  ```

3.**Set up Environment Variables:**
Create a .env file and add your MongoDB, Auth0, and any other API keys:

```
# API Keys
API_KEY="YOUR_HUGGINGFACE_API_KEY"
ORS_API_KEY="YOUR_OPENROUTESERVICE_API_KEY"

# MongoDB Atlas
MONGODB_USERNAME="YOUR_MONGODB_USERNAME"
MONGODB_PASSWORD="YOUR_MONGODB_PASSWORD"
MONGODB_URL="YOUR_MONGODB_CLUSTER_URL"

# SendGrid Email API
SENDGRID_API_KEY="YOUR_SENDGRID_API_KEY"
SENDER_EMAIL="YOUR_SENDER_EMAIL_ADDRESS"

# AWS S3 Configuration
S3_BUCKET_NAME="YOUR_S3_BUCKET_NAME"
S3_ENDPOINT_URL="YOUR_S3_ENDPOINT_URL"
ACCESS_KEY_S3_ID="YOUR_S3_ACCESS_KEY_ID"
SECRET_ACCESS_KEY_S3="YOUR_S3_SECRET_ACCESS_KEY"
```

4. **Run the Application:**
```
python filename.py
```


- Install https://wkhtmltopdf.org/ for pdf generation. 
