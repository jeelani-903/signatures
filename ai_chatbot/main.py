# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.utils import formataddr
# import ollama
# import sys
# import json
# import re
# from datetime import datetime

# app = Flask(__name__)

# SUPERVISOR_EMAIL = "digital@seapol.com"
# SENDER_EMAIL = "mohammedjeelani903@gmail.com"
# SENDER_PASSWORD = "zeil scbo taox begj"

# user_sessions = {}

# with open("knowledge_base.json", "r", encoding="utf-8") as f:
#     scraped_content = json.load(f)

# @app.route('/reset_session', methods=['POST'])
# def reset_session():
#     user_ip = request.remote_addr
#     user_sessions.pop(user_ip, None)
#     return jsonify({"status": "session cleared"})

# def generate_query_id():
#     return f"Q{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

# def send_email_notification(name, contact, email, query, query_id):
#     subject = f"New User Query Received - {query_id}"
#     body = (
#         f"A new query has been submitted by a user.\n\n"
#         f"📌 Query ID: {query_id}\n"
#         f"👤 Name: {name}\n"
#         f"📞 Contact Number: {contact}\n"
#         f"📧 Email: {email}\n"
#         f"📜 Query: {query}\n\n"
#         f"You can reply to this email to contact the user directly."
#     )

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = formataddr((name, SENDER_EMAIL))
#     msg["To"] = SUPERVISOR_EMAIL
#     msg["Reply-To"] = email

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)
#             server.send_message(msg)
#     except Exception as e:
#         print(f"❌ Error sending email: {e}")

# def send_user_confirmation_email(name, email, query_id):
#     subject = f"Your Query Received - {query_id}"
#     body = f"""
#     <html>
#     <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
#         <div style="text-align: center;">
#             <img src="Seapol_Logo.jpg" alt="Seapol Logo" style="width: 150px;" />
#         </div>
#         <h2>Hello {name},</h2>
#         <p>Thank you for contacting <strong>Seapol</strong>.</p>
#         <p>Your query has been received and is being reviewed by our support team.</p>
#         <p><strong>🆔 Query ID:</strong> {query_id}</p>
#         <p>We’ll get back to you as soon as possible.</p>
#         <p>📞 <strong>+91 12345 67890</strong><br>
#         📧 <strong>digital@seapol.com</strong></p>
#         <br><p>Warm regards,<br><strong>Team Seapol</strong></p>
#     </body>
#     </html>
#     """
#     msg = MIMEMultipart("alternative")
#     msg["Subject"] = subject
#     msg["From"] = formataddr(("Seapol Support", SENDER_EMAIL))
#     msg["To"] = email
#     msg.attach(MIMEText(body, "html"))

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)
#             server.sendmail(SENDER_EMAIL, email, msg.as_string())
#     except Exception as e:
#         print(f"❌ Error sending confirmation email to user: {e}")

# def save_user_info(name, contact, email, query, query_id):
#     file_path = "customer_queries.xlsx"
#     if os.path.exists(file_path):
#         df = pd.read_excel(file_path)
#     else:
#         df = pd.DataFrame(columns=["Query ID", "Name", "Contact", "Email", "Query", "Reply"])
#     df = pd.concat([df, pd.DataFrame([{
#         "Query ID": query_id,
#         "Name": name,
#         "Contact": contact,
#         "Email": email,
#         "Query": query,
#         "Reply": ""
#     }])], ignore_index=True)
#     df.to_excel(file_path, index=False)

# def log_chat(user_ip, user_input, response):
#     log_file = "chat_logs.xlsx"
#     now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     row = {
#         "Timestamp": now,
#         "IP Address": user_ip,
#         "User Input": user_input,
#         "Bot Response": response
#     }

#     if os.path.exists(log_file):
#         df = pd.read_excel(log_file)
#         df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
#     else:
#         df = pd.DataFrame([row])

#     df.to_excel(log_file, index=False)

# def is_informational_query(text):
#     keywords = ["about seapol", "what is seapol", "information about seapol", "seapol company", "services", "describe"]
#     return any(kw in text.lower() for kw in keywords)

# def is_support_request(text):
#     patterns = ["question", "query", "doubt", "speak", "talk", "support", "clarification", "representative"]
#     return any(p in text.lower() for p in patterns)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     user_input = data.get("user_input", "").strip()
#     user_ip = request.remote_addr

#     if user_input == "Want to know about our Seapol":
#         reply = (
#             "Seapol Group is a leading multimodal logistics and shipping company headquartered in Chennai, India. "
#             "We offer a wide range of integrated services including freight forwarding, customs clearance, container operations, port infrastructure, air cargo, and trading. "
#             "Our group includes divisions like Seaport Logistics, Seaport Shipping, Seaport Lines, Seapol Port, Eastern Bulk Trading, and Airpol Xpress. "
#             "With a strong presence in major Indian ports and global outreach, Seapol is committed to delivering excellence in end-to-end logistics solutions."
#         )
#         log_chat(user_ip, user_input, reply)
#         return jsonify({"response": reply})

#     # Location Logic
#     if user_input.lower() in ["location", "branch", "where are you located", "office locations", "branches", "locations"]:
#         options = (
#             "We have two main offices:\n\n"
#             "**Chennai, India**\n"
#             "Seapol Group of Companies\n"
#             "📞 +91 44 42288111 / +91 44 25229006\n"
#             "📧 info@seapol.com\n\n"
#             "**Tuticorin, India**\n"
#             "SEAPORT LOGISTICS Private Limited\n"
#             "📍 B-32, World Trade Avenue, Harbour Estate, Tuticorin – 628 004\n"
#             "📞 +91 461 4005700 / +91 461 2353590 / +91 461 2353707\n"
#             "📧 infotuti@seapol.com\n\n"
#             "We also have branch offices for specific service divisions:\n"
#             "1. Logistics Division\n"
#             "2. Shipping Division\n"
#             "3. Container Division\n"
#             "4. Port Infrastructure Division\n"
#             "5. Trading Division\n\n"
#             "Please enter the option number to know locations for that division."
#         )
#         user_sessions[user_ip] = {"stage": "awaiting_division_choice"}
#         return jsonify({"response": options})

#     if user_sessions.get(user_ip, {}).get("stage") == "awaiting_division_choice":
#         div_choice = user_input.strip()
#         division_locations = {
#             "1": """**Logistics Division**

# **CHENNAI**\nSEAPORT LOGISTICS PRIVATE LIMITED\nDheen Estate, New No-85, Old No-42, Moore Street, Chennai – 600 001\n📞 +91 44 42288111 / +91 44 42160111 / +91 44 25229006\n📧 logistics@seapol.com

# **TRICHY**\n📍 No-69w, Narayanapuram, Kottapattu, Airport, Near-Annai Ashramam, Trichy – 620 007\n📞 +91 431 2341195\n📧 infotrichy@seapol.com

# **TUTICORIN**\n📍 B-32, World Trade Avenue, Harbour Estate, Tuticorin – 628 004\n📞 +91 461 4005700 / +91 461 2353590 / +91 461 2353707\n📧 infotuti@seapol.com

# **KARAIKAL**\n📍 No.138, Nagore Road, Poosai Mandapam, Neravy, Karaikal -609604\n📞 +91 461 4005700 / +91 461 2353590\n📧 kppltrans@seapol.com

# **VISAKHAPATNAM**\n📍 Archana Building, First Floor, D.No 11-2-15/1, Daspalla Hills, Visakhapatnam – 530 003\n📞 +91 0891 2714371 / +91 0891 2783687\n📧 infovizag@seapol.com

# **HALDIA**\n📍 M-Block, Old CPT Complex, Chirinjibpur, Haldia – 721 604, West Bengal\n📞 +91 03224 252767 / +91 81700 20222\n📧 infohaldia@seapol.com""",
#             "2": """**Shipping Division**

# **CHENNAI**\nSeaport Shipping Pvt Ltd, Dheen Estate, Moore Street, Chennai – 600 001\n📞 +91 44 40468999\n📧 info@seaportshipping.in""",
#             "3": """**Container Division**

# **CHENNAI**\nSeaport Lines (India) Pvt Ltd, Dheen Estate, Moore Street, Chennai – 600 001\n📞 +91 44 40469900\n📧 info@seaportlines.com

# **SINGAPORE**\nSeaport Lines (Singapore) Pte Ltd\n📍 8, Shenton Way, #34-01 AXA Tower, Singapore 068811\n📧 singapore@seaportlines.com""",
#             "4": """**Port Infrastructure Division**

# **CHENNAI**\nSeapol Port Pvt Ltd, No-42, Dheen Estate, First Floor, Moore Street, Chennai – 600 001\n📞 +91 44 40469999\n📧 spplchennai@seapol.com

# **KARAIKAL**\nNo 38, Gnanaprakasam St, Near MOH Petrol Bunk, Karaikal – 609602\n📞 +91 4365 256624\n📧 spplkaraikal@seapol.com

# **VISAKHAPATNAM**\nArchana Building, Ground Floor, Door No .11-2-15/1, Daspalla Hills, Visakhapatnam – 530003\n📞 0891-2522789\n📧 spplvizag@seapol.com""",
#             "5": """**Trading Division**

# **CHENNAI**\nEasternbulk Trading & Shipping Pvt Ltd, Dheen Estate, New No-85, Old No-42, Moore Street, Chennai – 600 001\n📞 +91 97909 09004 / +91 44 42064401 / 02 / 03 / 04\n📧 info@easternbulk.in"""
#         }

#         response = division_locations.get(div_choice, "❗ Invalid option. Please enter a number between 1 and 5.")
#         log_chat(user_ip, user_input, response)
#         user_sessions.pop(user_ip, None)
#         return jsonify({"response": response})

#     # ... [rest of your existing code for FAQ, support, and Ollama AI] ...

#     try:
#         system_prompt = (
#             "You are a customer support assistant for Seapol, a logistics company. "
#             "Only answer questions related to Seapol, its services, or relevant business information. "
#             "Keep your responses short, professional, and to the point. Avoid unnecessary details or long paragraphs. "
#             "If the user asks about anything unrelated to Seapol, respond with: "
#             "'I'm only trained to answer Seapol-related queries. Please reach out to digital@seapol.com for anything else.'"
#         )
#         response = ollama.chat(model="llama3", messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_input}
#         ])
#         ai_reply = response.get("message", {}).get("content", None)
#         log_chat(user_ip, user_input, ai_reply)
#         return jsonify({"response": ai_reply[:700] if ai_reply else "I'm having trouble responding. Please try again."})
#     except Exception as e:
#         print(f"AI Error: {e}")
#         return jsonify({"response": "Sorry, I’m having trouble responding right now. Please try again later."})

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import ollama
import sys
import json
import re
from datetime import datetime

app = Flask(__name__)

SUPERVISOR_EMAIL = "digital@seapol.com"
SENDER_EMAIL = "mohammedjeelani903@gmail.com"
SENDER_PASSWORD = "zeil scbo taox begj"  # App password

user_sessions = {}

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    scraped_content = json.load(f)

@app.route('/reset_session', methods=['POST'])
def reset_session():
    user_ip = request.remote_addr
    user_sessions.pop(user_ip, None)
    return jsonify({"status": "session cleared"})

def generate_query_id():
    return f"Q{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

def send_email_notification(name, contact, email, query, query_id):
    subject = f"New User Query Received - {query_id}"
    body = (
        f"A new query has been submitted by a user.\n\n"
        f"📌 Query ID: {query_id}\n"
        f"👤 Name: {name}\n"
        f"📞 Contact Number: {contact}\n"
        f"📧 Email: {email}\n"
        f"📜 Query: {query}\n\n"
        f"You can reply to this email to contact the user directly."
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = formataddr((name, SENDER_EMAIL))
    msg["To"] = SUPERVISOR_EMAIL
    msg["Reply-To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("✅ Email sent to supervisor.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def send_user_confirmation_email(name, email, query_id):
    subject = f"Your Query Received - {query_id}"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <div style="text-align: center;">
            <img src="Seapol_Logo.jpg" alt="Seapol Logo" style="width: 150px;" />
        </div>
        <h2>Hello {name},</h2>
        <p>Thank you for contacting <strong>Seapol</strong>.</p>
        <p>Your query has been received and is being reviewed by our support team.</p>
        <p><strong>🆔 Query ID:</strong> {query_id}</p>
        <p>We’ll get back to you as soon as possible.</p>
        <p>📞 <strong>+91 12345 67890</strong><br>
        📧 <strong>digital@seapol.com</strong></p>
        <br><p>Warm regards,<br><strong>Team Seapol</strong></p>
    </body>
    </html>
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Seapol Support", SENDER_EMAIL))
    msg["To"] = email
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print("✅ Confirmation email sent to user.")
    except Exception as e:
        print(f"❌ Error sending confirmation email to user: {e}")

def save_user_info(name, contact, email, query, query_id):
    file_path = "customer_queries.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=["Query ID", "Name", "Contact", "Email", "Query", "Reply"])
    df = pd.concat([df, pd.DataFrame([{
        "Query ID": query_id,
        "Name": name,
        "Contact": contact,
        "Email": email,
        "Query": query,
        "Reply": ""
    }])], ignore_index=True)
    df.to_excel(file_path, index=False)
    print("✅ User query saved to Excel.")

def log_chat(user_ip, user_input, response):
    log_file = "chat_logs.xlsx"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row = {
        "Timestamp": now,
        "IP Address": user_ip,
        "User Input": user_input,
        "Bot Response": response
    }

    if os.path.exists(log_file):
        df = pd.read_excel(log_file)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(log_file, index=False)

def search_scraped_content(query):
    query = query.lower()
    for entry in scraped_content:
        if query in entry.get("content", "").lower():
            return entry["content"][:700]
    return None

def is_informational_query(text):
    keywords = ["about seapol", "what is seapol", "information about seapol", "seapol company", "services", "describe"]
    return any(kw in text.lower() for kw in keywords)

def is_support_request(text):
    patterns = ["question", "query", "doubt", "speak", "talk", "support", "clarification", "representative"]
    return any(p in text.lower() for p in patterns)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("user_input", "").strip()
    user_ip = request.remote_addr

    # Handle "Want to know about our Seapol"
    if user_input == "Want to know about our Seapol":
        manual_reply = (
            "Seapol Group is a leading multimodal logistics and shipping company headquartered in Chennai, India. "
            "We offer a wide range of integrated services including freight forwarding, customs clearance, container operations, port infrastructure, air cargo, and trading. "
            "Our group includes divisions like Seaport Logistics, Seaport Shipping, Seaport Lines, Seapol Port, Eastern Bulk Trading, and Airpol Xpress. "
            "With a strong presence in major Indian ports and global outreach, Seapol is committed to delivering excellence in end-to-end logistics solutions."
        )
        log_chat(user_ip, user_input, manual_reply)
        return jsonify({"response": manual_reply})


    if user_input == "Any questions or FAQ's about our company":
        user_sessions[user_ip] = {"stage": "ask_name"}
        return jsonify({"response": "Sure! May I know your name first?"})

    if user_input == "Track your goods with AWB number":
        return jsonify({"redirect": "https://www.track-trace.com/aircargo"})

    if user_input == "Services that are provided by Seapol":
        services = [
            {"name": "Seaport Logistics", "url": "https://seapol.com/logistics/"},
            {"name": "Seaport Shipping Pvt Ltd", "url": "https://seapol.com/shipping/"},
            {"name": "Seaport Lines (India) Pvt Ltd", "url": "https://seapol.com/container/"},
            {"name": "Seapol Port Pvt Ltd", "url": "https://seapol.com/port/"},
            {"name": "Eastern Bulk Trading & Shipping Pvt Ltd", "url": "https://seapol.com/trading/"},
            {"name": "Airpol Xpress Pvt Ltd", "url": "https://seapol.com/airpolxpress/"}
        ]
        return jsonify({"response": services})

    session = user_sessions.get(user_ip)
    if session:
        if session["stage"] == "ask_name":
            session["name"] = user_input.strip()
            session["stage"] = "ask_contact"
            return jsonify({"response": "Thanks! Please provide your contact number."})

        elif session["stage"] == "ask_contact":
            contact = user_input.strip()
            if not (contact.isdigit() and len(contact) == 10):
                return jsonify({"response": "❗ Please enter a valid 10-digit contact number."})
            session["contact"] = contact
            session["stage"] = "ask_email"
            return jsonify({"response": "Great! Now, please provide your email address."})

        elif session["stage"] == "ask_email":
            email = user_input.strip()
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, email):
                return jsonify({"response": "❗ Please enter a valid email address."})
            session["email"] = email
            session["stage"] = "ask_query"
            return jsonify({"response": "Thank you! Please type your query."})

        elif session["stage"] == "ask_query":
            session["query"] = user_input
            query_id = generate_query_id()
            name = session.get("name", "User")
            contact = session.get("contact", "Not Provided")
            email = session.get("email", "no-reply@seapol.com")
            query = session.get("query", "No query submitted.")

            save_user_info(name, contact, email, query, query_id)
            send_email_notification(name, contact, email, query, query_id)
            if email != "no-reply@seapol.com":
                send_user_confirmation_email(name, email, query_id)
            user_sessions.pop(user_ip, None)
            response_text = f"Thanks! We've recorded your query (ID: {query_id}). A representative will contact you soon.\n\n📞 +91 12345 67890\n📧 digital@seapol.com"
            log_chat(user_ip, user_input, response_text)
            return jsonify({"response": response_text})

    if is_support_request(user_input):
        user_sessions[user_ip] = {"stage": "ask_name"}
        return jsonify({"response": "Sure! May I know your name first?"})

    if is_informational_query(user_input):
        content = search_scraped_content("seapol")
        if content:
            log_chat(user_ip, user_input, content)
            return jsonify({"response": content})

    try:
        system_prompt = (
            "You are a customer support assistant for Seapol, a logistics company. "
            "Only answer questions related to Seapol, its services, or relevant business information. "
            "Keep your responses short, professional, and to the point. Avoid unnecessary details or long paragraphs. "
            "If the user asks about anything unrelated to Seapol, respond with: "
            "'I'm only trained to answer Seapol-related queries. Please reach out to digital@seapol.com for anything else.'"
        )
        response = ollama.chat(model="llama3", messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ])
        ai_reply = response.get("message", {}).get("content", None)
        log_chat(user_ip, user_input, ai_reply)
        return jsonify({"response": ai_reply[:700] if ai_reply else "I'm having trouble responding. Please try again."})
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"response": "Sorry, I’m having trouble responding right now. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True)