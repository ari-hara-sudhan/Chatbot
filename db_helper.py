from fastapi import FastAPI
from fastapi.responses import Request
import JSONResponse
import mysql.connector

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'rupinsspa'
}

app = FastAPI()

def validate_phone_number(phone_number):
    # Implement your phone number validation logic here
    # For example, check if the phone number is in the correct format
    return True  # Placeholder validation, replace with actual logic

def book_appointment(parameters: dict):
    try:
        phone_number = parameters.get('phone-number')
        
        if not phone_number:
            return {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Phone number not provided."
                            ]
                        }
                    }
                ]
            }

        if not validate_phone_number(phone_number):
            return {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Invalid phone number format."
                            ]
                        }
                    }
                ]
            }

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Verify phone number
        cursor.execute("SELECT customer_id, name FROM customers WHERE phone_number = %s", (phone_number,))
        customer = cursor.fetchone()

        if not customer:
            cursor.close()
            connection.close()
            return {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Your mobile number is not registered. Please contact Rupins for assistance."
                            ]
                        }
                    }
                ]
            }

        # Ask for date and time
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            f"Welcome, {customer[1]}! Please Enter ur date and time like ex:tuesday 5pm"
                        ]
                    }
                }
            ],
            "phone_number": phone_number,  # Include phone number in the response
            "customer_id": customer[0]      # Include customer ID in the response
        }

    except mysql.connector.Error as e:
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Database error"
                        ]
                    }
                }
            ]
        }

    except Exception as e:
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Server error"
                        ]
                    }
                }
            ]
        }



    



def store_appointment(parameters, phone_number: str):
    # Extract date string from parameters and convert it to a string
    datetime_str = str(parameters.get('datestr', ''))

    # Check if datetime or phone number is not provided
    if not datetime_str or not phone_number:
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Datetime or phone number not provided."
                        ]
                    }
                }
            ]
        }

    # Try to connect to the database
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Store appointment details
        cursor.execute("INSERT INTO appointments (phone_number, appointment_date) VALUES (%s, %s)",
                       (phone_number, datetime_str))
        connection.commit()

        # Close database connection
        cursor.close()
        connection.close()

        # Return success message
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Your appointment is successfully booked!"
                        ]
                    }
                }
            ]
        }

    # Handle database errors
    except mysql.connector.Error as e:
        # Log the error for debugging purposes
        print("Database Error:", e)
        # Return an error message with details of the database error
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            f"An error occurred while processing your request. Database Error: {str(e)}"
                        ]
                    }
                }
            ]
        }