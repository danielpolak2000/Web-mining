import scrapy


class CoffeeSpider(scrapy.Spider):
    name = 'coffee'
    start_urls = [
        'https://www.amazon.de/s?k=kaffeewaage&crid=30SBKMXBY7589&sprefix=kaffeewa%2Caps%2C123&ref=nb_sb_ss_ts-doa-p_1_8']

    def parse(self, response):
        for products in response.css('div.s-result-item'):
            if products.css('span.a-size-base-plus::text').get() is not None:

                link = products.css('a.a-link-normal').attrib['href']
                yield {
                    'name': products.css('span.a-size-base-plus::text').get(),
                    'price': products.css('span.a-offscreen::text').get(),
                    'link': 'https://www.amazon.de' + link
                }

        # [-1] wegen liste von a tags.
        next_page = response.css(
            'span.s-pagination-strip').css('a')[-1].attrib['href']
        if next_page is not None:
            yield response.follow('amazon.de' + next_page, callback=self.parse)
