import json
import boto3

lex_client = boto3.client('lexv2-runtime', region_name="us-east-1")

LEX_BOT_ID = "XV4SJMRDHD"
LEX_BOT_ALIAS_ID = "TSTALIASID"

def lambda_handler(event, context):

    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "Hello")

        lex_response = lex_client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId="en_US",
            sessionId="user-session",
            text=user_message
        )

        lex_message = "Sorry, I didn't get that."
        if "messages" in lex_response and len(lex_response["messages"]) > 0:
            lex_message = lex_response["messages"][0]["content"]

        return {
            "statusCode": 200,
            "body": json.dumps({"response": lex_message}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }