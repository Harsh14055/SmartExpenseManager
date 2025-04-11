from flask import Blueprint, request, jsonify
from transformers import pipeline

# Create a Blueprint for the chatbot
chatbot_bp = Blueprint("chatbot", __name__)

# Load NLP model (You can replace with a better model later)
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    # Generate response using Transformer model
    response = qa_pipeline(user_message)[0]['generated_text']
    
    return jsonify({"response": response})
