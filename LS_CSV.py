import os
import csv

class CSVHandler:
    def __init__(self, filepath, filename="produtosML.csv"):
        # Inicializa a classe com um caminho e nome de arquivo especificados.
        self.filepath = os.path.abspath(filepath)
        self.filename = filename
        self.full_path = os.path.join(self.filepath, self.filename)
        self.header = ["Título", "Preço", "URL"]

        # Se o diretório não existir, ele será criado automaticamente.
        self.create_directory()
        self.create_csv_if_not_exists()

    def create_directory(self):
        # Cria o diretório especificado se não existir
        try:
            os.makedirs(self.filepath, exist_ok=True)
            print(f"Pasta '{self.filepath}' ok")
        except OSError as e:
            print(f"Erro em '{self.filepath}': {e}")

    def create_csv_if_not_exists(self):
        # Cria o arquivo CSV com cabeçalhos se não existir
        if not os.path.exists(self.full_path):
            try:
                with open(self.full_path, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(self.header)
                print(f"Arquivo '{self.full_path}' criado")
            except IOError as e:
                print(f"Erro em criar arquivo '{self.full_path}': {e}")

    def save_data(self, title, price, url):
        # Salva ou atualiza os dados do produto no arquivo CSV especificado
        try:
            with open(self.full_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([title, price, url])
            print(f"Dados salvos em {self.full_path}")
        except IOError as e:
            print(f"Erro em '{self.full_path}': {e}")

if __name__ == "__main__":
    filepath = "/home/iagou/Desktop/Projects/LSWebScrapping"
    filename = "my_products.csv"
    csv_handler = CSVHandler(filepath=filepath, filename=filename)
    csv_handler.save_data("Air Fryer Mondial 12L", "R$ 499,99", "https://www.mercadolivre.com.br/fritadeira-air-fryer-oven-mondial-afon-12l-fb-2-em-1-12l-2000w-cor-preta-127v/p/MLB39936633?pdp_filters=item_id%3AMLB5159321302#polycard_client=offers&deal_print_id=ed388b01-3b17-4267-bd94-c01079b8f5e3&position=2&tracking_id=&wid=MLB5159321302&sid=offers")
