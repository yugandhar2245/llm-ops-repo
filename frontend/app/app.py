from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

FASTAPI_URL = "http://backend-service:8000/chat"  # Change this if needed  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response = requests.post(FASTAPI_URL, json={
        "messages": user_message,
        "thread_id": "aa1234"  # You can modify this as needed
    })
    
    if response.status_code == 200:
        response_data = response.json()
        return jsonify({"response": response_data['response']})
    else:
        return jsonify({"response": "Error from API"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
