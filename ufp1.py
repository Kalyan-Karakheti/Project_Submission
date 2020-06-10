# Import scrapy library
import scrapy
from scrapy.crawler import CrawlerProcess
import csv


# Spider class
class KKSpider(scrapy.Spider):
    name = "kkspider"

    def start_requests(self):

        urls = ["https://www.datacamp.com/courses/all"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_course_links)

    # parse_front method: to parse the front page
    def parse_front(self, response):

        course_blocks = response.css('div.course-block')

        course_links = course_blocks.xpath('./a/@href')

        # extract the links
        links_to_follow = course_links.extract()

        # follow the links to the next parser
        for link in links_to_follow:
            yield response.follow(url=link, callback=self.parse_pages)

    # to parse the pages
    def parse_pages(self, response):

        # direct to the course title text
        course_title = response.xpath('//h1[contains(@class, "title")]/text()')

        # extract and clean the course title text
        course_title_text = course_title.extract_first().strip()

        # direct to chapter titles text
        chapter_titles = response.css('h4.chapter__title::text')

        # extract and clean the chapter titles text
        chapter_titles_text = [t.strip() for t in chapter_titles.extract()]

        # store this in dictionary
        dict_kk[chapter_titles_text] = chapter_titles_text

    # to work on the website pages
    def parse_course_links(self, response):

        titles = response.css('h4.course-block__title::text').extract()
        authors = response.css('div.course-block__author > img::attr(alt)').extract()
        links = response.css('div.course-block > a::attr(href)').extract()

        #write links to csv
        get_file = 'datacamp_courses.csv'

        with open(get_file, 'w') as f:
            f.write(
                'Course Title' + '\t' + 'Course Author' + '\t' + 'Course Link' + '\n')
            for i in range(len(titles)):
                f.write("%s\t %s\t %s\n" % (titles[i], authors[i], links[i]))



# Initialize the dictionary
dict_kk = dict()


# Run the Spider
process = CrawlerProcess()
process.crawl(KKSpider)
process.start()

