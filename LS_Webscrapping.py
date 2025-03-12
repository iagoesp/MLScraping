from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class MercadoLivreScraper:
    def __init__(self):
        self.url = None
        self.driver = self.configure_selenium()

    def define_url(self, url):
        # Define a URL do produto que será analisado.
        self.url = url

    def configure_selenium(self):
        # Configura o Selenium com o WebDriver do Chrome
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(service=service, options=options)

    def get_infos(self):
        # Extrai o título e o preço da página do produto
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 2) # Define um tempo máximo de espera para os elementos carregarem
        title = self.get_title(wait)
        price = self.get_price(wait)
        return title, price

    def get_title(self, wait):
        # Encontra e retorna o título do produto na página
        title_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//h1[@class="ui-pdp-title"]')
        ))
        return title_element.text

    def get_price(self, wait):
        # Encontra e retorna o preço do produto na página 
        price_meta = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//meta[@itemprop="price"]')
        ))
        return price_meta.get_attribute("content")

    def scrape_price(self):
        # Método principal para capturar os dados e fechar o navegador
        try:
            title, price = self.get_infos()
            print(f"Title found: {title}") 
            print(f"Price found: {price}") 
            return title, price, self.url
        except Exception as e:
            print(f"Error: {e}")
            return None, None, None
        finally:
            self.driver.quit()


if __name__ == "__main__":
    MLS = MercadoLivreScraper()
    url =  "https://www.mercadolivre.com.br/fritadeira-air-fryer-oven-mondial-afon-12l-fb-2-em-1-12l-2000w-cor-preta-127v/p/MLB39936633?pdp_filters=item_id%3AMLB5159321302#polycard_client=offers&deal_print_id=ed388b01-3b17-4267-bd94-c01079b8f5e3&position=2&tracking_id=&wid=MLB5159321302&sid=offers"
    MLS.define_url(url)
    MLS.scrape_price()
