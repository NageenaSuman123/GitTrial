
# ------------- Selenium Python Test Frameowrk AOL(Phase-1)------------#


import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Xedge.Exceldata import Data


@pytest.mark.usefixtures("Setup")
class TestFramework:
    def test_AOLSite(self):
        global closeTab

        for J in range(0, len(Data.InstruList)):
            self.driver.implicitly_wait(5)
            self.driver.refresh()
            self.driver.find_element_by_link_text("Browse").click()  # Navigating to Browse Section
            #******************************  Search Section ************************#
            Y = len(self.driver.find_elements_by_xpath("//body/div[2]/form[2]/div/table/tbody/tr[2]/td[2]/input"))#No of characters present in 'Browse Versioned Legislation'
            print("No of Alphabets present in 'Browse by Legislation section'=" + str(Y))
            #for a in range(0, len(Data.InstruList)):
            abc = self.driver.find_element_by_xpath("//body/div[2]/form[2]/div/table/tbody/tr[2]/td[2]")
            my_char = ord('A')  # convert char to ascii
            if Data.InstruList[J] is not None:
                while my_char <= ord(Data.CharList[J]):  #Iterating from 'A' till the first character of instrument name till it gets matched
                    if my_char == ord(Data.CharList[J]):
                        print(Data.CharList[J])
                        abc.find_element_by_xpath("//input[@value='" + Data.CharList[J] + "']").click()   #Opening the link based on first character
                        try:
                            print(Data.InstruList[J])
                            element = self.driver.find_element(By.LINK_TEXT, "show all")
                            element.is_displayed()
                            element.click()
                            self.driver.find_element(By.LINK_TEXT, Data.InstruList[J]).click()

                        except NoSuchElementException:
                            self.driver.find_element(By.LINK_TEXT, Data.InstruList[J]).click()
                    my_char += 1  # iterate over abc
            else:
                continue

            parent = self.driver.window_handles[0]
            #__________________________Checking whether instrument is available with nodes/not____________________
            try:
                self.driver.find_element_by_id("expand_button")
            except NoSuchElementException:
                print("No nodes are available for the instrument:" + Data.InstruList[J])   # Writing the no of nodes count if not present to workbook
                Data.sheet.cell(row=J + 2, column=2).value = int(0)
                Data.sheet.cell(row=J + 2, column=3).value = "No timeline nodes are present"
                Data.Workbook.save("Files\\UserFile.xlsx")
                continue
            # ****************************  Nodes Loading Section  ***********************#
            Node = self.driver.find_elements_by_xpath("//body[1]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[1]/table/tbody/tr/td")  # Grabbing the no of nodes
            Count = len(Node)
            Data.sheet.cell(row=J+2, column=2).value = Count   #Writing the no of nodes count to workbook
            Data.Workbook.save("Files\\UserFile.xlsx")
            print("No of Nodes available=" + str(Count))
            node = 0
            Explicit = WebDriverWait(self.driver, 5)
            List = []

            while node <= Count:  # Initialising the node and iterating till the nth node
                self.driver.find_element_by_id("expand_button").click()
                node = node + 1
                getLink = self.driver.find_elements(By.XPATH, "//body[1]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[1]/table/tbody/tr/td" + "[" + str(node) + "]" + "/a[last()]")
                for links in getLink:  #To get the instrument document link
                    URL = links.text
                    List.append(URL)
                if node <= Count:  # Loading the nodes one by one till the nth node
                    DateElement = self.driver.find_element_by_xpath(
                    "//body[1]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[1]/table/tbody/tr/td" + "[" + str(
                    node) + "]")
                    Date = DateElement.get_attribute("innerText")
                    NodeDate = Date.split()[0]
                    Explicit.until(EC.element_to_be_clickable((By.XPATH,"//body[1]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[1]/table/tbody/tr/td" + "[" + str(node) + "]"))).click()
                    NodeErrList = ["The Versioned Legislation Database System is presently unable to locate the legislation contemplated for the hyperlink that you have selected.  You may wish to locate the legislation concerned by using the Search or Browse functions of the Versioned Legislation Database System.Thank you."]
                    NodeText = self.driver.execute_script('return document.getElementsByTagName("span")[3].textContent')
                    for z in range(0, len(NodeErrList)):
                        try:
                            assert NodeErrList[z] not in NodeText
                        except AssertionError:
                            print("The link is broken for the Node:" + str(node))
                            NodeUrl = self.driver.execute_script('return document.URL')
                            print(NodeUrl)
    #######################################     Drafting Output for Nodes Section ###########################
                            #********************   Node Number  ***************
                            a = 0
                            if Data.sheet.cell(row=J+2, column=3).value is None:
                                Data.sheet.cell(row=J+2, column=3).value = str(node) + "-" + NodeDate + ","
                            elif not Data.sheet.cell(row=J+2, column=3).value is None:
                                Em = Data.sheet.cell(row=J+2, column=3).value
                                Data.sheet.cell(row=J+2, column=3).value = "".join([Em, "\n", str(node), "-", NodeDate]) + ","
                            a = a + 1
                            Data.Workbook.save("Files\\UserFile.xlsx")
                            # ********************   Node URL ***************
                            a = 0
                            if Data.sheet.cell(row=J+2, column=4).value is None:
                                Data.sheet.cell(row=J+2, column=4).value = NodeUrl + ","
                            elif not Data.sheet.cell(row=J+2, column=4).value is None:
                                Em1 = Data.sheet.cell(row=J+2, column=4).value
                                Data.sheet.cell(row=J+2, column=4).value = "".join([Em1, "\n", NodeUrl]) + ","
                            a = a + 1
                            Data.Workbook.save("Files\\UserFile.xlsx")
                    self.driver.back()
                    
            # **********************************   Document Loading Section  **************************#
            print("The List of Amending documents present are:")
            for i in range(0, Count):  # To iterate over the amending links and skipping the non-loading documents
                if i < Count:
                    if List[i] != '':
                        self.driver.find_element_by_link_text(List[i]).click()
                        DocuErrList = ["The Versioned Legislation Database System is presently unable to locate the legislation contemplated for the hyperlink that you have selected.  You may wish to locate the legislation concerned by using the Search or Browse functions of the Versioned Legislation Database System.Thank you.", "No records found."]
                        DocuText = self.driver.execute_script('return document.getElementsByTagName("span")[3].textContent')
                        for y in range(0, len(DocuErrList)):
                            try:      #Type-1 Error Check
                                assert DocuErrList[y] not in DocuText
                            except AssertionError:
        #######################################     Drafting Output for Amend Documents Section ###########################
                            # ********************   AmendNote  ***************
                                print(List[i] + "-" + DocuErrList[y])
                                DocuUrl = self.driver.execute_script('return document.URL')
                                a = 0
                                if Data.sheet.cell(row=J+2, column=5).value is None:
                                    Data.sheet.cell(row=J+2, column=5).value = List[i] + ","
                                elif not Data.sheet.cell(row=J+2, column=5).value is None:
                                    E1 = Data.sheet.cell(row=J+2, column=5).value
                                    Data.sheet.cell(row=J+2, column=5).value = "".join([E1, "\n", List[i]]) + ","
                                a = a + 1
                                Data.Workbook.save("Files\\UserFile.xlsx")
                                # ********************   AmendNote URL  ***************
                                a = 0
                                if Data.sheet.cell(row=J+2, column=6).value is None:
                                    Data.sheet.cell(row=J+2, column=6).value = DocuUrl + ","
                                elif not Data.sheet.cell(row=J+2, column=6).value is None:
                                    E2 = Data.sheet.cell(row=J+2, column=6).value
                                    Data.sheet.cell(row=J+2, column=6).value = "".join([E2, "\n", DocuUrl]) + ","
                                a = a + 1
                                Data.Workbook.save("Files\\UserFile.xlsx")

                        self.driver.back()
                        Explicit.until(EC.element_to_be_clickable((By.ID, "expand_button"))).click()
                        print(List[i])

            #*******************************  PDF Loading Section   ************************#
            NonPDF = self.driver.find_elements_by_xpath("//td/img[@alt='Blank']")
            print("No of Blanks(without PDF links)=" + str(len(NonPDF)))
            PDF = self.driver.find_elements_by_xpath("//td/a/img[@alt='View PDF']")
            print("No of PDF links=" + str(len(PDF)))
            j = len(PDF)
            PDFErrList = ["Page not found", "Could not find pdf file with url:"]

            for Link in PDF:
                Link.click()
                self.driver.switch_to.window(parent)
            i = 1
            closeTab = []
            while i <= j:
                child = self.driver.window_handles[i]
                self.driver.switch_to.window(child)
                print(i)
                for k in range(0, len(PDFErrList)):
                    try:
                        PDFText = self.driver.execute_script('return document.body.innerText')
                        PDFUrl = self.driver.execute_script('return document.URL')
                        assert PDFErrList[k] not in PDFText
                    except AssertionError:
    #######################################     Drafting Output for PDF Section ###########################
                        # ********************   PDF URL  ***************
                        a = 0
                        if Data.sheet.cell(row=J+2, column=7).value is None:
                            Data.sheet.cell(row=J+2, column=7).value = PDFUrl + ","
                        elif not Data.sheet.cell(row=J+2, column=7).value is None:
                            NE = Data.sheet.cell(row=J+2, column=7).value
                            Data.sheet.cell(row=J+2, column=7).value = "".join([str(NE), "\n", PDFUrl]) + ","
                        a = a + 1
                        Data.Workbook.save("Files\\UserFile.xlsx")
                        # ********************   PDF Number  ***************
                        a = 0
                        if Data.sheet.cell(row=J+2, column=8).value is None:
                            Data.sheet.cell(row=J+2, column=8).value = str(i) + ","
                        elif not Data.sheet.cell(row=J+2, column=8).value is None:
                            NE1 = Data.sheet.cell(row=J+2, column=8).value
                            Data.sheet.cell(row=J+2, column=8).value = "".join([str(NE1), "\n", str(i)]) + ","
                        a = a + 1
                        Data.Workbook.save("Files\\UserFile.xlsx")
                closeTab.append(self.driver.window_handles[i])
                i += 1

            for tab in range(0, len(closeTab)):
                self.driver.switch_to.window(closeTab[tab])
                self.driver.close()
                self.driver.switch_to.window(parent)

            ############################    Node Icon and MouseHover Text Comparison ####################
            ############ Image link ########
            images = self.driver.find_elements_by_xpath("//a//span//img")
            imageLink = []
            for element in images:
                imageLink.append(element.get_attribute("src"))
            print(imageLink)
            print(len(imageLink))

            ######## Icon text #######
            for icon in range(0, len(imageLink)):

                TotalData = self.driver.find_element_by_xpath("//body[1]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[1]/table/tbody/tr/td[" + str(icon + 1) + "]")
                NodeData = TotalData.get_attribute("innerText")
                Data1 = " ".join(NodeData.split())
                print(Data1)
                MouseHover = Data1.split()[1].lower()
                print(MouseHover)

                if MouseHover in imageLink[icon]:
                    print("Matched")
                elif (MouseHover == "spent") and ("formal-cons-cur" in imageLink[icon]):
                    print("Spent Node - Matched")
                elif (MouseHover == "informal") and ("retro" in imageLink[icon]):
                    print("Retro Node - Matched")
                else:
                    print("Not Matched" + "No," + "Node:" + str(icon+1))
                    if Data.sheet.cell(row=J + 2, column=9).value is None:
                        Data.sheet.cell(row=J + 2, column=9).value = "No," + "Node:" + str(icon+1)
                    elif not Data.sheet.cell(row=J + 2, column=9).value is None:
                        E1 = Data.sheet.cell(row=J + 2, column=9).value
                        Data.sheet.cell(row=J + 2, column=9).value = E1 + "\n" + "No," + "Node:" + str(icon+1)
                    Data.Workbook.save("Files\\UserFile.xlsx")
                ###########################   Check for Amended by string on nodes ###########################

                if (icon+1 == 1) and (("Act" in Data1) or ("RevEd" in Data1)):
                    print("Its a OE node")
                    continue  # Skipping the iteration for first node as it is OE node
                if ("Spent" in Data1) or ("RevEd" in Data1):
                    print("Its a Spent/RevisedEdition node")
                elif ("Amended by" in Data1) or ("Repealed by" in Data1):
                    print("Matching")
                else:
                    print("Not matching for the node:" + str(icon+1))
                    if Data.sheet.cell(row=J + 2, column=10).value is None:
                        Data.sheet.cell(row=J + 2, column=10).value = "Not begins with Amended by,for the node:" + str(icon+1)
                    elif not Data.sheet.cell(row=J + 2, column=10).value is None:
                        E2 = Data.sheet.cell(row=J + 2, column=10).value
                        Data.sheet.cell(row=J + 2, column=10).value = E2 + "\n" + "Not begins with Amended by,for the node:" + str(icon+1)

                    Data.Workbook.save("Files\\UserFile.xlsx")




























