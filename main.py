from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import mysql.connector
from db_helper import book_appointment, store_appointment 

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'rupinsspa'
}

app = FastAPI()
phone_number = None  # Initialize phone number as None

@app.post("/")
async def handle_request(request: Request):
    global phone_number  # Access the phone_number variable defined outside the function
    try:
        payload = await request.json()

        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']

        if intent == "Verify.number":
            response = book_appointment(parameters)
            phone_number = parameters.get('phone-number')  # Update phone_number variable
            return JSONResponse(content=response, status_code=200)
        elif intent == "date.time":
            response = store_appointment(parameters, phone_number)  # Pass phone_number to store_appointment
            return JSONResponse(content=response, status_code=200)
       

    except Exception as e:
        return JSONResponse(content={"message": "Error processing request"}, status_code=500)
