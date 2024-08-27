from robocorp.tasks import task
# from robocorp import workitems
from search_latimes import NewsSearcher
from scrapping_latimes import ScrapeNews
from save_data import SaveData
from src.challenge import AppController


@task
def run_process():
    
    app_controller = AppController()
    app_controller.initialize()
    logger = app_controller.logger


    payload = {
        "search_phrase": "business",
        "topic": "California",
        "n_months": 0,
        "max_news": 999
    }

    # for item in workitems.inputs:
    # for item in payload:
    try:
        search_news = NewsSearcher(app_controller, payload)
        scrape_news_instance = ScrapeNews(app_controller, payload)
        save_data = SaveData(app_controller)

        search_news.execute_news_search()
        data = scrape_news_instance.scrape_news()
        save_data.create_excel_file(data, payload["search_phrase"])

        # item.done()
        logger.info(f"Scrape of phrase '{payload['search_phrase']}' finished.")

    except Exception as e:
        # item.fail(message=f"Error: {e}")
        logger.error(f"Error scraping fresh news: {str(e)}")
        raise Exception(e)

    app_controller.end_process()
    logger.info("Finishing process: Scrape Fresh News...")
