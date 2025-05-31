from flask import Flask, redirect
from link_generator import get_next_phone_number, generate_whatsapp_link

app = Flask(__name__)

@app.route('/redirect')
def handle_redirect():
    phone_number = get_next_phone_number()
    if phone_number:
        whatsapp_link = generate_whatsapp_link(phone_number)
        if whatsapp_link:
            return redirect(whatsapp_link)
        else:
            return "Error generating WhatsApp link.", 500
    else:
        return "No phone numbers available.", 500

if __name__ == '__main__':
    # Ensure Flask and link_generator are installed if running in a new environment
    # For now, assume they are available.
    app.run(debug=True, port=5000)
