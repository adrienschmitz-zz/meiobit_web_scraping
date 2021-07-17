from bs4 import BeautifulSoup
import pandas as pd 
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("window-size=800,600")
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

#do selenimum
driver = webdriver.Chrome(options=options)
driver.get('https://tecnoblog.net/meiobit/')
#do beautiful
html = driver.page_source
soup = BeautifulSoup(html)

sleep(2)
cookies = driver.find_element_by_css_selector('div > a')
cookies.click()

#a listagem de posts apenas para pegar os links, que são entregues antes da div de cada posts
lista_posts = soup.find('div', attrs={'class': 'col-articles-list f-left'})

links = driver.find_elements_by_xpath("//a[@class='list-post-link']")

hrefs=[]

#cria a lista de links que serão acessados um a um posteriormente
for link in links:
    hrefs.append(link.get_attribute('href'))

#cria o dicionário vazio
d = []

#acessa cada uma das postagens e salva o titulo, resumo, autor e data, alem de guardar no dicionario
for href in hrefs:
    driver.get(href)
    titulo = driver.find_element_by_tag_name('h1')
    resumo = driver.find_element_by_tag_name('h2')
    autor = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div[1]/div[2]/p/a")
    data = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div[1]/div[2]/p/span")
    sleep(0.5)

    d.append(
        {
            'Titulo': titulo.text, 
            'Resumo': resumo.text, 
            'Autor': autor.text, 
            'Data': data.text
        }
    )

#converte o dicionario para dataframe
dados = pd.DataFrame.from_dict(d)

#converte o dataframe para excell(xlsx)
dados.to_excel("meiobit.xlsx")
