from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
import pymongo,time
from Setting import Username,Password,Host,DBName,ClientName
from urllib.parse import quote

option = webdriver.ChromeOptions()
#option.add_argument('--proxy-server=127.0.0.1:9000')
# option.add_argument('--headless')

option.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = Chrome(options=option)

def login(name,password):
	url = "https://login.taobao.com/member/login.jhtml"
	browser.get(url)
	# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR()))).click()
	try:
		browser.find_element_by_css_selector("div.login-switch #J_Quick2Static").click()
	except Exception as e:
		pass
	browser.find_element_by_id("TPL_username_1").send_keys(name)
	browser.find_element_by_id("TPL_password_1").send_keys(password)
	time.sleep(1)
	try:
		slider = browser.find_element_by_css_selector("#nc_1_n1z")
		action = ActionChains(browser)
		action.drag_and_drop_by_offset(slider, 500, 0).perform()
		time.sleep(3)
	except Exception as e:
		pass
	time.sleep(2)
	browser.find_element_by_id("J_SubmitStatic").click()
	
def index_page(page):
	print("正在爬取第",page,"页")
	try:
		browser.get("https://s.taobao.com/search?q="+quote(ShopName))
		try:
			slider2 = browser.find_element_by_css_selector("#nc_1__scale_text span.nc-lang-cnt")
			action2 = ActionChains(browser)
			action2.drag_and_drop_by_offset(slider2,500,0).perform()
			time.sleep(5)
		except Exception as e:
			pass
		input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager div.form > input")))
		submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#mainsrp-pager div.form > span.btn.J_Submit")))
		input.clear()
		input.send_keys(page)
		submit.click()
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager li.item.active > span"),str(page)))
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".m-itemlist .items .item")))
		get_products()
	except TimeoutException:
		index_page(page)

def get_products():
	html = browser.page_source
	doc = pq(html)
	items = doc("#mainsrp-itemlist .items .item").items()
	for item in items:
		product = {
			'image':item.find('.pic .img').attr('data-src'),
			'price':item.find('.price').text(),
			'deal':item.find('.deal-cnt').text(),
			'title':item.find('.title').text(),
			'shop':item.find('.shop').text(),
			'location':item.find('.location').text(),
		}
		print(product)
		save_to_mongo(product)

def save_to_mongo(result):
	client = pymongo.MongoClient(Host)
	db = client[DBName]
	try:
		if db[ClientName].insert(result):
			print("存储成功")
	except Exception as e:
		print(e)
		print("存储失败")


def main():
	for x in range(21,101):
		import time
		time.sleep(10)
		index_page(x)
if __name__ == "__main__":
	wait = WebDriverWait(browser, 10)
	ShopName = input("请输入要爬去的商品名称")
	login(Username,Password)
	main()
	browser.close()
	
