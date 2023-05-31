from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import whatsapp_auto.exception as exception
import undetected_chromedriver as uc
from urllib.parse import quote
from re import fullmatch
import time,os


class Login():
    def __init__(self):
        options = uc.ChromeOptions()
        if os.name == 'nt':
            path = os.getcwd()+'\whatsapp_session'
        else:
            path = os.getcwd()+'/whatsapp_session'
        options.add_argument('--user-data-dir=' + path)
        options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
        
        driver = uc.Chrome(options=options,use_subprocess=True)
        wait_60 = WebDriverWait(driver, 60)
        driver.get('https://web.whatsapp.com/')
        try:
            # verifying login
            wait_60.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[4]/div/div/div[2]/div[1]/h1'))).text
            print('login sucessfully')
            self.driver = driver
            self.wait_10 = WebDriverWait(self.driver, 10)
        except:
            driver.close()
            driver.quit()
            raise exception.Login_Failed("Whatsapp Login Failed")
        
        
    def send_message(self,phone_no,message):
        """Send a message to the phone number
        
        :param str phone_no : Receiver's phone number
        :param str message : The message you want to send
        
        """
        self.verify_number(phone_no)
        self.driver.get('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + quote(message))
        time.sleep(1)
        try:
            # send button (click)
            self.wait_10.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'))).click()
        except:
            raise exception.Invalid_Phone_Number("The Phone Number Doesn't Have Whatsapp")
        
        
    def verify_number(self,phone_no):
        if not "+" in phone_no or "_" in phone_no:
            raise exception.Country_Code_Exception("Country Code Missing in Phone Number!")
        
        number = phone_no.replace(" ", "")
        if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", number):
            raise exception.Invalid_Phone_Number("Invalid Phone Number.")
        return True
    
    
    def file(self,path,caption):
        # attach button (click)
        self.wait_10.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'))).click()
        
        # attach files path
        self.wait_10.until(EC.presence_of_element_located((By.XPATH,
                                                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'))).send_keys(path)
        if caption is not None:
            # typing caption
            self.wait_10.until(EC.presence_of_element_located((By.XPATH,"//div//p[contains(@class,'selectable-text copyable-text')]"))).send_keys(caption)
        time.sleep(1)
        
        # send button (click)
        self.wait_10.until(EC.presence_of_element_located((By.XPATH,
                                                        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'))).click()

    
    def send_file(self,phone_no,path,caption=None):
        """Send a File to a WhatsApp number 
        
        :param str phone_no : Receiver's phone number
        :param str path : file path
        :param str caption : Caption for the file
        
        """
        if os.path.isfile(path):
            self.verify_number(phone_no)
            self.driver.get('https://web.whatsapp.com/send?phone=' + phone_no)
            self.file(path,caption)
        else:
            raise FileNotFoundError(f"Invalid File Path : {path}")
        

    def send_multiple_files(self,phone_no,folder_path,caption=None):
        """Send multiple files to a WhatsApp number 
        
        :param str phone_no : Receiver's phone number
        :param str folder_path : Folder path
        :param str caption : Caption for the file
        
        """
        if os.path.isdir(folder_path):
            self.verify_number(phone_no)
            path = ''
            for i in os.listdir(folder_path):
                if os.name == 'nt':
                    path+=f'{folder_path}\{i}\n'
                else:
                    path+=f'{folder_path}/{i}\n'
            final_path = path[:-1]
            # wait = WebDriverWait(self.driver, 10)
            self.driver.get('https://web.whatsapp.com/send?phone=' + phone_no)
            self.file(final_path,caption)
        else:
            raise FileNotFoundError(f"Invalid Folder Path : {folder_path}")
        
        
    def send_message_to_group(self,group_link,message):
        """Send a message to the group
        
        :param str group_link : whatsapp group link 
        :param str message : The message you want to send
        
        """
        if 'https' in group_link:
            group_link = group_link.split('https://chat.whatsapp.com/')[1]
        
        self.driver.get('https://web.whatsapp.com/accept?code=' + group_link)
        try:
            message_xpath = self.wait_10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')))
            for message in message.split('\n'):
                message_xpath.send_keys(message)
                message_xpath.send_keys(Keys.SHIFT + Keys.ENTER)
                
            # send button (click)
            self.wait_10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'))).click()
        except:
            exception.Invalid_Group_Link("Group link given is Invalid")


    def send_file_to_group(self,group_link,path,caption=None):
        """Send a message to the group
        
        :param str group_link : whatsapp group link 
        :param str path : file path
        :param str caption : Caption for the file    
            
        """
        
        if os.path.isfile(path):
            if 'https' in group_link:
                group_link = group_link.split('https://chat.whatsapp.com/')[1]
            self.driver.get('https://web.whatsapp.com/accept?code=' + group_link)
            self.file(path,caption)
        else:
            raise FileNotFoundError(f"Invalid File Path : {path}")
        

    def send_multiple_files_to_group(self,group_link,folder_path,caption=None):
        """Send multiple files to a WhatsApp group 
        
        :param str group_link : whatsapp group link 
        :param str folder_path : Folder path
        :param str caption : Caption for the file
        
        """
        if os.path.isdir(folder_path):
            path = ''
            for i in os.listdir(folder_path):
                if os.name == 'nt':
                    path+=f'{folder_path}\{i}\n'
                else:
                    path+=f'{folder_path}/{i}\n'
            final_path = path[:-1]
            if 'https' in group_link:
                group_link = group_link.split('https://chat.whatsapp.com/')[1]
            self.driver.get('https://web.whatsapp.com/accept?code=' + group_link)
            self.file(final_path,caption)
        else:
            raise FileNotFoundError(f"Invalid Folder Path : {folder_path}")
        
        
    def close(self):
        self.driver.close()
        self.driver.quit()