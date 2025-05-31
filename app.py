from flask import Flask, redirect, render_template, request, url_for
from link_generator import (
    get_next_phone_number, generate_whatsapp_link,
    get_all_phone_numbers, add_phone_number_to_list, remove_phone_number_from_list
)

app = Flask(__name__)
# app.secret_key = 'your secret key' # Needed for flash messages, can add later

@app.route('/')
def index():
    current_phone_numbers = get_all_phone_numbers()
    return render_template('index.html', phone_numbers=current_phone_numbers)

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

@app.route('/add_number', methods=['POST']) # Renamed route
def add_number(): # Renamed function
    number = request.form.get('phone_number')
    if number:
        add_phone_number_to_list(number)
        # flash(f"Number {number} added successfully!", "success")
    # else:
        # flash("Failed to add number. Input was empty.", "error")
    return redirect(url_for('index'))

@app.route('/remove_number', methods=['POST']) # Renamed route
def remove_number(): # Renamed function
    number_to_remove = request.form.get('phone_number_to_remove')
    if number_to_remove:
        remove_phone_number_from_list(number_to_remove)
        # flash(f"Number {number_to_remove} removed successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure Flask and link_generator are installed if running in a new environment
    # For now, assume they are available.
    app.run(debug=True, port=5000)
