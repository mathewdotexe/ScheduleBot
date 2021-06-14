#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():

	with open('input.txt') as f:
		lines = f.read().splitlines()

	[null, null, null, null, null, null, username, password, null, null, null, 
	location1, subject1, number1, labDay1, null, null, null, location2, subject2, 
	number2, labDay2, null, null, null, location3, subject3, number3, labDay3, null, 
	null, null, location4, subject4, number4, labDay4, null, null, null, null] = lines

	subjects = [subject1, subject2, subject3, subject4]
	numbers = [number1, number2, number3, number4]
	labDays = [labDay1, labDay2, labDay3, labDay4]
	locations = [location1, location2, location3, location4]

	index = 0
	classIndex = 1

	labExists = False

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
		print("loading class " + str(classIndex) + " subject preferences...")

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
			location = course.find_element_by_class_name("locationBuildingColumnValue.nowrap")
			title = course.find_element_by_class_name("titleColumnValue")
			instructor = course.find_element_by_class_name("instructorListColumnValue")

			if(className.text == subjects[index] + " " + numbers[index]):

				if(title.text != "Laboratory"):

					classLocation = (location.text.split()[0])

					if(classLocation == locations[index]):

						if(labDays[index] != "*REPLACE WITH 'M', 'T', 'W', 'Th', or 'F' (IF NO LAB, DO NOT MODIFY LINE)*"):

							print("")
							print("class found!")

							time.sleep(3)

							link = course.find_element_by_css_selector('[alt="Select"]').click()

							expand = WebDriverWait(body, 10).until(
								EC.presence_of_element_located((By.CLASS_NAME, "panel-heading.accordion-toggle"))
								)
							expand.click()

							lab = body.find_element_by_class_name("table.table-hover.related-classes-tbl")
							myLab = lab.find_element_by_tag_name("tbody")
							selections = myLab.find_elements_by_tag_name("tr")

							for selection in selections:

								infos = selection.find_elements_by_class_name("rc")

								for info in infos:

									if(info.text == labDays[index]):

										print("lab found!")

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


						else:

							print("")
							print("class found!")

							time.sleep(3)

							link = course.find_element_by_class_name("btn.btn-add-class").click()

						print("adding to class cart...")
						time.sleep(1)

						cart = WebDriverWait(driver, 10).until(
							EC.presence_of_element_located((By.CLASS_NAME, "ps_mid_section"))
							)
							
						addCart = cart.find_element_by_class_name("ps_box-button.psc_primary.psc_button-next")

						clickAdd = addCart.find_element_by_id("ASU_ADDCLAS_WRK_ADD_BTN").click()

						if(index < 3):

							classSearch = WebDriverWait(driver, 10).until(
								EC.presence_of_element_located((By.CLASS_NAME, "pst_panel-content"))
								)

							print("almost there...")
							searchy = WebDriverWait(driver, 10).until(
								EC.presence_of_element_located((By.CLASS_NAME, "ps_box-scrollarea.psa_list-linkmenu.psc_list-has-icon.psa_vtab"))
								)

							time.sleep(2)
							expand = WebDriverWait(driver,10).until(
								EC.presence_of_element_located((By.ID, "PT_SIDE$PIMG"))
								)
							expand.click()

							time.sleep(2)
							nowSearch = WebDriverWait(driver,10).until(
								EC.presence_of_element_located((By.ID, "win2divSCC_NAV_TAB_row$2"))
									)
							nowSearch.click()
							print("cart updated!")

						break

		index += 1
		classIndex += 1

	print("class cart finalized!")
	print("")
	time.sleep(2)
	print("schedule building process complete")
	print("")
	driver.quit()

main()
