from selenium import webdriver
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

        # The home page tells her she's looking at the To-Do list site.
        self.assertIn('To-Do', self.browser.title)
        self.fail('...more steps need to be added to this test!')

        # The home page has a text box that invites her to enter a to-do item straight away.
        # She types "Buy peacock feathers". (She likes to make fly-fishing lures.)

        # She hits enter and the page updates.
        # Now the page lists "1: Buy peacock feathers"

        # There is still a text box inviting her to add another item.
        # She types "Use peacock feathers to make a fly"

        # She hits enter and the page updates again.
        # Now the page lists both of her items.

        # Wendy notices that the site has generated a unique URL for her list, with some explanatory text to that effect.
        # She visits that URL and sees that her list is still there.

        # She calls it a day.

if __name__ == '__main__':
    unittest.main()
        
