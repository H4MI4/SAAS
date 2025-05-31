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
            # If the number to remove is the one at current_index,
            # and it's not the only number, the next get_next_number_for_robin
            # should ideally serve the number that *would have been next*.
            # However, simple removal and index reset/adjustment is also common.
            # Current implementation: if current_index is beyond the new list end, reset.

            # Store current number to see if it's the one being removed
            # and if it affects the index logic for get_next_number_for_robin
            num_at_current_index = None
            if self.numbers and self.current_index < len(self.numbers):
                 num_at_current_index = self.numbers[self.current_index]

            self.numbers.remove(number_str)

            if not self.numbers:
                self.current_index = 0
            elif self.current_index >= len(self.numbers):
                 # If the removed number was before or at current_index,
                 # and current_index is now out of bounds, wrap around or reset.
                 self.current_index = 0 # Reset to start for simplicity after removal
            # Optional: More sophisticated index adjustment if `num_at_current_index == number_str`
            # For example, if the removed number was what current_index was pointing to,
            # current_index effectively should point to the "next" item in the modified list,
            # which means it might not need to change if subsequent items shifted left.
            # But if it was the last item, or if current_index was beyond the removed item,
            # it might need adjustment.
            # The current logic of resetting to 0 if index is out of bounds is safe.

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
