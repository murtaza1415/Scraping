import scrapy

specialty_codes = [345,132,346,105,143,156,133,98,101,385,130,127,386,106,173,388,110,114,398,362,373,107,128,113,104,111,116,157,151,135,117,139,152,100,336,335,120,121,153,137,122,337,108,123,109,155,129,158,387,382,126,142]

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming',]

base_address = 'https://www.zocdoc.com/search?'

all_urls = []
for code in specialty_codes:
    url1 = base_address + 'dr_specialty=' + str(code)
    for state in states:
        url2 = url1 + '&address=' + state
        all_urls.append(url2)


        
class ProviderSpider(scrapy.Spider):
    name = "provider"
    
    global all_urls
    start_urls = all_urls
    

    def parse(self, response):
        pages = response.css('a.ocaw9w-0::attr(href)').getall()
        for page in pages:    
            next_page = response.urljoin(page)
            yield scrapy.Request(next_page, callback=self.parse_page)
            
    
    def parse_page(self, response):
        providers = response.css('a.htzklx-14::attr(href)').getall()
        
        for provider in providers:
            next_provider = response.urljoin(provider)
            print(next_provider)
            yield scrapy.Request(next_provider, callback=self.parse_provider)
        
        
    def parse_provider(self, response):
        name = response.css('h1.sc-1s83c7v-8 span::text').get()
        gender = response.css('section[data-test="Sex-section"] p::text').get()
        npi = response.css('section[data-test="NPI-section"] p::text').get()
        rating = response.css('div.sc-15uikgc-1::text').get()
        reviews = response.css('button.sc-15uikgc-4 span::text').get()
        location = response.css('h2.sc-1s83c7v-14::text').get()
        practice_name = response.css('div.sc-1anfxv2-2::text').get()
        address = response.css('div.sc-1anfxv2-1 div:nth-child(2)::text').get()
        about = response.css(':nth-child(21)::attr(content)').get()
        specialties = response.css('section[data-test="Specialties-section"] ul li::text').getall()
        if specialties == []:
            specialties = response.css('section[data-test="Specialties-section"] ul li span::text').getall()
        certifications = response.css('section[data-test="Certifications-section"] ul li::text').getall()
        if certifications == []:
            certifications = response.css('section[data-test="Certifications-section"] ul li span::text').getall()
        practices = response.css('section[data-test="Practice-section"] ul li a::text').getall()
        if practices == []:
            practices = response.css('section[data-test="Practice-section"] ul li span a::text').getall()
        hospitals = response.css('section[data-test="HospitalAffiliations-section"] ul li::text').getall()
        if hospitals == []:
            hospitals = response.css('section[data-test="HospitalAffiliations-section"] ul li span::text').getall()
        memberships = response.css('section[data-test="Memberships-section"] ul li::text').getall()
        if memberships == []:
            memberships = response.css('section[data-test="Memberships-section"] ul li span::text').getall()
        trainings = response.css('section[data-test="Education-section"] ul li::text').getall()
        if trainings == []:
            trainings = response.css('section[data-test="Education-section"] ul li span::text').getall()
        languages = response.css('section[data-test="Languages-section"] ul li::text').getall()
        if languages == []:
            languages = response.css('section[data-test="Languages-section"] ul li span::text').getall()
        
    
        
        with open('providers.txt', 'a') as f:
            f.write('\n\n\n\n\n\n\n\n\n\n')
            f.write('*****************************************************************************************')
            
            f.write('\nName: ')
            if name != None:
                name = name.encode('utf-8')
                name = name.replace('\r','')
                name = name.replace('\n','')
                f.write(name)
            
            f.write('\nGender: ')
            if gender != None:
                gender = gender.encode('utf-8')
                gender = gender.replace('\r','')
                gender = gender.replace('\n','')
                f.write(gender)
            
            f.write('\nNPI: ')
            if npi != None:
                npi = npi.encode('utf-8')
                npi = npi.replace('\r','')
                npi = npi.replace('\n','')
                f.write(npi)
            
            f.write('\nRating: ')
            if rating != None:
                rating = rating.encode('utf-8')
                rating = rating.replace('\r','')
                rating = rating.replace('\n','')
                f.write(rating)
            
            f.write('\nNo. reviews: ')
            if reviews != None:
                reviews = reviews.encode('utf-8')
                reviews = reviews.replace('\r','')
                reviews = reviews.replace('\n','')
                f.write(reviews)
                
            f.write('\nLocation: ')
            if location != None:
                location = location.encode('utf-8')
                location = location.replace('\r','')
                location = location.replace('\n','')
                f.write(location)
                
            f.write('\nPractice Name: ')
            if practice_name != None:
                practice_name = practice_name.encode('utf-8')
                practice_name = practice_name.replace('\r','')
                practice_name = practice_name.replace('\n','')
                f.write(practice_name)
            
            f.write('\nAddress: ')
            if address != None:
                address = address.encode('utf-8')
                address = address.replace('\r','')
                address = address.replace('\n','')
                f.write(address)
                
            f.write('\nSpecialties: ' )
            if specialties != None:                
                for j,specialty in enumerate(specialties,1):
                    specialty = specialty.encode('utf-8')
                    specialty = specialty.replace('\r','')
                    specialty = specialty.replace('\n','')
                    f.write(specialty)
                    if j < len(specialties):
                        f.write(', ')
                        
            f.write('\nBoard Certifications: ' )            
            if certifications != None:    
                for j,certification in enumerate(certifications,1):
                    certification = certification.encode('utf-8')
                    certification = certification.replace('\r','')
                    certification = certification.replace('\n','')
                    f.write(certification)
                    if j < len(certifications):
                        f.write(', ')
                        
            f.write('\nOther Practice Names: ' )
            if practices != None:    
                for j,practice in enumerate(practices,1):
                    practice = practice.encode('utf-8')
                    practice = practice.replace('\r','')
                    practice = practice.replace('\n','')
                    f.write(practice)
                    if j < len(practices):
                        f.write(', ')
            
            f.write('\nHospital Affiliations: ' )
            if hospitals != None:    
                for j,hospital in enumerate(hospitals,1):
                    hospital = hospital.encode('utf-8')
                    hospital = hospital.replace('\r','')
                    hospital = hospital.replace('\n','')
                    f.write(hospital)
                    if j < len(hospitals):
                        f.write(', ')
            
            f.write('\nMemberships: ' )
            if memberships != None:      
                for j,membership in enumerate(memberships,1):
                    membership = membership.encode('utf-8')
                    membership = membership.replace('\r','')
                    membership = membership.replace('\n','')
                    f.write(membership)
                    if j < len(memberships):
                        f.write(', ')
            
            f.write('\nEducation and Trainings: ' )
            if trainings != None:
                for j,training in enumerate(trainings,1):
                    training = training.encode('utf-8')
                    training = training.replace('\r','')
                    training = training.replace('\n','')
                    f.write(training)
                    if j < len(trainings):
                        f.write(', ')
            
            f.write('\nLanguages Spoken: ' )
            if languages != None:    
                for j,language in enumerate(languages,1):
                    language = language.encode('utf-8')
                    language = language.replace('\r','')
                    language = language.replace('\n','')
                    f.write(language)
                    if j < len(languages):
                        f.write(', ')
            
            f.write('\nAbout: ' )
            if about != None:
                about = about.encode('utf-8')
                about = about.replace('\r','')
                about = about.replace('\n','')
                f.write(about)            
            f.write('\n*****************************************************************************************\n')
            
        