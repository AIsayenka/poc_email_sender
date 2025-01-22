from flask import Blueprint, request, jsonify
from .logic.send_email import send_email
from .logic.render_template import render_template

api = Blueprint("api", __name__)

@api.route("/send-email", methods=["POST"])
def send_email_api():
    try:
        data = request.json
        if not all(key in data for key in ("template", "recipients", "subject")):
            return jsonify({"error": "Missing required fields"}), 400

        template = data["template"]  # Dynamic template content
        recipients = data["recipients"]
        subject = data["subject"]
        context = data.get("context", {})

        # Render the template with provided context
        body = render_template(template, context)
        print("BODY")
        print(body)
        
        print("RECIPIENT")
        print(recipients)
        # Send the email
        send_email(subject, recipients, body)
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500