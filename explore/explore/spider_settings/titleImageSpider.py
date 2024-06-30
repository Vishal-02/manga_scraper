IMAGES_STORE = "D:/Vishals Folder/Study/Code/Python/manga_project/images"

ITEM_PIPELINES = {
    "explore.pipelines.CustomPipeline": 1,
#    "explore.pipelines.ExplorePipeline": 300,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
#    "explore.middlewares.ExploreDownloaderMiddleware": 543,
}