import scrapy

def create_file():
    with open('therapists.csv', 'w') as f: 
        f.write('"URL","Name","Titles","Phone","State","Address","Specialties","Cost per Session","Years in Practice","License","School","Year Graduated","Certificates","Insurances"\n')
    return
    
create_file()        
        
    
    
class TherapistSpider(scrapy.Spider):
    name = 'therapistSpider'
    
    def start_requests(self):
        main_url = 'https://www.psychologytoday.com/us/therapists'
        yield scrapy.Request(main_url, callback=self.parse_main)
    
    def parse_main(self, response):
        state_urls = response.css('div.us_region_list ::attr(href)').getall()
        for state_url in state_urls:
            yield scrapy.Request(state_url, callback=self.parse_state)
    
    def parse_state(self, response):
        state = response.url.split('/')[-1]
        print('\n' + state + '\n')
        yield scrapy.Request(response.url, dont_filter = True, callback=self.parse_page, meta={'state': state})
    
    def parse_page(self, response):
        state = response.meta['state']
        page_count = response.url.split('=')[-1]
        print('\n' + state + ' -' + page_count + '\n')

        therapist_urls = response.css('a.result-name::attr(href)').getall()
        for therapist_url in therapist_urls:
            yield scrapy.Request(therapist_url, callback=self.parse_therapist)

        with open('pages_scraped.txt', 'a') as f:
            f.write(response.url + '\n')
        
        next_page = response.css('a.btn-next::attr(href)').get()
        if next_page != None:
            yield scrapy.Request(next_page, callback=self.parse_page, meta={'state': state})
        
    def parse_therapist(self, response):
        
        therapist_url = self.scrape_url(response)
        therapist_state = self.scrape_state(response)
        therapist_name = self.scrape_name(response)
        therapist_titles = self.scrape_titles(response)
        therapist_phone = self.scrape_phone(response)
        therapist_address = self.scrape_address(response)
        therapist_specialties = self.scrape_specialties(response)
        cost_per_session = self.scrape_cost(response)
        insurances = self.scrape_insurances(response)
        years_in_practice, license, school, year_graduated = self.scrape_qualifications(response)
        certificates = self.scrape_certificates(response)
        
        therapist_titles = ', '.join([elem for elem in therapist_titles])
        therapist_specialties = ', '.join(elem for elem in therapist_specialties)
        insurances = ', '.join(elem for elem in insurances)
        certificates = ', '.join(elem for elem in certificates)
        
        print('\n')
        print('name: ' + therapist_name)        
        print('titles: ' + therapist_titles)
        print('phone: ' + therapist_phone)
        print('address: ' + therapist_address)
        print('specialties: ' + therapist_specialties)
        print('cost per session: ' + cost_per_session)
        print('insurances: ' + insurances)
        print('years in practice: ' + years_in_practice)
        print('license: ' + license)
        print('school: ' + school)
        print('year graduated: ' + year_graduated)
        print('certificates: ' + certificates)
        print('\n')
    
        with open('therapists.csv', 'a') as f:
            f.write('"' + therapist_url.replace('"','') + '",')
            f.write('"' + therapist_name.replace('"','') + '",')
            f.write('"' + therapist_titles.replace('"','') + '",')
            f.write('"' + therapist_phone.replace('"','') + '",')
            f.write('"' + therapist_state.replace('"','') + '",')
            f.write('"' + therapist_address.replace('"','') + '",')
            f.write('"' + therapist_specialties.replace('"','') + '",')
            f.write('"' + cost_per_session.replace('"','') + '",')
            f.write('"' + years_in_practice.replace('"','') + '",')
            f.write('"' + license.replace('"','') + '",')
            f.write('"' + school.replace('"','') + '",')
            f.write('"' + year_graduated.replace('"','') + '",')
            f.write('"' + certificates.replace('"','') + '",')
            f.write('"' + insurances.replace('"','') + '"')
            f.write('\n')
        
        return    
    
    def scrape_url(self, response):
        url = response.url.split('?')[0]
        return url
    
    def scrape_state(self, response):
        state = response.url.split('/')[-2].replace('-', ' ').title()
        return state
        
    def scrape_name(self, response):
        name = ''
        try:
            name = response.xpath('//h1[@itemprop="name"]/text()').get().strip()
        except:
            return name
        return name
    
    def scrape_phone(self, response):
        phone = ''
        try:
            phone = response.css('div.profile-phone a.phone-click-reveal::text').get().strip()
        except:
            return phone
        return phone
    
    def scrape_cost(self, response):
        cost_per_session = ''
        try:
            potential_cost = response.css('div.finances-office ul li')[0].css('::text').getall()
        except:
            return cost_per_session
        potential_cost = ' '.join(elem for elem in potential_cost)
        if 'Cost per Session:' in potential_cost:
            cost_per_session = potential_cost.replace('Cost per Session:', '').strip()
        return cost_per_session
    
    def scrape_qualifications(self, response):
        years_in_practice = ''
        license = ''
        school = ''
        year_graduated = ''
        selector_list = response.css('div.profile-qualifications li')
        for selector in selector_list:
            qualification = selector.css('::text').getall()
            qualification = ' '.join(elem.strip() for elem in qualification)
            if 'Years in Practice:' in qualification:
                years_in_practice = qualification.replace('Years in Practice:', '').strip()
            if 'License:' in qualification and 'Supervisor License:' not in qualification:
                license = qualification.replace('License:', '').replace('\n', '').replace('                                                ', '').strip()
            if 'School:' in qualification:
                school = qualification.replace('School:', '').strip()
            if 'Year Graduated:' in qualification:
                year_graduated = qualification.replace('Year Graduated:', '').strip()
        return years_in_practice, license, school, year_graduated
    
    def scrape_certificates(self, response):
        certificates = []
        selector_list = response.css('div.profile-additional-credentials li')
        for selector in selector_list:
            potential_certificate = selector.css('::text').getall()
            potential_certificate = ' '.join(elem for elem in potential_certificate)
            if 'Certificate:' in potential_certificate:
                certificate = potential_certificate.replace('Certificate:', '').strip()
                certificates.append(certificate)
        return certificates
        
    def scrape_titles(self, response):
        titles = []
        scraped_list = response.css('div.name-title-column div.profile-title ::text').getall()
        for elem in scraped_list:
            elem = elem.strip(' ,\n')
            if elem != '':
                title = elem
                titles.append(title)
        return titles        
            
    def scrape_address(self, response):
        address_items = []
        address = ''
        try:
            scraped_list = response.css('div.profile-address')[1].css('div.location-address-phone')[0].css('::text').getall()
        except:
            return address
        for elem in scraped_list:
            elem = elem.strip(' ,\n')
            if elem != '':
                address_items.append(elem)
        address = ', '.join(address_items)
        return address
    
    def scrape_specialties(self, response):
        specialties = []
        scraped_list = response.css('ul.specialties-list li::text').getall()
        for potential_specialty in scraped_list:
            potential_specialty = potential_specialty.strip()
            if potential_specialty != '':
                specialty = potential_specialty
                specialties.append(specialty)
        return specialties
    
    def scrape_insurances(self, response):
        insurances = []
        try:
            scraped_list = response.css('div.attributes-insurance')[0].css('li::text').getall()
        except:
            return insurances
        for potential_insurance in scraped_list:
            potential_insurance = potential_insurance.strip()
            if potential_insurance != '':
                insurance = potential_insurance
                insurances.append(insurance)
        return insurances
