import scrapy


class ToolSpider(scrapy.Spider):
    name = 'tool'
    page_number = 36
    # allowed_domains = ['a']
    # start_urls = ['https://www.houzz.com/']
    base_url = 'https://www.houzz.com/'
    # start_urls = ['https://www.houzz.com/products/outdoor-products']
    # start_urls = ['https://www.houzz.com/products/bath-products']
    # start_urls = ['https://www.houzz.com/products/home-improvement']
    # start_urls = ['https://www.houzz.com/products/home-decor']
    # start_urls = ['https://www.houzz.com/products/lighting']
    # start_urls = ['https://www.houzz.com/products/kitchen-and-dining']
    # start_urls = ['https://www.houzz.com/products/furniture']
    start_urls = ['https://www.houzz.com/products/living-products']



    def parse(self, response):
        links = response.css('.department-card.spf-link')
        for link in links:
            flink = link.css('a::attr(href)').get()
            # print(flink)
            yield scrapy.Request(url=flink, callback=self.parse1)

    def parse1(self, response):
        links = response.css('.category-card__wrapper')
        for link in links:
            flink = link.css('a::attr(href)').get()  
            # print(flink)  
            yield scrapy.Request(url=flink, callback=self.parse2)

    def parse2(self, response):
        links =   response.css('.hz-product-card__link')
        for link in links:
            flink = link.css('::attr(href)').get()
            # print(flink)  
            yield scrapy.Request(url=flink, callback=self.parse3)

        next_page  = 'https://www.houzz.com/products/outdoor-lounge-sets/p/'+ str(ToolSpider.page_number)  
        if ToolSpider.page_number <= 2000:
            ToolSpider.page_number += 36
            if next_page is not None:
                yield scrapy.Request(url=next_page, callback=self.parse2)         

    def parse3(self, response):
        Product_name = response.css('.hz-view-product-title span::text').get()
        Price = response.css('.pricing-info__price::text').get()
        Full_descriptions = response.css('.vp-redesign-description').get()
        Short_descriptions = response.css('.vp-redesign-description::text').get()  
        Images = response.css('.alt-images__thumb img::attr(src)').getall()
        image_all = []
        for image in Images:
            split_image = image.split(',')
            if len(split_image):
                for img in split_image:
                    image_all.append(img.replace('65','700'))  

        yield {
            'Product_name': Product_name,
            'Price': Price,
            'Full_descriptions': Full_descriptions,
            'Short_descriptions': Short_descriptions,
            'Images': image_all,
        }
