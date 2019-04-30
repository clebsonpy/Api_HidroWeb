# -*- coding: utf-8 -*-
import time
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

home = os.path.expanduser('~')

def wait_load_items(driver, xpath, id_station):

	n = 1
	p = 1
	while p:
		try:
			driver.find_element_by_xpath(xpath)
			p = 0
		except:
			print(n, id_station)
			time.sleep(1)
			n += 1
		if n == 300:
			print('Tempo de espera excedito. Processo encerrado.')
			exit()

def click_css_selector(driver, css_selector):
	n = 0
	p = 1
	while p:
		try:
			driver.find_element_by_css_selector(css_selector).click()
			p = 0
		except:
			time.sleep(1)
			n += 1

		if n == 300:
			print('Tempo de espera excedido.')
			break

def download_hidroweb(id_station, dir_out):

	fp = webdriver.FirefoxProfile()

	fp.set_preference("browser.download.folderList",2)
	fp.set_preference("browser.download.dir", dir_out)
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

	driver = webdriver.Firefox(firefox_profile=fp)
	url = 'http://www.snirh.gov.br/hidroweb/publico/apresentacao.jsf'
	driver.get(url)
	time.sleep(1)
	driver.get(url)
	n = 0
	p = 1
	while  p:
		try:
			driver.find_element_by_link_text('Séries Históricas').click()
			p = 0
		except:
			time.sleep(1)
			n += 1
		if n == 300:
			print('Tempo de espera excedido. Processo encerrado.')
			exit()

	wait_load_items(driver, '//*[@id="form:fsListaEstacoes:codigoEstacao"]', id_station)
	driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:codigoEstacao"]').send_keys([id_station, Keys.ENTER])
	click_css_selector(driver, '#form\\:fsListaEstacoes\\:bt')
	wait_load_items(driver, '//div[contains(@class, "checkbox i-checks")]', id_station)
	time.sleep(2)
	try:
		driver.find_element_by_xpath('//div[contains(@class, "checkbox i-checks")]').click()
		click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesC\\:radTipoArquivo-componente > div:nth-child(2) > div:nth-child(2)')
		click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesC\\:btBaixar')
	except Exception as e:
		print(e)



def select_station(basin, subbasin, river):
	driver = webdriver.Firefox()
	url = 'http://www.snirh.gov.br/hidroweb/publico/apresentacao.jsf'
	driver.get(url)

	n = 0
	p = 1
	while  p:
		try:
			driver.find_element_by_link_text('Séries Históricas').click()
			p = 0
		except:
			time.sleep(1)
			n += 1
		if n == 300:
			print('Tempo de espera excedido. Processo encerrado.')
			exit()


	for label, ctr in [['Bacia', basin], ['SubBacia', subbasin], ['Rio', river]]:
		time.sleep(1)
		element = driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:componente"]')
		all_elements = {i.find_element_by_tag_name("label").text:i for i in element.find_elements_by_class_name(name="form-group")}

		all_basin = {i.get_attribute('text'):i for i in all_elements[label].find_elements_by_tag_name("option")}
		all_basin[ctr].click()


	click_css_selector(driver, '#form\\:fsListaEstacoes\\:bt')

	pg = 1
	pgt = 2
	list_sta = []
	while pg <= pgt:
		time.sleep(1)
		driver.find_element_by_link_text('%s' % pg).click()
		time.sleep(1)
		station = driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:fsListaEstacoesC:componente"]')
		all_station = [i.get_attribute("text") for i in station.find_elements_by_tag_name("a")]
		for i in all_station:
			if len(i) >= 8 and len(i) <= 9:
				list_sta.append(i)
		pg+=1
		pgt = int(all_station[-3])

	return list_sta



display = Display(visible=False, size=(1500, 900))
display.start()
station = select_station(basin="ATLÂNTICO, TRECHO SUDESTE", subbasin="RIO TAQUARI", river="RIO CARREIRO")
display.stop()
for i in station:
	display = Display(visible=False, size=(1500, 900))
	display.start()
	download_hidroweb(i, home)
	display.stop()
