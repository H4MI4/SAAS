# Link generation logic

class PhoneNumberManager:
    def __init__(self):
        self.numbers = []
        self.current_index = 0

    def add_number(self, number_str):
        if number_str and isinstance(number_str, str) and number_str not in self.numbers:
            # Basic validation: ensure it's a non-empty string.
            self.numbers.append(number_str)
            return True
        return False

    def remove_number(self, number_str):
        if number_str in self.numbers:
            # Save the index of the number prior to removal so we can adjust
            # the round-robin pointer correctly.
            removed_index = self.numbers.index(number_str)
            self.numbers.remove(number_str)

            if not self.numbers:
                # List became empty; simply reset index
                self.current_index = 0
            else:
                if removed_index < self.current_index:
                    # Elements shifted left before the current index,
                    # so decrement to keep pointing at the same logical item
                    self.current_index -= 1
                elif removed_index == self.current_index and self.current_index >= len(self.numbers):
                    # Removed the element we were about to serve and it was the
                    # last element. Wrap to the start.
                    self.current_index = 0

            return True
        return False

    def get_all_numbers(self):
        return list(self.numbers) # Return a copy

    def get_next_number_for_robin(self):
        if not self.numbers:
            return None

        # Ensure current_index is valid even if list shrank and index wasn't adjusted perfectly elsewhere
        if self.current_index >= len(self.numbers):
            self.current_index = 0
            if not self.numbers: # List might have become empty due to concurrent modification
                 return None

        number = self.numbers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.numbers)
        return number

manager = PhoneNumberManager()

# --- Public API for the rest of the app ---
def get_next_phone_number():
    return manager.get_next_number_for_robin()

def add_phone_number_to_list(number_str):
    return manager.add_number(number_str)

def remove_phone_number_from_list(number_str):
    return manager.remove_number(number_str)

def get_all_phone_numbers():
    return manager.get_all_numbers()

def generate_whatsapp_link(phone_number): # Stays the same
    if not phone_number:
        return None
    # Basic cleaning: remove '+' and spaces. More robust cleaning can be added later.
    clean_number = phone_number.replace('+', '').replace(' ', '')
    if not clean_number: # Add this check
        return None
    return f"https://wa.me/{clean_number}"
