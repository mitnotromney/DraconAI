                 
from flask import Flask, request, jsonify
import requests  # Assuming you use requests library to interact with GPT-4 API

app = Flask(__name__)

# Define the GPT-4 API endpoint and API key
GPT4_API_URL = 'https://api.openai.com/v1/chat/completions'
API_KEY = ''  # Replace with your actual API key

def query_gpt4(message):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    data = {'message': message}
    response = requests.post(GPT4_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('response')
    else:
        return 'Error: Unable to process your request'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']

    # Customizing the prompt or context based on user's message
    prompt = f"User: {user_message}\nBot:"

    # Query GPT-4 API with custom prompt
    bot_response = query_gpt4(prompt)

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
