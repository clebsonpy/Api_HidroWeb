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


	element_basin = driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:j_idt156"]')
	all_basin = {i.get_attribute('text'):i for i in element_basin.find_elements_by_tag_name("option")}
	all_basin[basin].click()

	time.sleep(2)
	element_subbasin = driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:j_idt159"]')
	all_subbasin = {i.get_attribute('text'):i for i in element_subbasin.find_elements_by_tag_name("option")}
	all_subbasin[subbasin].click()

	time.sleep(3)
	element_river = driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:j_idt162-componente"]/div/select')
	all_river = {i.get_attribute('text'):i for i in element_river.find_elements_by_tag_name("option")}
	all_river[river].click()

	click_css_selector(driver, '#form\\:fsListaEstacoes\\:bt')

	time.sleep(4)
	element_station = driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:fsListaEstacoesC:j_idt178:table"]/tbody')
	all_station = [i.get_attribute("text") for i in element_station.find_elements_by_tag_name("a")]
	print(all_station)


#display = Display(visible=True, size=(1500, 900))
#display.start()

select_station(basin="ATLÂNTICO, TRECHO SUDESTE", subbasin="RIO TAQUARI", river="RIO CARREIRO")
#ID_ESTACAO = '47001000'
#download_hidroweb(ID_ESTACAO, home)
