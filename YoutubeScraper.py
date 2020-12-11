from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import string
import time
import pandas as pd

YT_Channel = 'https://www.youtube.com/c/%E6%97%85%E8%89%B2/videos'

PATH = "/Users/temporary/Documents/coruscant/src/chrome_driver/mac/chromedriver"                                        #Change depending on location of chromedriver
driver = webdriver.Chrome(PATH)

driver.get(YT_Channel)                                                                                                  #Load videos page
driver.maximize_window()
time.sleep(5)
print(f"Currently on {driver.current_url}")
print(driver.title)

for i in range(5):                                                                                                      #Change depending on how many videos
    #scroll 1000 px
    driver.execute_script('window.scrollTo(0,(window.pageYOffset+1000))')
    print("Scrolling", i+1, "times")
    #waiting for the page to load
    time.sleep(1)
print("Scrolling done")

driver.execute_script('window.scrollTo(0,(window.pageYOffset+1000))')

videos = driver.find_elements_by_class_name('style-scope ytd-grid-video-renderer')

video_list = []

print("Compiling video records")

v = 0

for video in videos:
    v = v+1
    print("Getting information on video", v)
    title = video.find_element_by_xpath('.// *[ @ id = "video-title"]').text
    views = video.find_element_by_xpath('.//*[@id="metadata-line"]/span[1]').text
    length = video.find_element_by_xpath('.//*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span').text
    when = video.find_element_by_xpath('.//*[@id="metadata-line"]/span[2]').text
    link = video.find_element_by_xpath('.// *[ @ id = "video-title"]').get_attribute('href')
    vid_item = {
        'title': title,
        'views': views,
        'length': length,
        'posted': when,
        'url': link
    }
    video_list.append(vid_item)

df = pd.DataFrame(video_list)

rows = df.shape[0]
spec_view = 0
row = 0
wait = WebDriverWait(driver, 30)

while row < rows:
    driver.get(df.iloc[spec_view]['url'])
    print("Updating record", row+1, "of", rows)

    e1_wait = wait.until(
        EC.visibility_of_element_located((By.XPATH, './/*[@id="count"]/yt-view-count-renderer/span[1]')))
    ActionChains(driver).move_to_element(e1_wait).perform()
    e1 = driver.find_element_by_xpath('.//*[@id="count"]/yt-view-count-renderer/span[1]')
    df.iloc[spec_view]['views'] = e1.text
    print(df.iloc[spec_view]['views'])

    e2_wait = wait.until(
        EC.visibility_of_element_located((By.XPATH, './/*[@id="date"]/yt-formatted-string')))
    ActionChains(driver).move_to_element(e1_wait).perform()
    e2 = driver.find_element_by_xpath('.//*[@id="date"]/yt-formatted-string')
    df.iloc[spec_view]['posted'] = e2.text
    print(df.iloc[spec_view]['posted'])

    spec_view = spec_view + 1
    row = row + 1

df['views'] = df['views'].str.replace(r'\D', '')

print(df)

df.to_csv(r'/Users/temporary/Desktop/youtube.csv', encoding='utf-8-sig')

driver.quit()