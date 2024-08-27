from robocorp.tasks import task
from robocorp import workitems
from search_latimes import NewsSearcher
from scrapping_latimes import ScrapeNews
from save_data import SaveData
from challenge import AppController


@task
def run_process():
    
    app_controller = AppController()
    app_controller.initialize()
    logger = app_controller.logger

    for item in workitems.inputs:
        try:
            payload = app_controller.validator.validate_payload(item.payload)
            logger.info(f"Item payload: {payload}")

            search_news = NewsSearcher(app_controller, payload)
            scrape_news = ScrapeNews(app_controller, payload)
            save_data = SaveData(app_controller)

            search_news.perform_news_search()
            data = scrape_news.scrape_news()
            save_data.create_excel_file(data, payload["search_phrase"])

            item.done()
            logger.info(f"Scrape of phrase '{payload['search_phrase']}' finished.")

        except Exception as e:
            item.fail(message=f"Error: {e}")
            logger.error(f"Error scraping fresh news: {str(e)}")
            raise Exception(e)

    app_controller.end_process()
    logger.info("Finishing process: Scrape Fresh News...")
