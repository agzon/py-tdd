from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

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
    # user goes to check out homepage
    self.browser.get('http://localhost:8000')

    # She notices the page title and header mention To-Do /list
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # User is invited to enter a to-do item straight away
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )

    # User types "Buy milk" into a text box
    inputbox.send_keys('Buy milk')

    # User hits enter, the page updates and now the page lists:
    # "1: Buy Milk" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('1: Buy milk')

    # There is still a text box inviting to add another item. The user 
    # enters "Buy bread"
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy bread')
    inputbox.send_keys(Keys.ENTER)

    self.check_for_row_in_list_table('1: Buy milk')
    self.check_for_row_in_list_table('2: Buy bread')

    self.fail('Finish the test')

    # The page updates again, and now shows both items in the list

    # The user wondes whether the site will remember her to-do list.
    # Then she sees the the site has generated a unique URL for her

    # The user visits that URL - her to-do list is still there.

    # Satisfied, the user leaves the web page

if __name__ == '__main__':
  unittest.main(warnings='ignore')
