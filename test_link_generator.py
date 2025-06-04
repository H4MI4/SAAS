import unittest
# Import the manager instance and the public functions
from link_generator import manager, get_next_phone_number, generate_whatsapp_link, add_phone_number_to_list, remove_phone_number_from_list, get_all_phone_numbers

class TestLinkGenerator(unittest.TestCase):

    def setUp(self):
        # Reset the state of the global manager before each test
        # Directly manipulate manager's internal list for clean test state
        manager.numbers = []
        manager.current_index = 0

    def test_add_and_get_all_numbers(self):
        self.assertTrue(add_phone_number_to_list("111"))
        self.assertTrue(add_phone_number_to_list("222"))
        self.assertEqual(get_all_phone_numbers(), ["111", "222"])

    def test_add_duplicate_number(self):
        add_phone_number_to_list("111")
        self.assertFalse(add_phone_number_to_list("111")) # Try adding duplicate
        self.assertEqual(get_all_phone_numbers(), ["111"])

    def test_add_empty_or_none_number(self):
        self.assertFalse(add_phone_number_to_list(""))
        self.assertFalse(add_phone_number_to_list(None))
        self.assertEqual(get_all_phone_numbers(), [])


    def test_remove_number(self):
        add_phone_number_to_list("111")
        add_phone_number_to_list("222")
        self.assertTrue(remove_phone_number_from_list("111"))
        self.assertEqual(get_all_phone_numbers(), ["222"])
        self.assertFalse(remove_phone_number_from_list("nonexistent")) # Try removing non-existent
        self.assertEqual(get_all_phone_numbers(), ["222"])

    def test_get_next_phone_number_cycles_and_wraps(self):
        add_phone_number_to_list('1')
        add_phone_number_to_list('2')
        add_phone_number_to_list('3')
        self.assertEqual(get_next_phone_number(), '1')
        self.assertEqual(get_next_phone_number(), '2')
        self.assertEqual(get_next_phone_number(), '3')
        self.assertEqual(get_next_phone_number(), '1') # Wraps

    def test_get_next_phone_number_empty_list(self):
        self.assertIsNone(get_next_phone_number())

    def test_get_next_phone_number_single_number(self):
        add_phone_number_to_list('123')
        self.assertEqual(get_next_phone_number(), '123')
        self.assertEqual(get_next_phone_number(), '123') # Stays on single number

    def test_remove_number_updates_index_correctly_simple_reset_case(self):
        # Verify index adjustment when removing an item while the pointer is at
        # the end of the list. After removing a number before the current index
        # the pointer should move left to keep pointing at the same logical
        # element.
        add_phone_number_to_list('1')
        add_phone_number_to_list('2')
        add_phone_number_to_list('3') # numbers: ['1', '2', '3'], index: 0

        get_next_phone_number() # returns '1', index becomes 1 (for '2')
        get_next_phone_number() # returns '2', index becomes 2 (for '3')

        remove_phone_number_from_list('1')  # remove first element while index points to last
        # After removal, index should decrease by one to keep targeting '3'
        self.assertEqual(manager.current_index, 1)
        self.assertEqual(get_next_phone_number(), '3')  # Should now get '3'
        self.assertEqual(get_next_phone_number(), '2')  # Then wraps to '2'
        self.assertEqual(get_next_phone_number(), '3')

    def test_remove_last_remaining_number(self):
        add_phone_number_to_list('1')
        remove_phone_number_from_list('1')
        self.assertEqual(get_all_phone_numbers(), [])
        self.assertIsNone(get_next_phone_number())
        self.assertEqual(manager.current_index, 0)

    def test_remove_number_maintains_order_and_index_for_next_item(self):
        # Test case: ['a', 'b', 'c', 'd'], index = 1 (pointing to 'b')
        # Remove 'b'. List becomes: ['a', 'c', 'd']. Index should ideally point to 'c' (still index 1).
        add_phone_number_to_list('a')
        add_phone_number_to_list('b')
        add_phone_number_to_list('c')
        add_phone_number_to_list('d')

        get_next_phone_number() # Returns 'a', index is now 1 (pointing to 'b')
        self.assertEqual(manager.current_index, 1)

        remove_phone_number_from_list('b') # List: ['a', 'c', 'd']
        # In current remove_number, if index was 1, and len(numbers) is 3, index 1 is still valid.
        # It should not reset to 0 unless it was >= len(numbers)
        self.assertEqual(manager.current_index, 1) # Index should still be 1, now pointing to 'c'
        self.assertEqual(get_next_phone_number(), 'c') # Should pick up 'c'
        self.assertEqual(get_next_phone_number(), 'd')
        self.assertEqual(get_next_phone_number(), 'a')

    def test_remove_number_before_current_index_shifts_index(self):
        add_phone_number_to_list('a')
        add_phone_number_to_list('b')
        add_phone_number_to_list('c')
        add_phone_number_to_list('d')

        # Cycle twice so current_index points to 'c'
        self.assertEqual(get_next_phone_number(), 'a')
        self.assertEqual(get_next_phone_number(), 'b')
        self.assertEqual(manager.current_index, 2)

        remove_phone_number_from_list('b')  # Remove element before current index
        # Index should shift left to keep pointing at 'c'
        self.assertEqual(manager.current_index, 1)
        self.assertEqual(get_next_phone_number(), 'c')


    # generate_whatsapp_link tests remain largely the same as they are pure functions
    def test_generate_whatsapp_link_valid_number(self):
        self.assertEqual(generate_whatsapp_link('1234567890'), 'https://wa.me/1234567890')

    def test_generate_whatsapp_link_with_plus_and_spaces(self):
        self.assertEqual(generate_whatsapp_link('+1 23 456 7890'), 'https://wa.me/1234567890')

    def test_generate_whatsapp_link_empty_string_number(self):
        self.assertIsNone(generate_whatsapp_link(''))

    def test_generate_whatsapp_link_only_spaces_and_plus(self):
        self.assertIsNone(generate_whatsapp_link(' + '))

    def test_generate_whatsapp_link_none_number(self):
        self.assertIsNone(generate_whatsapp_link(None))

if __name__ == '__main__':
    unittest.main()
