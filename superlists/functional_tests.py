import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitor(unittest.TestCase): 

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_text_in_todo_list(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_start_and_retrieve_list(self):
        # User visits homepage of to-do app.
        self.browser.get('http://localhost:8000')

        # They notice that the title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # They are prompted to enter a to-do item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # They type 'Buy peacock feathers' into a text box.
        # When they hit enter, the page updates and the page lists
        # "1. Buy peacock feathers" as an item in a to-do list table.
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.check_text_in_todo_list('1: Buy peacock feathers')

        # There is still a text box they can use to add another item. They
        # enter "Use peacock feathers to make a fly"
        # When they hit enter, the page updates and the page shows both items.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_text_in_todo_list('1: Buy peacock feathers')
        self.check_text_in_todo_list('2: Use peacock feathers to make a fly')

        self.fail("Finish the test!")
        
if __name__ == '__main__':
    unittest.main()
