from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import pandas

import datetime

class shop:
    options = webdriver.EdgeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    def __init__(self, offline: bool = False) -> None:
        self.__RAWdata = None
        self.RAWdata = None
        self.__parsed = None
        if offline == False:
            def checkKey(dictionary: dict, key: str) -> None:
                if not dictionary.get(key, None):
                    raise KeyError("Proper Data Doesnt Exist")
                
            def parser(data: dict) -> list:
                
                data = json.loads(data)
                
                checkKey(data, "catalog")
                checkKey(data["catalog"], "categories")
                
                data = data["catalog"]["categories"]
                itemShop = []
                
                for category in data:
                    for section in category["sections"]:
                        for offer in section["offerGroups"]:
                            for item in offer["items"]:
                                
                                inDate = item.get("inDate", None)
                                outDate = item.get("outDate", None)
                                
                                item_dict = {
                                    "name" : item.get("title", None).replace("&amp;", "&"),
                                    "category" : category["navLabel"].replace("&amp;", "&"),
                                    "section" : section["displayName"].replace("&amp;", "&"),
                                    "assetType" : item["assetType"].replace("dynamicbundle", "dynamic bundle").replace("jamtrack", "jam track").replace("rmtpack", "real money pack").replace("staticbundle", "static bundle"),
                                    "price" : (str(item["pricing"]["finalPrice"]) + " V-Bucks") if item["assetType"] != "rmtpack" else "$" + "".join([x for x in str(item["pricing"]["finalPrice"])[:len(str(item["pricing"]["finalPrice"]))-2]]) + "." + str(item["pricing"]["finalPrice"])[-2:],
                                    "inDate" : inDate if inDate == None else inDate.split("T")[0] if "T" in inDate else inDate,
                                    "outDate" : outDate if outDate == None else outDate.split("T")[0] if "T" in outDate else outDate,
                                    "hasVariants" : item.get("hasVariants", None)
                                }

                                itemShop.append(item_dict)
                                del item_dict
                return itemShop
            
            driver = webdriver.Edge(self.options)
            driver.get("https://www.fortnite.com/item-shop?lang=en-US&_data=routes%2Fitem-shop._index")
            driver.minimize_window()
            
            self.__RAWdata = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[hidden="true"]'))).get_attribute("innerHTML")
            self.__parsed = parser(self.__RAWdata)
        
    @property
    def RAW(self) -> str:
        if self.__RAWdata == None:
            return self.RAWdata            
        return self.__RAWdata
    
    @property
    def parsed(self) -> dict:
        def checkKey(dictionary: dict, key: str) -> None:
                if not dictionary.get(key, None):
                    raise KeyError("Proper Data Doesnt Exist")
              
        def parser(data: str) -> list:
                
                data = json.loads(data)
                
                checkKey(data, "catalog")
                checkKey(data["catalog"], "categories")
                
                data = data["catalog"]["categories"]
                itemShop = []
                
                for category in data:
                    for section in category["sections"]:
                        for offer in section["offerGroups"]:
                            for item in offer["items"]:
                                
                                inDate = item.get("inDate", None)
                                outDate = item.get("outDate", None)
                                
                                item_dict = {
                                    "name" : item.get("title", None).replace("&amp;", "&"),
                                    "category" : category["navLabel"].replace("&amp;", "&"),
                                    "section" : section["displayName"].replace("&amp;", "&"),
                                    "assetType" : item["assetType"].replace("dynamicbundle", "dynamic bundle").replace("jamtrack", "jam track").replace("rmtpack", "real money pack").replace("staticbundle", "static bundle"),
                                    "price" : (str(item["pricing"]["finalPrice"]) + " V-Bucks") if item["assetType"] != "rmtpack" else "$" + "".join([x for x in str(item["pricing"]["finalPrice"])[:len(str(item["pricing"]["finalPrice"]))-2]]) + "." + str(item["pricing"]["finalPrice"])[-2:],
                                    "inDate" : inDate if inDate == None else inDate.split("T")[0] if "T" in inDate else inDate,
                                    "outDate" : outDate if outDate == None else outDate.split("T")[0] if "T" in outDate else outDate,
                                    "hasVariants" : item.get("hasVariants", None)
                                }

                                itemShop.append(item_dict)
                                del item_dict
                return itemShop
            
        if self.__parsed != None:
            return self.__parsed
        self.__parsed = parser(self.RAWdata)
        return self.__parsed
    
    @property
    def new(self) -> dict:
        now = datetime.datetime.now()
        if 17 <= now.hour <= 23:
            date = now + datetime.timedelta(1)
        else: 
            date = now
        date = date.strftime("%Y-%m-%d")
        df = pandas.DataFrame(self.__parsed)
        
        return df[df.inDate == date].to_json(orient="records", index=False)
    
    @property
    def sections(self) -> list:
        df = pandas.DataFrame(self.__parsed)
        return list(set(df["section"]))
    
    def section(self, section: str) -> dict:
        df = pandas.DataFrame(self.__parsed)
        return df[df.section == section].to_json(orient="records", index = False)
    
    def assetType(self, assetType: str = "emote") -> dict:
        df = pandas.DataFrame(self.__parsed)
        return df[df.assetType == assetType].to_json(orient="records", index = False)
    
    @property
    def categories(self) -> list:
        df = pandas.DataFrame(self.__parsed)
        return list(set(df["category"]))

    def category(self, category: str) -> dict:        
        df = pandas.DataFrame(self.__parsed)
        return df[df.category == category].to_json(orient="records", index=False)
    
    @property
    def leaving(self) -> dict:
        now = datetime.datetime.now()
        if 17 <= now.hour <= 23:
            date = now + datetime.timedelta(1)
        else: 
            date = now
        date = date.strftime("%Y-%m-%d")
        df = pandas.DataFrame(self.__parsed)
        
        return df[df.outDate == date].to_json(orient="records", index = False)
    
    def varaints(self, hasVaraints: bool = True) -> dict:
        df = pandas.DataFrame(self.__parsed)
        return df[df.hasVariants == hasVaraints].to_json(orient="records")
    
    @property
    def dropin(self) -> dict:
        now = datetime.datetime.now()
        if 17 <= now.hour <= 23:
            date = now + datetime.timedelta(1)
        else: 
            date = now
        
        date = date.strftime("%Y-%m-%d")
        
        df = pandas.DataFrame(self.__parsed)
        
        return df[(df.inDate == date) & (df.outDate == date)].to_json(orient="records")