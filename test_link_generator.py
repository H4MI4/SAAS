import unittest
import link_generator # To allow modifying phone_numbers and current_index

class TestLinkGenerator(unittest.TestCase):

    def setUp(self):
        # Reset state before each test
        link_generator.current_index = 0
        # We need to assign to link_generator.phone_numbers directly,
        # not create a new local variable 'phone_numbers'.
        link_generator.phone_numbers = []

    def test_get_next_phone_number_cycles_and_wraps(self):
        link_generator.phone_numbers = ['1', '2', '3']
        self.assertEqual(link_generator.get_next_phone_number(), '1')
        self.assertEqual(link_generator.get_next_phone_number(), '2')
        self.assertEqual(link_generator.get_next_phone_number(), '3')
        self.assertEqual(link_generator.get_next_phone_number(), '1') # Wraps around

    def test_get_next_phone_number_empty_list(self):
        link_generator.phone_numbers = []
        self.assertIsNone(link_generator.get_next_phone_number())

    def test_get_next_phone_number_single_number(self):
        link_generator.phone_numbers = ['123']
        self.assertEqual(link_generator.get_next_phone_number(), '123')
        self.assertEqual(link_generator.get_next_phone_number(), '123') # Stays on single number

    def test_generate_whatsapp_link_valid_number(self):
        self.assertEqual(link_generator.generate_whatsapp_link('1234567890'), 'https://wa.me/1234567890')

    def test_generate_whatsapp_link_with_plus_and_spaces(self):
        self.assertEqual(link_generator.generate_whatsapp_link('+1 23 456 7890'), 'https://wa.me/1234567890')

    def test_generate_whatsapp_link_empty_string_number(self):
        # This test relies on the modification made to generate_whatsapp_link
        # to return None if the cleaned number is empty.
        self.assertIsNone(link_generator.generate_whatsapp_link(''))

    def test_generate_whatsapp_link_only_spaces_and_plus(self):
        # Similar to empty string, but with characters that get stripped
        self.assertIsNone(link_generator.generate_whatsapp_link('+   +'))

    def test_generate_whatsapp_link_none_number(self):
        self.assertIsNone(link_generator.generate_whatsapp_link(None))

if __name__ == '__main__':
    unittest.main()
