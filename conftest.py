import pytest
from selenium import webdriver


import xml.etree.ElementTree as ET


class XML:
    #Parsing the ScriptConfig(Userdata) XML file
    Tree = ET.parse("Files\\Config.xml")
    Root = Tree.getroot()
    UserInputXL = Root[0].text  #Location of the Excel file
    AOL = Root[1].text          #AOL Site Link
    UserName = Root[2].text     #Username
    Password = Root[3].text     #Password


#Using Fixture to wrap-up the test case
@pytest.fixture(scope="class")   # Loading the Microsoft Edge Browser based on the data from ScriptConfig
def Setup(request):

    driver = webdriver.Edge(executable_path="C:\\msedgedriver.exe")
    driver.get(XML.AOL)
    driver.maximize_window()
    driver.find_element_by_css_selector("input[name=name]").send_keys(XML.UserName)
    driver.find_element_by_css_selector("input[name=pass]").send_keys(XML.Password)
    driver.find_element_by_css_selector("input[value=Login]").click()
    driver.maximize_window()
    driver.implicitly_wait(5)
    request.cls.driver = driver

    yield
    driver.quit()
    pass

