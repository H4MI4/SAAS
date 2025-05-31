# Link generation logic

phone_numbers = ['+11111111111', '+22222222222', '+33333333333'] # Example numbers
current_index = 0

def get_next_phone_number():
    global current_index
    if not phone_numbers:
        return None

    number = phone_numbers[current_index]
    current_index = (current_index + 1) % len(phone_numbers)
    return number

def generate_whatsapp_link(phone_number):
    if not phone_number:
        return None
    # Basic cleaning: remove '+' and spaces. More robust cleaning can be added later.
    clean_number = phone_number.replace('+', '').replace(' ', '')
    if not clean_number: # Add this check
        return None
    return f"https://wa.me/{clean_number}"

# Example usage (optional)
# if __name__ == '__main__':
#     num = get_next_phone_number()
#     if num:
#         print(generate_whatsapp_link(num))
