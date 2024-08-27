from RPA.HTTP import HTTP
from time import sleep
from teste import payload
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class NewsSearcher:
    def __init__(self, challenge, payload):
        self.output_path = challenge.output_path
        self.url = challenge.url
        self.sort_type = challenge.sort_type

        self.search_phrase = payload["search_phrase"].strip()
        self.topic = payload["topic"].strip()

        self.browser = challenge.browser
        self.locators = challenge.locators
        self.validator = challenge.validator
        self.logger = challenge.logger
        self.http = HTTP()

    def execute_search_phrase(self):
        """Click search button, input search text and click submit button"""
        self.logger.info(f"Search phrase: {self.search_phrase}")

        self.browser.click_button(self.locators.search_btn())
        self.browser.input_text(self.locators.input_search(), self.search_phrase)
        self.browser.click_button(self.locators.submit_search_btn())
        self.browser.wait_until_page_contains_element(
            self.locators.results(), error="Results page didn't load", timeout=20
        )

    def select_topic(self):
        """Click see all topics button and select a topic"""
        self.logger.info(f"Selecting topic: {self.topic}")
        try:
            self.browser.click_element(self.locators.see_all_topics())

            if self.browser.get_webelement(self.locators.topic(self.topic)):
                self.browser.select_checkbox(self.locators.topic(self.topic))
                self.logger.info("Topic selected")
        except:
            raise NoSuchElementException("Topic not found!")

    def apply_sorting(self):
        self.logger.info(f"Applying sorting by {self.sort_type}")
        self.browser.wait_until_element_is_enabled(self.locators.sort())
        self.browser.select_from_list_by_label(self.locators.sort(), self.sort_type)

    def execute_news_search(self):
        try:
            self.execute_search_phrase()
            self.select_topic()
            sleep(5)
            self.apply_sorting()
            sleep(5)

        except TimeoutException as e:
            self.logger.exception(f"Timeout occurred during news search: {e}")
            raise TimeoutException(e)

        except NoSuchElementException as e:
            self.logger.exception(f"Element not found during news search: {e}")
            raise NoSuchElementException(e)

        except Exception as e:
            self.logger.exception(f"Error during news search: {e}")
            raise Exception(e)


# from RPA.HTTP import HTTP
# from time import sleep
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# class NewsSearcher:
#     def __init__(self, challenge, item_payload):
#         self.output_path = challenge.output_path
#         self.url = challenge.url
#         self.sort_type = challenge.sort_type

#         self.search_phrase = item_payload["search_phrase"].strip()
#         self.topic = item_payload["topic"].strip()

#         self.browser = challenge.browser
#         self.locators = challenge.locators
#         self.validator = challenge.validator
#         self.logger = challenge.logger
#         self.http = HTTP()

#     def execute_search_phrase(self):
#         """Click search button, input search text and click submit button"""
#         self.logger.info(f"Search phrase: {self.search_phrase}")

#         self.browser.click_button(self.locators.search_btn())
#         self.browser.input_text(self.locators.input_search(), self.search_phrase)
#         self.browser.click_button(self.locators.submit_search_btn())
#         self.browser.wait_until_page_contains_element(
#             self.locators.results(), error="Results page didn't load", timeout=20
#         )

#     def select_topic(self):
#         """Click see all topics button and select a topic"""
#         self.logger.info(f"Selecting topic: {self.topic}")
#         try:
#             self.browser.click_element(self.locators.see_all_topics())

#             if self.browser.get_webelement(self.locators.topic(self.topic)):
#                 self.browser.select_checkbox(self.locators.topic(self.topic))
#                 self.logger.info("Topic selected")
#         except:
#             raise NoSuchElementException("Topic not found!")

#     def apply_sorting(self):
#         self.logger.info(f"Applying sorting by {self.sort_type}")
#         self.browser.wait_until_element_is_enabled(self.locators.sort())
#         self.browser.select_from_list_by_label(self.locators.sort(), self.sort_type)

#     def execute_news_search(self):
#         try:
#             self.execute_search_phrase()
#             self.select_topic()
#             sleep(5)
#             self.apply_sorting()
#             sleep(5)

#         except TimeoutException as e:
#             self.logger.exception(f"Timeout occurred during news search: {e}")
#             raise TimeoutException(e)

#         except NoSuchElementException as e:
#             self.logger.exception(f"Element not found during news search: {e}")
#             raise NoSuchElementException(e)

#         except Exception as e:
#             self.logger.exception(f"Error during news search: {e}")
#             raise Exception(e)
