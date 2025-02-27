import json

def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']

    if intent_name == "GreetingIntent":
        message = "Hi there! How can I assist you today?"
    elif intent_name == "ThankYouIntent":
        message = "You're welcome! Let me know if you need anything else."
    elif intent_name == "DiningSuggestionsIntent":
        slots = event['sessionState']['intent']['slots']
        location = slots['Location']['value']['interpretedValue']
        cuisine = slots['Cuisine']['value']['interpretedValue']
        dining_time = slots['DiningTime']['value']['interpretedValue']
        num_people = slots['NumberOfPeople']['value']['interpretedValue']
        email = slots['Email']['value']['interpretedValue']

        message = f"Got it! Finding {cuisine} restaurants in {location} for {num_people} people at {dining_time}. You will receive an email at {email}."

    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

    return response
