from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    # user goes to check out homepage
    self.browser.get('http://localhost:8000')

    # She notices the page title and header mention To-Do /list
    self.assertIn('To-Do', self.browser.title)
    self.fail('Finish the test')

    # User is invited to enter a to-do item straight away

    # User types "Buy Milk" into a text box

    # User hits enter, the page updates and now the page lists:
    # "1: Buy Milk" as an item in a to-do list

    # There is still a text box inviting to add another item. The user 
    # enters "Buy bread"

    # The page updates again, and now shows both items in the list

    # The user wondes whether the site will remember her to-do list.
    # Then she sees the the site has generated a unique URL for her

    # The user visits that URL - her to-do list is still there.

    # Satisfied, the user leaves the web page

if __name__ == '__main__':
  unittest.main(warnings='ignore')
