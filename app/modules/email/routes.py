from flask import Blueprint, request, jsonify
from .logic.send_email import send_email
from .logic.render_template import render_template

api = Blueprint("api", __name__)

@api.route("/send-email", methods=["POST"])
def send_email_api():
    try:
        data = request.json
        if not all(key in data for key in ("email_body", "recipients", "personalization_data")):
            return jsonify({"error": "Missing required fields"}), 400

        template = data["email_body"]  # Dynamic template content
        recipients = data["recipients"]
        
        context = data.get("personalization_data", {})

        # Render the template with provided context
        for recipient in recipients:
            body = render_template(template, context.get(recipient, {}))
            
            # Send the email
            send_email(recipient, body)
        
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500