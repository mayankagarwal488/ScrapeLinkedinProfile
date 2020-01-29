from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from bs4 import BeautifulSoup as bs
import os
import csv


driver = webdriver.Chrome('[location of the chromdriver]')
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

# Mention your Username and Password

linkedin_username = "abc@abc.com"
linkedin_password = "**********"

# Will enter the given Username and Password in the designated fields

username = driver.find_element_by_id('username')
username.send_keys(linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('password')
password.send_keys(linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
sign_in_button.click()
sleep(2)

# Will pick up the Link of every LinkedIn profile and open their profiles (row wise operation)

with open('Test.csv', newline='') as myfile:
    reader = csv.reader(myfile)
    
    for row in reader:
            rowarray = ', '.join(row)
            ALLLink = rowarray.split(", ")
            try:

                driver.get(ALLLink[1])
                sleep(5)
                driver.page_source
                sel = Selector(text=driver.page_source)

                # The name of the profile holder
    
                name = sel.xpath('//*[@id="ember46"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
                if name:
                    name = name.strip()

                # The job Title of the profile holder

                job_title = sel.xpath('//*[@id="ember46"]/div[2]/div[2]/div[1]/h2/text()').extract_first()
                if job_title:
                    job_title = job_title.strip()

                # Prepare the array with the extracted details
    
                d = [name, job_title, ALLLink[1]]

                # Extracts upto four experiences
                
                try: 
                    for a in range(1,4):
                        print ("Experience "+str(a))
                        b = ('//*[@id="experience-section"]/ul/li[' + str(a) + ']')
                        experience = sel.xpath(b).getall()


                        for x in range(len(experience)):
                            html = experience[x]
                            soup = bs(html)
                            for script in soup(["script", "style"]):
                                script.extract()
                            text = soup.get_text()
                            lines = (line.strip() for line in text.splitlines())
                            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                            text = '\n'.join(chunk for chunk in chunks if chunk)
                            e = text.splitlines()
                            d = d + e
                       # print (d)
                        d.pop(4)
                        d.pop(5)
                        d.pop(6)
                        d.pop(6)

                        #print (d)
                        with open('List.csv', 'a') as checkfile:
                                    writer = csv.writer(checkfile)
                                    writer.writerow(d)
                                    checkfile.close()
                        d = [name, job_title, ALLLink[1]]
                except:
                     pass
            except:
                    z = [ALLLink[0],ALLLink[1]]
                    with open('Link Down.csv', 'a') as checkfile:
                                    writer = csv.writer(checkfile)
                                    writer.writerow(z)
                                    checkfile.close()
                # print ("Link down of " + ALLLink[0] + " "+ ALLLink [1])
    
driver.quit()
