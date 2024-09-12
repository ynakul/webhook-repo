#GitHub Webhook to MongoDB with Flask
Installation
Install Dependencies

Create a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


Install required packages:
pip install -r requirements.txt
Run MongoDB

Ensure MongoDB is running locally on localhost:27017.

Run the Flask Server

Start the Flask server:
python app.py

Expose Local Server with ngrok

To make your local Flask server accessible to GitHub for webhook events, use ngrok:
ngrok http 5000
Note the public URL provided by ngrok and use it for the GitHub webhook configuration.

Importance of ngrok
Ngrok is used to expose your local development server to the public internet. This is necessary for GitHub to send webhook events to your Flask application running on localhost. The public URL provided by ngrok serves as the endpoint that GitHub will call when triggering webhooks.

