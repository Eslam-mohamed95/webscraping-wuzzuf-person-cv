from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Database import Database as db


class Scraper:

    def __init__(self):

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
        self.visited_links = [] # list of visited url
        self.personal_url=[]  # list for saved member url for 1 : end 
        self.href_links = [] # list of url try in loop
        self.data_user = []  # list for infromation member url 
        self.db = db() # run database.py 


    def crawl(self, link):

    
        if link in self.visited_links :
            return
        
        self.driver.get(link)
        self.visited_links.append(link)
        print(f"[INFO] Crawling: {link}")
        
        links = self.driver.find_elements(By.TAG_NAME, "a")
        
    #parent url 
        for url in links:
            href = url.get_attribute("href")
        
            if "members/" in href : 

                if "?p=" in href and href not in self.personal_url:
                    self.personal_url.append(href)
                    self.visited_links.append(href)
                    print(f"done saved {href}")
                # filter scraping from a to z pages for member
                elif href not in self.href_links :
                    self.href_links.append(href)

            elif href and "wuzzuf.net/me/" in href:

                # add url for CV person to list 
                if href not in self.data_user:
                    self.data_user.append(href)        
                    print(f"url member of infromation saved   {href}")

    # children url
        for child_url in self.href_links:

            if child_url not in self.visited_links:

        # make recurion for childen url
                self.crawl(child_url)
        self.data_save(self.data_user)

    
    #function for screenshot and get infromation about person to save it in database
    def data_save (self, list):
        try:
            # make height of tab before screenshot
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.set_window_size(800, page_height)
            
            #scraping values
            for href in list:

                self.driver.get(href)
                name = self.driver.find_element(By.TAG_NAME, "h1").text
                job = self.driver.find_element(By.TAG_NAME,"h2").text
                
                if job == "at , Egypt" :
                    job = "Not Have Job Yet"
  
                skills = self.driver.find_element(by=By.CLASS_NAME, value="css-1fw72n4").find_elements(by=By.TAG_NAME, value="li")
                all_skill = ", ".join([skill.text for skill in skills])
                languages = self.driver.find_elements(by=By.CLASS_NAME, value="css-oz54ti")
                all_languages = "، ".join([language.text for language in languages])
                location = self.driver.find_element(by=By.CLASS_NAME, value="css-1shh2qx").text

                # save infromation in database
                self.db.insert(name, location, all_skill, all_languages, job)
                
            
                # for picture (save picture with name of person)
                name_url = href.split('/me/')[-1]
                self.driver.save_screenshot(f"/home/kali/Desktop/scrapper/data_user/{name_url}.png")
                print(f"picture profile save    {name_url}")

        except Exception as e:
            print(e)

    # after finish scraping close browser
    def exit(self):
        self.driver.quit()


if __name__ == '__main__':
    start_link = "https://wuzzuf.net"
    crawling = Scraper()
    crawling.crawl(start_link)
    crawling.exit()
    
