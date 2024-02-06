from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# WhatsApp Cloud API endpoint and authentication details
WHATSAPP_API_URL = 'https://graph.facebook.com/v17.0/1399135125402/messages'
API_KEY = 'ctjKZC39jwuLF3p6Uk9LDZB2aAhw3gX86r3ZAPjpLse3dGHxl5Xmfcp8R0UlzFmVRajvlLkpCeM5A22P64xx7ISSosKuKRXBv7jZAxZBOcDa1hT4cBvr6ATEZAMVoxA4umM'


@app.route('/send', methods=['POST'])
def send_message():
    # Get the message data from the request
    message_data = request.get_json()

    # Extract the necessary information
    recipients = message_data.get('recipients')
    template_name = message_data.get('template_name')
    template_variables = message_data.get('template_variables', {})

    if not recipients or not template_name:
        return jsonify({"error": "Missing required parameters"}), 400

    # Modify template variables to include recipient names
    variable_names = template_variables.get('variable1', '').split(',')
    for i, recipient in enumerate(recipients):
        if i < len(variable_names):
            template_variables[f'user{i+1}'] = variable_names[i]

        # Construct payload for WhatsApp message
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": template_variables.get(f'user{i+1}', '')
                            },
                            {
                                "type": "text",
                                "text": template_variables.get('variable2', '')
                            },
                            {
                                "type": "text",
                                "text": template_variables.get('variable3', '')
                            }
                        ]
                    }
                ]
            }
        }

        # Include the access token as authorization headers
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        # Send the message using the requests library
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

        # Get the response data from the API
        response_data = response.json()

        # Print the response body
        print(f"WhatsApp API Response for {recipient}:")
        print(response_data)

    return jsonify({"message": "Messages sent successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




