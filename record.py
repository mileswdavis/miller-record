#!/usr/bin/python
import subprocess
from datetime import datetime
import time
import sys
import itertools
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import yagmail

# Location to store the sermons
sermon_file_location = "~/Sermons/"
sermon_tmp_file_location = "~/Sermons/tmp/"
sermon_file_name_ending = "Undefined"

class style:
   BOLD = '\033[1m'
   END = '\033[0m'

print ("........................................................")
print (". Welcome to the Miller Ave Auto-Recording Script!     .")
print (". This script will do the following actions in order:  .")
print (". Record, Convert from WAV to MP3, Burn to a CD and    .")
print (". Eject if present, and finally upload the MP3 to      .")
print (". the milleravechurch.com website.                     .")
print ("........................................................")
print ()
print ("--------------------------------------------------------")
print ("| Enter a filename suffix. This could be AM, PM, 1, or |")
print ("| 2. For example if AM is entered the filename would   |")
print ("| be MillerAve_2017-01-16_AM. Do not include spaces.   |")
print ("--------------------------------------------------------")

sermon_file_name_ending = input (style.BOLD + " Enter a filename suffix: " + style.END)
sermon_file_name_ending = "".join(sermon_file_name_ending.split())

sermon_file_name_wav = "MillerAve_" + str(datetime.now().date()) + "_" + sermon_file_name_ending + ".wav"
sermon_file_name_mp3 = "MillerAve_" + str(datetime.now().date()) + "_" + sermon_file_name_ending + ".mp3"

sermon_file_full_path_wav = sermon_tmp_file_location + sermon_file_name_wav
sermon_file_full_path_mp3 = sermon_tmp_file_location + sermon_file_name_mp3

print ()
print ("!!!!!!!!!!!!!!! Starting Recording !!!!!!!!!!!!!!!")

record_process = subprocess.Popen(["rec " + sermon_file_full_path_wav + " > /dev/null 2>&1"], stdout=subprocess.PIPE, shell=True)

print ("--------------------------------------------------------")
print ("| Audio is currently being recorded. It will continue  |")
print ("| recording until you type 'Stop'. Doing so will cease |")
print ("| the recording and begin the next automation stages.  |")
print ("--------------------------------------------------------")

continue_recording = ""
while True:
	if continue_recording == "stop":
		break
	elif continue_recording == "Stop":
		break
	elif continue_recording == "STOP":
		break
	elif continue_recording == "'Stop'":
		break
	continue_recording = input(style.BOLD + " Type 'Stop' to stop the recording: " + style.END)

record_process.terminate()
print ("!!!!!!!!!!!!!!! Recording Finished !!!!!!!!!!!!!!!")
print ()

print ("!!!!!!!!!!!!!!! Starting Conversion !!!!!!!!!!!!!!!")
print ("--------------------------------------------------------")
print ("| Audio is currently being converted from WAV to MP3.  |")
print ("| This will take up to 5 minutes. Once conversion is   |")
print ("| complete it will begin burning a CD. Make sure a CD  |")
print ("| is in the drive is this is your intention.           |")
print ("--------------------------------------------------------")
convert_process = subprocess.Popen(["lame -h " + sermon_file_full_path_wav + " " + sermon_file_full_path_mp3 + " > /dev/null 2>&1"], stdout=subprocess.PIPE, shell=True)

spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])

while convert_process.poll() is None:
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    time.sleep(0.1)
    sys.stdout.write('\b')

print ("!!!!!!!!!!!!!!! Conversion Finished !!!!!!!!!!!!!!!")
print ()

disc_detected = False
#disc_check_process = subprocess.Popen(["drutil discinfo"], stdout=subprocess.PIPE, shell=True)
if disc_detected:
	print ("!!!!!!!!!!!!!!! Disc Burning !!!!!!!!!!!!!!!")
	print ("--------------------------------------------------------")
	print ("| Audio is currently being burned to a CD. Once        |")
	print ("| complete, the CD will eject. This may take 5         |")
	print ("| minutes.                                             |")
	print ("--------------------------------------------------------")
	
	#disc_burn_process = subprocess.Popen(["drutil burn -audio " + sermon_file_full_path_mp3], stdout=subprocess.PIPE, shell=True)
	#while disc_burn_process.poll() is None:
	#    sys.stdout.write(next(spinner))
	#    sys.stdout.flush()
	#    sleep(0.1)
	#    sys.stdout.write('\b')
	#disc_eject_process = subprocess.Popen(["drutil eject"], stdout=subprocess.PIPE, shell=True)
	print ("!!!!!!!!!!!!!!! Disc Burning Finished !!!!!!!!!!!!!!!")
	print ()
else:
	print ("--------------------------------------------------------")
	print ("| A CD was not detected in the burner. Disc burning    |")
	print ("| was skipped.                                         |")
	print ("--------------------------------------------------------")
	print ()

print ("!!!!!!!!!!!!!!! Audio Uploading to Website !!!!!!!!!!!!!!!")
print ("--------------------------------------------------------")
print ("| Using a few simply questions we will try to          |")
print ("| automatically fill in some information about this    |")
print ("| recording. Please use the 'Custom' option for        |")
print ("| sermons being recorded on a day other than Sunday.   |")
print ("--------------------------------------------------------")
sermon_title_str = input (style.BOLD + "Enter a Sermon Title: " + style.END)
valid_website_upload_option = False
while not valid_website_upload_option:
	print ()
	print ("Which common sermon type is this?")
	print ("1. Sunday AM")
	print ("2. Sunday PM")
	print ("3. Custom")
	website_upload_option = input (style.BOLD + "Select an option: " + style.END)
	if int(website_upload_option) > 0 and int(website_upload_option) < 4:
		valid_website_upload_option = True

sermon_day = time.strftime("%d")
sermon_month = time.strftime("%b")
sermon_year = time.strftime("%Y")
sermon_type_id_str = "Sermon"
sermon_availability_str = "Both"


sermon_speaker_option_1 = input (style.BOLD + "Is the speaker David Barnes (Yes or No): " + style.END)
if sermon_speaker_option_1 == "Yes" or sermon_speaker_option_1 == "YES" or sermon_speaker_option_1 == "yes" or sermon_speaker_option_1 == "Y" or sermon_speaker_option_1 == "y":
	sermon_speaker = "David Barnes"
else:
	sermon_speaker_option_2 = input (style.BOLD + "Is the speaker Ben Keehn (Yes or No): " + style.END)
	if sermon_speaker_option_2 == "Yes" or sermon_speaker_option_2 == "YES" or sermon_speaker_option_2 == "yes" or sermon_speaker_option_2 == "Y" or sermon_speaker_option_2 == "y":
		sermon_speaker = "Ben Keehn"
	else:
		sermon_speaker_option_3 = input (style.BOLD + "Is the speaker Jim Malone (Yes or No): " + style.END)
		if sermon_speaker_option_3 == "Yes" or sermon_speaker_option_3 == "YES" or sermon_speaker_option_3 == "yes" or sermon_speaker_option_3 == "Y" or sermon_speaker_option_3 == "y":
			sermon_speaker = "Jim Malone"
		else:
			print ("You should have done the Custom option. Fixing that for you now.")
			website_upload_option = "3"

if int(valid_website_upload_option) == 1:
	sermon_service_id_str = 'AM'
elif int(valid_website_upload_option) == 2:
	sermon_service_id_str = 'PM'

browser = webdriver.Chrome()
browser.get('http://www.milleravechurch.com/admin/sermons/add')
time.sleep(1)

# Login Page
username = browser.find_element(By.ID,'username')
password = browser.find_element(By.ID,'password')
username.send_keys("mileswdavis")
password.send_keys("a4D-r4a-pLo-gyh")

time.sleep(1)

browser.find_element_by_xpath('//input[@type="submit" and @value="login"]').click()

browser.find_element_by_xpath('//button[@id="btn_upload_sermon_uploads"]').click

sermon_date_month = Select(browser.find_element_by_id('sermon_date'))
sermon_date_month.select_by_visible_text(sermon_month)
sermon_date_day = Select(browser.find_element_by_id('sermon_date_day'))
sermon_date_day.select_by_visible_text(sermon_day)
sermon_date_year = Select(browser.find_element_by_id('sermon_date_year'))
sermon_date_year.select_by_visible_text(sermon_year)

sermon_type_id = Select(browser.find_element_by_id('sermon_type_id'))
sermon_type_id.select_by_visible_text(sermon_type_id_str)

sermon_availibility = Select(browser.find_element_by_id('sermon_availability'))
sermon_availibility.select_by_visible_text(sermon_availability_str)

sermon_title = browser.find_element_by_id('sermon_title')
sermon_title.send_keys(sermon_title_str)

sermon_active = browser.find_element_by_id('sermon_active').click()

sermon_upload = browser.find_element_by_xpath("//input[@type='file']")
sermon_upload.send_keys(os.path.expanduser(sermon_file_full_path_mp3))

if int(website_upload_option) != 3:

	sermon_service_id = Select(browser.find_element_by_id('sermon_service_id'))
	sermon_service_id.select_by_visible_text(sermon_service_id_str)

	sermon_speaker_id = Select(browser.find_element_by_id('sermon_speaker_id'))
	sermon_speaker_id.select_by_visible_text(sermon_speaker)

	submit_button = browser.find_element_by_xpath("//button[@type='submit' and text()='Add']")

	while not submit_button.is_displayed():
		sys.stdout.write(next(spinner))
		sys.stdout.flush()
		time.sleep(0.1)
		sys.stdout.write('\b')

	submit_button.click()
	browser.quit()
else:
	print ("--------------------------------------------------------")
	print ("| Complete the sermon information manually in the      |")
	print ("| Chrom web browser. Once complete and submitted,      |")
	print ("| return to this interface and press enter.            |")
	print ("--------------------------------------------------------")
	input (style.BOLD + "Press enter when complete with manual sermon information entry is complete in the browser: " + style.END)
	browser.quit()

print ("!!!!!!!!!!!!!!! Audio Upload Complete !!!!!!!!!!!!!!!")
print ()

announce_email = yagmail.SMTP('mileswdavis')
content = ['The audio upload to milleravechurch.com is complete. Please use the web interface (http://www.milleravechurch.com/admin/sermons/) to make it availible to everyone.']
announce_email.send('mileswdavis@gmail.com', 'MillerAve Sermon Upload Compolete', content)

print ("!!!!!!!!!!!!!!! Cleaning Up !!!!!!!!!!!!!!!")
new_sermon_file_full_path_mp3 = sermon_file_location + sermon_file_name_mp3
while os.path.isfile(os.path.expanduser(new_sermon_file_full_path_mp3)):
	new_sermon_file_full_path_mp3 = new_sermon_file_full_path_mp3.split('.')[0] + "_1.mp3"
cleanup_process = subprocess.Popen(["mv " + sermon_file_full_path_mp3 + " " + new_sermon_file_full_path_mp3 +" && rm " + sermon_file_full_path_wav], shell=True)
print ("!!!!!!!!!!!!!!! Cleanup Complete !!!!!!!!!!!!!!!")

