from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        # Look for 'liveserver' argument and, if found, use that as our test server url.
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        # If 'liveserver' argument is omitted, just use built-in test server url.
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about an online to-do list site. She goes to it's home page using her Web browser.
        self.browser.get(self.server_url)

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

        # When she hits enter she is taken to a new URL.
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        
        # Now the browser page lists "1: Buy peacock feathers"
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # She types "Use peacock feathers to make a fly"
        inputbox.send_keys('Use peacock feathers to make a fly')

        # She hits enter and the page updates again.
        inputbox.send_keys(Keys.ENTER)
        
        # Now the page lists both of her items.
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Francis, sits down at her browser. (We kill the existing browser session and start a new one).
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('peacock feathers', page_text)

        # Francis enters his first item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertNotEqual(francis_list_url, edith_list_url)

        # And his list has his item, but none of Edith's items.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('1: Buy milk', page_text)
        self.assertNotIn('peacock feathers', page_text)
        
    def test_layout_and_styling(self):

        # Edith goes to the home page
        self.browser.get(self.server_url)
        window_width = 1024
        window_height = 768
        self.browser.set_window_size(window_width, window_height)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] +( inputbox.size['width'] / 2 ),
            window_width / 2,
            delta = 15
        )

        # She starts a new list and sees that the input is centered there, too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + ( inputbox.size['width'] / 2 ),
            window_width / 2,
            delta = 15
        )
