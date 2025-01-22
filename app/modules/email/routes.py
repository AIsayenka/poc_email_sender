from flask import Blueprint, request, jsonify
from app.modules.email.logic.send_email_task import send_email_task
from app.modules.email.logic.render_template import render_template
import uuid
import os
from app.modules.email.enums.request_status import RequestStatus
from app.modules.email.enums.email_status import EmailStatus
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import current_app

api = Blueprint("api", __name__)

executor = ThreadPoolExecutor(max_workers=int(os.getenv("CONCURENT_SENDERS", 2)))

@api.route("/send-email", methods=["POST"])
def send_email_api():
    request_id = uuid.uuid4()
    try:
        
        data = request.json
        if not all(key in data for key in ("email_body", "recipients", "personalization_data")):
            return jsonify({"error": "Missing required fields"}), 400

        template = data["email_body"]  # Dynamic template content
        recipients = data["recipients"]
        
        context = data.get("personalization_data", {})
        statuses = {}
        
        # Prepare tasks for concurrent execution
        futures = []
        for recipient in recipients:
            email_id = str(uuid.uuid4())
            body = render_template(template, context.get(recipient, {}))
            statuses[email_id] = EmailStatus.PENDING

            # Submit email sending task to the executor
            futures.append(
                executor.submit(send_email_task, email_id, recipient, body, current_app._get_current_object())
            )

        # Process results as they complete
        for future in as_completed(futures):
            try:
                email_id, status = future.result()
                statuses[email_id] = status
            except Exception as e:
                print(f"Error sending email: {e}")

        print("EMAIL STATUSES: ", statuses)
        
        return jsonify({"status": RequestStatus.SUBMITTED, "request_id": request_id}), 202

    except Exception as e:
        return jsonify({"status": RequestStatus.ERROR, "request_id": request_id, "details": str(e)}), 500