import scrapy
import re

base_address = 'https://www.merriam-webster.com/browse/dictionary/'
#alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0']
alphabets = ['a', 'b', 'c']


class DictSpider(scrapy.Spider):
    name = 'dictionary'
    
    start_urls = [(base_address + char) for char in alphabets]
    
    def parse(self, response):
        no_pages = int( response.css('span.counters::text').get().split('page 1 of ')[1] )
        pages = [ (response.url + '/' + str(x)) for x in range(1,no_pages+1) ]
        for page in pages:
            yield scrapy.Request(page, callback=self.parse_page)
        
        
    def parse_page(self, response):
        word_links = response.css('.entries a::attr(href)').getall()
        word_links = [response.urljoin(word) for word in word_links]
        
        for link in word_links:
            yield scrapy.Request(link, callback=self.parse_word)
        
    def parse_word(self, response):
        no_entries = len(response.xpath("//*[contains(@id, 'dictionary-entry')]"))
        
        for entry in range(no_entries):
            word = response.css('.entry-header .hword').getall()[entry]
            word = re.sub('[\<].*?[\>]', '', word)
            
            category = response.css('.entry-header .fl').getall()
            #Some instances of words have no categories e.g. eyess. 
            #In such cases, there isn't a 1-to-1 correspondence between 'entry' and 'category' list. 
            #So we skip adding any category at all.
            if len(category) == no_entries:
                category = category[entry]
                category = re.sub('[\<].*?[\>]', '', category)
            else:
                category = ''
            
            definitions = []
            
            dt = response.css('#dictionary-entry-{} .dtText ::text'.format(entry+1)).getall()
            dt = ''.join(dt)
            dt = dt.split(':')
            for i in range(len(dt)):
                dt[i] = dt[i].split('\n')[0]
                dt[i] = dt[i].strip('                                      ')
            while("" in dt) : 
                dt.remove("")
            
            definitions = dt
            
            #Sometimes word or any definitons might not be detected by script.
            if word != '' and definitions != []:
                with open('dictionary.txt', 'a') as f:
                    f.write('\n' + word + '\n')
                    #f.write('Type: ' + category  + '\n')
                    f.write('Definitions: \n')
                    for i in range(len(definitions)):
                        f.write('{}) {}\n'.format(i+1, definitions[i]))
                    #Print a finishing line if word is last in page.
                    if entry == (no_entries-1):
                        f.write('---------------------------------------------------------------------------\n')

                yield {
                    'word': word,
                    #'type': category,
                    'definitions': definitions,
                }
        
        
        
        