import scrapy


class CrawlAudi(scrapy.Spider):
    

    name = "Audi"

    page_count = 0

    def start_requests(self):
        for i in range(self.page_count, 1000):
            yield scrapy.Request("https://www.cars.com/shopping/results/?page={}&page_size=20&list_price_max=&makes[]=volvo&maximum_distance=all&models[]=&stock_type=all&zip=".format(str(i)), callback=self.parse
                                 )

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
        'FILES_STORE': '/my/valid/path/',
    }

    def parse(self, response):
        for link in response.css("a.vehicle-card-visited-tracking-link::attr(href)"):
            product_link = 'https://www.cars.com'+link.get()
            yield response.follow(product_link, callback=self.parse_info)
            next_page = 'https://www.cars.com' + \
                response.css("a.sds-pagination__control::attr(href)").get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_info(self, response):
        product = response.css("section.sds-page-container")
        for product_link in product:
            yield dict(product_type=product_link.css("p.new-used::text").get(),
                       year=int(product_link.css(
                           "h1.listing-title::text").get().split(" ")[0]),
                       vehicle_made=product_link.css(
                           "h1.listing-title::text").get()[4:].strip(),
                       mileage=int(product_link.css(
                           "div.listing-mileage::text").get().translate({ord(s): None for s in [",", "m", "i", "."]})),
                       price=float(product_link.css(
                           "span.primary-price::text").get().translate({ord(s): None for s in ["$", ","]})),
                       drivetrain_type=product_link.css(
                           "dl.fancy-description-list dd::text")[2].get().strip(),
                       fueltype=product_link.css(
                           "dl.fancy-description-list dd::text")[5].get().strip(),
                       mpg=product_link.css(
                           "span.sds-tooltip span::text").get(),
                       transmission=product_link.css(
                           "dl.fancy-description-list dd::text")[6].get().strip(),
                       engine_type=product_link.css(
                           "dl.fancy-description-list dd::text")[7].get().strip(),
                       seller_info=product_link.css(
                           "div.dealer-address::text").get().strip(),
                       vehicle_features=product_link.css("ul.vehicle-features-list li::text").getall())

