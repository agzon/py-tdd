from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest

class NewVisitorTest(LiveServerTestCase):

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
    # Edith goes to check out homepage
    self.browser.get(self.live_server_url)

    # She notices the page title and header mention To-Do /list
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # Edith is invited to enter a to-do item straight away
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )

    # Edith types "Buy milk" into a text box
    inputbox.send_keys('Buy milk')

    # Edith hits enter, the page updates and now the page lists:
    # "1: Buy Milk" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')
    self.check_for_row_in_list_table('1: Buy milk')

    # There is still a text box inviting to add another item. Edith 
    # enters "Buy bread"
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy bread')
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items in the list
    self.check_for_row_in_list_table('1: Buy milk')
    self.check_for_row_in_list_table('2: Buy bread')

    # Now a new user, Francis, comes along to the site.

    ## We use a new browser session to make sure that no information
    ## of Edith's is coming through from cookies etc
    self.browser.quit()
    self.browser = webdriver.Firefox()

    # Francis visits the home page. There is no sign of Edith's list
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy milk', page_text)
    self.assertNotIn('Buy bread', page_text)

    # Francis starts a new list by entering a new item.
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Go to work')
    inputbox.send_keys(Keys.ENTER)

    # Francis gets his own unique URL
    francis_list_url = self.browser.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    # Again, there is no trace of Edith's list
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy milk', page_text)
    self.assertNotIn('Buy bread', page_text)

    # Satisfied, they both go back to sleep

