from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Wendy has heard about an online to-do list site. She goes to it's home page using her Web browser.
        self.browser.get('http://localhost:8000')

        # The home page title, and a heading, tells her she's looking at the To-Do list site.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # The home page has a text box that invites her to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # She types "Buy peacock feathers". (She likes to make fly-fishing lures.)
        inputbox.send_keys('Buy peacock feathers')
        # She hits enter and the page updates.
        inputbox.send_keys(Keys.ENTER)
        
        # Now the page lists "1: Buy peacock feathers"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )

        # There is still a text box inviting her to add another item.
        self.fail('Finish the test!')
        
        # She types "Use peacock feathers to make a fly"

        # She hits enter and the page updates again.
        
        # Now the page lists both of her items.

        # Wendy notices that the site has generated a unique URL for her list, with some explanatory text to that effect.
        # She visits that URL and sees that her list is still there.

        # She calls it a day.

if __name__ == '__main__':
    unittest.main()
        
