#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():

	try:

		with open('class_info.txt') as f:
			lines = f.read().splitlines()

		[null, null, null, null, null, null, username, password, null, null, null, 
		location1, subject1, number1, section1, labDay1, recDay1, null, null, null, location2, subject2, 
		number2, section2, labDay2, recDay2, null, null, null, location3, subject3, number3, section3, labDay3, recDay3, null, 
		null, null, location4, subject4, number4, section4, labDay4, recDay4, null, null, null, null] = lines

		section1 = section1 + " "
		section2 = section2 + " "
		section3 = section3 + " "
		section4 = section4 + " "

		subjects = [subject1, subject2, subject3, subject4]
		numbers = [number1, number2, number3, number4]
		labDays = [labDay1, labDay2, labDay3, labDay4]
		recDays = [recDay1, recDay2, recDay3, recDay4]
		sections = [section1, section2, section3, section4]
		locations = [location1, location2, location3, location4]

		index = 0
		classIndex = 1

		labExists = False
		recExists = False
		classExists = False

		classBlocks = []
		labBlocks = []
		recBlocks = []

		print("")
		print("*pat* *pat* good bot!")
		print("starting...")

		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		PATH = "/Users/castiel/chromedriver"
		driver = webdriver.Chrome(PATH, options = options)

		driver.get("https://webapp4.asu.edu/catalog/classlist?t=2217&hon=F&promod=F&e=open&page=1")

		login1 = driver.find_element_by_id("asu_mobile_button").click()
		time.sleep(1)
		login2 = driver.find_element_by_class_name("text").click()

		print("")
		print("logging in with given crudentials...")

		user = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "username"))
			)
		user.send_keys(username)

		passwrd = driver.find_element_by_id("password")
		passwrd.send_keys(password)
		passwrd.send_keys(Keys.RETURN)

		print("")
		print("DUO required for initial log in")

		iframe = driver.find_element_by_tag_name("iframe")
		driver.switch_to.frame(iframe)

		authenticate = driver.find_element_by_tag_name("body")

		push = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.ID, "auth_methods"))
				)
		time.sleep(1)
		print("push sent...")
		pushMe = push.find_element_by_class_name("row-label.push-label")
		finalPush = pushMe.find_element_by_tag_name("button").click()

		subSearch = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.ID, "subjectEntry"))
				)
		numSearch = driver.find_element_by_id("catNbr")

		print("")
		print("login successful!")
		print("ASU course catalog loaded")

		while index < 4:

			time.sleep(5)

			print("")
			print("searching for class " + str(classIndex) + ": " + subjects[index] + " " + numbers[index])

			subSearch = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.ID, "subjectEntry"))
				)
			numSearch = driver.find_element_by_id("catNbr")

			subSearch.clear()
			numSearch.clear()
			subSearch.send_keys(subjects[index])
			numSearch.send_keys(numbers[index])
			numSearch.send_keys(Keys.RETURN)

			time.sleep(3)

			catalog = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.ID, "CatalogList"))
				)

			body = catalog.find_element_by_tag_name("tbody")

			courses = body.find_elements_by_tag_name("tr")

			for course in courses:

				className = course.find_element_by_class_name("subjectNumberColumnValue.nowrap")
				title = course.find_element_by_class_name("titleColumnValue")
				sectionNum = course.find_element_by_class_name("classNbrColumnValue")
				instructor = course.find_element_by_class_name("instructorListColumnValue")
				section = course.find_element_by_class_name("dayListColumnValue.hide-column-for-online")
				start = course.find_element_by_class_name("startTimeDateColumnValue.hide-column-for-online")
				end = course.find_element_by_class_name("endTimeDateColumnValue.hide-column-for-online")
				location = course.find_element_by_class_name("locationBuildingColumnValue.nowrap")
				date = course.find_element_by_class_name("startDateColumnValue.nowrap")

				classInfo = className.text + " " + title.text + " " + sectionNum.text + " " + instructor.text + " " + section.text + " " + start.text + " " + end.text + " " + location.text + " " + date.text

				if(className.text == subjects[index] + " " + numbers[index]):

					if(title.text != "Laboratory"):

						classLocation = (location.text.split()[0])

						if(classLocation == locations[index]):


							if(section.text == sections[index]):

								classExists = True

								print("")
								print("class loaded with: " + locations[index] + " | " + sections[index])
								print("")

								print("     " + className.text + " " + title.text + " " + sectionNum.text)
								print("     " + instructor.text + " " + section.text + start.text + "- " + end.text)
								print("     " + location.text + " " + date.text)
								
								classLine1 = (className.text + " " + title.text + " " + sectionNum.text)
								classLine2 = (instructor.text + " " + section.text + start.text + "- " + end.text)
								classLine3 = (location.text + " " + date.text)
								classLine4 = ""

								classBlocks.append(classLine1)
								classBlocks.append(classLine2)
								classBlocks.append(classLine3)
								classBlocks.append(classLine4)

								time.sleep(1)

								if(labDays[index] != "*REPLACE WITH LAB DAY ('M', 'T', 'W', 'Th', or 'F') IF NO LAB, DO NOT MODIFY LINE*"):

									print("")
									print("searching for lab on: " + labDays[index])

									time.sleep(3)

									link = course.find_element_by_css_selector('[alt="Select"]').click()

									expand = WebDriverWait(body, 10).until(
										EC.presence_of_element_located((By.CLASS_NAME, "panel-heading.accordion-toggle"))
										)
									contents = expand.get_attribute('href')
									expand.click()

									if(contents == "#Laboratory"):

										lab = body.find_element_by_class_name("table.table-hover.related-classes-tbl")
										myLab = lab.find_element_by_tag_name("tbody")
										selections = myLab.find_elements_by_tag_name("tr")

										for selection in selections:

											infos = selection.find_elements_by_class_name("rc")

											for info in infos:

												if(info.text == labDays[index]):

													print("")
													print("lab found:")
													print("")
													
													labStuff = selection.text.split()
														
													labInfoForUser1 = (labStuff[1] + " " + labStuff[2] + " " + labStuff[3] + " " + labStuff[4]
													 + " " + labStuff[5] + " - " + labStuff[6] + " " + labStuff[7])

													labInfoForUser2 = (labStuff[8] + " " + labStuff[9] + " " + labStuff[10] + " " + labStuff[11]
													 + " " + labStuff[12] + " " + labStuff[13])

													labInfoForUser3 = ""

													labBlocks.append(labInfoForUser1)
													labBlocks.append(labInfoForUser2)
													labBlocks.append(labInfoForUser3)

													print("     " + labInfoForUser1)
													print("     " + labInfoForUser2)

													time.sleep(1)
													info.click()

													labExists = True


										if(labExists == False):

											print("")
											print("unable to add class...")
											print("your chosen lab day is closed or does not exist")
											time.sleep(3)
											break

										if(labExists == True):

											add = WebDriverWait(body, 10).until(
												EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-asu.add-button"))
												)
											add.click()
											labExists = False



								if(recDays[index] != "*REPLACE WITH RECITATION DAY ('M', 'T', 'W', 'Th', or 'F') IF NO RECITATION, DO NOT MODIFY LINE*"):

									print("")
									print("searching for recitation on: " + recDays[index])

									time.sleep(3)

									link = course.find_element_by_css_selector('[alt="Select"]').click()

									expand = WebDriverWait(body, 10).until(
										EC.presence_of_element_located((By.CLASS_NAME, "panel-heading.accordion-toggle"))
										)
									contents = expand.get_attribute('href')
									expand.click()

									if(contents == "#Recitation"):

										lab = body.find_element_by_class_name("table.table-hover.related-classes-tbl")
										myLab = lab.find_element_by_tag_name("tbody")
										selections = myLab.find_elements_by_tag_name("tr")

										for selection in selections:

											infos = selection.find_elements_by_class_name("rc")

											for info in infos:

												if(info.text == recDays[index]):

													print("")
													print("recitation found:")
													print("")
													
													recStuff = selection.text.split()
														
													recInfoForUser1 = (recStuff[1] + " " + recStuff[2] + " " + recStuff[3] + " " + recStuff[4]
													 + " " + recStuff[5] + " - " + recStuff[6] + " " + recStuff[7])

													recInfoForUser2 = (recStuff[8] + " " + recStuff[9] + " " + recStuff[10] + " " + recStuff[11]
													 + " " + recStuff[12] + " " + recStuff[13])

													recInfoForUser3 = ""

													recBlocks.append(recInfoForUser1)
													recBlocks.append(recInfoForUser2)
													recBlocks.append(recInfoForUser3)

													print("     " + recInfoForUser1)
													print("     " + recInfoForUser2)

													time.sleep(1)
													info.click()

													recExists = True


										if(recExists == False):

											print("")
											print("unable to add class...")
											print("your chosen recitation day is closed or does not exist")
											time.sleep(3)
											break

										if(recExists == True):

											add = WebDriverWait(body, 10).until(
												EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-asu.add-button"))
												)
											add.click()
											recExists = False


								if(labDays[index] == "*REPLACE WITH LAB DAY ('M', 'T', 'W', 'Th', or 'F') IF NO LAB, DO NOT MODIFY LINE*"):


									if(recDays[index] == "*REPLACE WITH RECITATION DAY ('M', 'T', 'W', 'Th', or 'F') IF NO RECITATION, DO NOT MODIFY LINE*"):

										time.sleep(3)
										link = course.find_element_by_class_name("btn.btn-add-class").click()


								print("")
								print("adding to class cart...")
								time.sleep(2)

								cart = WebDriverWait(driver, 10).until(
									EC.presence_of_element_located((By.CLASS_NAME, "ps_mid_section"))
									)
									
								addCart = cart.find_element_by_class_name("ps_box-button.psc_primary.psc_button-next")

								clickAdd = addCart.find_element_by_id("ASU_ADDCLAS_WRK_ADD_BTN").click()

								if(index < 3):

									classSearch = WebDriverWait(driver, 10).until(
										EC.presence_of_element_located((By.CLASS_NAME, "pst_panel-content"))
										)

									searchy = WebDriverWait(driver, 10).until(
										EC.presence_of_element_located((By.CLASS_NAME, "ps_box-scrollarea.psa_list-linkmenu.psc_list-has-icon.psa_vtab"))
										)

									print("cart updated!")

									time.sleep(2)
									expand = WebDriverWait(driver,10).until(
										EC.presence_of_element_located((By.ID, "PT_SIDE$PIMG"))
										)
									expand.click()

									print("")
									print("--------------------------------")
									print("   starting next class search   ")
									print("--------------------------------")

									time.sleep(2)
									nowSearch = WebDriverWait(driver,10).until(
										EC.presence_of_element_located((By.ID, "win2divSCC_NAV_TAB_row$2"))
											)
									time.sleep(1)
									nowSearch.click()

								break

			if(classExists == False):

				print("")
				print("unable to find class " + subjects[index] + " " + numbers[index] + " in section " + sections[index])
				print("your chosen section is closed or does not exist")
				time.sleep(3)

			else:


				classExists = False


			index += 1
			classIndex += 1

		print("cart updated!")
		time.sleep(5)
		print("")
		print("**********************************************")
		print("******** your final ASU Shopping Cart ********")
		print("**********************************************")
		print("")

		print("Classes:")
		print("")

		for classBlock in classBlocks:

			print("     " + classBlock)

		print("Labs:")
		print("")

		for labBlock in labBlocks:

			print("     " + labBlock)

		print("Recitations:")
		print("")

		for recBlock in recBlocks:

			print("     " + recBlock)

		print("***********************************************")
		print("*** this bot only adds classes to your cart ***")
		print("******* make sure to finish enrolling! ********")
		print("***********************************************")
		print("")

		driver.quit()

	finally:

		driver.quit()

main()