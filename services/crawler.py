from apscheduler.schedulers.blocking import BlockingScheduler
from concurrent.futures import ThreadPoolExecutor
import requests


def crawler_run(url):
    r = requests.get(url)
    print(r)


class Crawler:
    def __init__(self, item_service, source_service):
        self.item_service = item_service
        self.source_service = source_service

    def crawler(self):
        urls = []
        sources = self.source_service.source_all()
        for source in sources:
            urls.append(source.url)
        executor = ThreadPoolExecutor(max_workers=2)
        executor.map(crawler_run, urls)
