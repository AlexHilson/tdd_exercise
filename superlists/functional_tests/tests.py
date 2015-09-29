import unittest

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitor(LiveServerTestCase): 

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
        # A user named Edith visits homepage of to-do app.
        self.browser.get(self.live_server_url)

        # Edith notices that the title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is prompted to enter a to-do item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types 'Buy peacock feathers' into a text box.
        inputbox.send_keys('Buy peacock feathers')
        
        # When she hits enter, they are taken to a new URL, and the page 
        # lists "1. Buy peacock feathers" as an item in a to-do list table.
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_text_in_todo_list('1: Buy peacock feathers')

        # There is still a text box they can use to add another item. Edith
        # enters "Use peacock feathers to make a fly".
        # When she hits enter, the page updates and the page shows both items.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_text_in_todo_list('1: Buy peacock feathers')
        self.check_text_in_todo_list('2: Use peacock feathers to make a fly')

        # A new user, Francis, visits the site.
        ## Start a new browser session to make sure no information is carried
        ## across in cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Francis visits the home page. There is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('User peacock feathers to make a fly', page_text)
        
        # He starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        
        # He gets his own unique URL.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        
        # Again, there is no trace of Edith's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
        self.fail("Finish the test!")