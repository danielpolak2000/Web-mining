import scrapy


class ArltSpider(scrapy.Spider):
    name = 'arlt'
    start_urls = ['https://www.arlt.com/PC/']

    def parse(self, response):
        for products in response.css('li.productLine'):
            yield {
                'name': products.css('a.productTitle::text').get(),
                'price': products.css('span.lead.price::text').get().replace('\n', '').replace(' ', ''),
                'link': products.css('a.productTitle::attr(href)').get(),
            }

        next_page = response.css('a.page-link')[-1].attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
