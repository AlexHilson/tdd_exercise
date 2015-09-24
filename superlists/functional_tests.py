import unittest

from selenium import webdriver

class NewVisitor(unittest.TestCase): 

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_start_and_retrieve_list(self):
        # User visits homepage of to-do app.
        self.browser.get('http://localhost:8000')

        # They notice that the title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)

if __name__ == '__main__':
    unittest.main()
