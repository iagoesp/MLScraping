import csv
import os
import sys
from time import sleep
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QGroupBox, QTableWidget, QTableWidgetItem, QAbstractItemView)

from LS_Webscrapping import MercadoLivreScraper
from LS_CSV import CSVHandler

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema - Lista de produtos do Mercado Livre")
        self.setFixedSize(1000, 600)

        self.current_title = ""
        self.current_price = ""
        self.current_url = ""

        self.define_ui()

    def define_ui(self):
        # Layout:
        #    3 containers:
        #       - Container Superior:
        #           Scraping e exibição dos dados
        #       - Container Intermediário:
        #           Carregar e/ou salvar os dados
        #       - Container Inferior:
        #           Lista de produtos e/ou leitura do CSV

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Container Superior:
        # Scraping e exibição dos dados
        top_container = QGroupBox("Scraping")
        top_layout = QVBoxLayout()
        top_container.setLayout(top_layout)

        # Linha do campo de texto da URL do Container Superior:
        #   Contém label "URL", campo de texto "URL" e o botão "Scrap"
        url_text_top_layout = QHBoxLayout()
        self.url_label = QLabel("URL do produto:")
        self.url_line_edit = QLineEdit()
        self.delete_url_button = QPushButton("Limpar")
        self.scrap_button = QPushButton("Scrap")
        # Inicialmente desabilitado até o usuário digitar
        self.scrap_button.setEnabled(False)  

        #Adicionando os componentes da linha da URL 
        url_text_top_layout.addWidget(self.url_label)
        url_text_top_layout.addWidget(self.url_line_edit)
        url_text_top_layout.addWidget(self.delete_url_button)
        url_text_top_layout.addWidget(self.scrap_button)

        # Linha do título do Container Superior:
        # exibindo título e preço dos produtos lado a lado
        title_top_layout = QHBoxLayout()
        self.title_text_label = QLabel("Título:")
        self.title_value_label = QLabel("--")
        self.price_text_label = QLabel("Preço:")
        self.price_value_label = QLabel("--")

        #Adicionando os componentes da linha do título 
        title_top_layout.addWidget(self.title_text_label)
        title_top_layout.addWidget(self.title_value_label)
        title_top_layout.addSpacing(50)
        title_top_layout.addWidget(self.price_text_label)
        title_top_layout.addWidget(self.price_value_label)

        # Linha da exibição da URL do Container Superior:
        # exibindo a URL do produto
        url_display_layout = QHBoxLayout()
        self.url_text_label = QLabel("URL:")
        self.url_value_label = QLabel("--")
        self.url_value_label.setOpenExternalLinks(True)
        self.url_value_label.setTextInteractionFlags(Qt.TextBrowserInteraction)

        #Adicionando os componentes da exibição da URL
        url_display_layout.addWidget(self.url_text_label)
        url_display_layout.addWidget(self.url_value_label)

        # Linha do botão para salvar produto e 
        # adicionando o componente no layout
        save_button_layout = QHBoxLayout()
        self.save_button = QPushButton("Salvar produto")
        save_button_layout.addStretch()
        save_button_layout.addWidget(self.save_button)

        # Adiciona os layouts ao Container Superior
        top_layout.addLayout(url_text_top_layout)
        top_layout.addLayout(title_top_layout)
        top_layout.addLayout(url_display_layout)
        top_layout.addLayout(save_button_layout)

        # Container Intermediário:
        # Carregando e/ou salvando os dados
        middle_container = QGroupBox("Configurações do arquivo em CSV")
        middle_layout = QVBoxLayout()
        middle_container.setLayout(middle_layout)

        # Linha para configurar o path da pasta
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Pasta:")
        self.folder_line_edit = QLineEdit()
        self.delete_folder_button = QPushButton("Limpar")
        self.folder_button = QPushButton("Selecione a pasta")
        self.folder_line_edit.setText(os.getcwd())

        # Adicionando os componentes da linha do path da pasta
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_line_edit)
        folder_layout.addWidget(self.delete_folder_button)
        folder_layout.addWidget(self.folder_button)

        # Linha para configurar o nome do path do arquivo CSV
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Nome do arquivo:")
        self.file_line_edit = QLineEdit("produtosML.csv")
        self.delete_file_button = QPushButton("Limpar")

        # Adicionando os componentes da linha do path do arquivo CSV
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_line_edit)
        file_layout.addWidget(self.delete_file_button)


        # Adiciona os layouts ao Container Intermediário
        middle_layout.addLayout(folder_layout)
        middle_layout.addLayout(file_layout)

        # Container Inferior:
        # Lista de produtos e/ou leitura do CSV
        bottom_container = QGroupBox("Lista de Produtos")
        bottom_layout = QVBoxLayout()
        bottom_container.setLayout(bottom_layout)

        # Adicionando botão para carregar o CSV
        open_csv_layout = QHBoxLayout()
        self.open_csv_button = QPushButton("Carregar planilha")
        open_csv_layout.addStretch()
        open_csv_layout.addWidget(self.open_csv_button)

        # Configurando tabela para mostrar os produtos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Título", "Preço", "URL"])
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        # Permite ajustar a largura das colunas
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # Adiciona os layouts ao Container Inferior
        bottom_layout.addLayout(open_csv_layout)
        bottom_layout.addWidget(self.table_widget)

        # Adiciona os Containers ao layout principal e
        # ajustar a proporção para cada container
        main_layout.addWidget(middle_container)
        main_layout.addWidget(top_container)
        main_layout.addWidget(bottom_container)

        # Define um timer depois de clicar o botão e antes de fazer o scraping
        # para evitar múltiplos cliques
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.do_scraping)

        # Associa as funções aos botões e ativa ou desativa o botão "Scrap"
        self.url_line_edit.textChanged.connect(self.on_url_text_changed)
        self.scrap_button.clicked.connect(self.countdown_to_do_scraping)
        self.save_button.clicked.connect(self.save_data_csv)
        self.folder_button.clicked.connect(self.select_folder)
        self.open_csv_button.clicked.connect(
            self.load_csv_into_table)
        self.delete_url_button.clicked.connect(
            lambda: self.delete_content(self.url_line_edit))
        self.delete_folder_button.clicked.connect(
            lambda: self.delete_content(self.folder_line_edit))
        self.delete_file_button.clicked.connect(
            lambda: self.delete_content(self.file_line_edit))


    def delete_content(self, widget):
        widget.setText("")
        
    # Uma função para habilitar e desabilitar o botão "Scrap"
    # O botão é ativado se o campo de texto não estiver vazio
    # Caso contrário, é desabilitado
    def on_url_text_changed(self, text):
        if text.strip():
            self.scrap_button.setEnabled(True)
        else:
            self.scrap_button.setEnabled(False)

    # Define uma função para alertar uma espera e desabilitar o botão "Scrap" e
    # inicializa um contador para executar o scraping
    def countdown_to_do_scraping(self):
        self.scrap_button.setText("Aguarde..")
        self.scrap_button.setEnabled(False)
        self.timer.start(2)
        
    # Realiza o scraping da URL e exibe os valores nos campos das labels.
    # Para isso acontecer, aguarda o timer finalizar e exibe um texto no botão
    def do_scraping(self):
        # Encerra o timer
        self.timer.stop()
        self.scrap_button.setText("Insira uma nova URL")
        url = self.url_line_edit.text().strip()
        if not url:
            self.title_value_label.setText("URL vazia")
            self.price_value_label.setText("--")
            self.url_value_label.setText("--")
            return

        # Realiza o scraping com a URL do produto
        scraper = MercadoLivreScraper()
        scraper.define_url(url)
        title, price, returned_url = scraper.scrape_price()

        if title and price and returned_url:
            self.current_title = title
            self.current_price = price
            self.current_url = returned_url

            # Insere os textos do título, preço e URL nas labels na tela
            self.title_value_label.setText(title)
            self.price_value_label.setText(price)
            link_html = f'<a href="{returned_url}">{returned_url}</a>'
            self.url_value_label.setText(link_html)
        else:
            self.current_title = ""
            self.current_price = ""
            self.current_url = ""
            self.title_value_label.setText("Erro ao obter dados")
            self.price_value_label.setText("--")
            self.url_value_label.setText("--")

    # Seleciona o path da pasta para salvar a planilha
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 
                                                       "Selecione a pasta")
        if folder_path:
            self.folder_line_edit.setText(folder_path)

    # Salva as informações na planilha e atualiza a lista na aplicação
    def save_data_csv(self):
        if not self.current_title or not \
            self.current_price or not self.current_url:
            return

        folder_path = self.folder_line_edit.text().strip()
        filename = self.file_line_edit.text().strip()

        if not folder_path:
            folder_path = os.getcwd()
            self.folder_line_edit.setText(folder_path)
        if not filename:
            filename = "produtosML.csv"

        # Cria o arquivo em CSV e salva os dados
        csv_handler = CSVHandler(filepath=folder_path, filename=filename)
        csv_handler.save_data(self.current_title, self.current_price, 
                              self.current_url)

        # Adiciona na tabela cada produto com as suas características
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)

        # Colunas: Título // Preço // URL
        self.table_widget.setItem(row_count, 0, QTableWidgetItem(
            self.current_title))
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(
            self.current_price))

        link_label = QLabel(f'<a href="{self.current_url}"> \
                            {self.current_url}</a>')
        link_label.setOpenExternalLinks(True)
        self.table_widget.setCellWidget(row_count, 2, link_label)

        #print(f"Dados salvos e adicionados à lista: {self.current_title}, {self.current_price}, {self.current_url}")

    # Carrega o arquivo em CSV e insere na tabela os dados dos produtos
    def load_csv_into_table(self):
        folder_path = self.folder_line_edit.text().strip()
        filename = self.file_line_edit.text().strip()

        if not folder_path:
            folder_path = os.getcwd()
        if not filename:
            filename = "produtosML.csv"

        full_path = os.path.join(folder_path, filename)

        if not os.path.exists(full_path):
            #print(f"Arquivo CSV '{full_path}' não existe.")
            return

        # Recria a tabela
        self.table_widget.setRowCount(0)

        # Lê o arquivo em CSV e insere os dados na tabela 
        # na ordem Título // Preço // URL
        with open(full_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None) 

            row_index = 0
            for line in reader:
                if len(line) < 3:
                    continue
                title, price, url = line[0], line[1], line[2]

                self.table_widget.insertRow(row_index)

                # Colunas: Título // Preço // URL
                self.table_widget.setItem(row_index, 0, QTableWidgetItem(title))
                self.table_widget.setItem(row_index, 1, QTableWidgetItem(price))

                link_label = QLabel(f'<a href="{url}">{url}</a>')
                link_label.setOpenExternalLinks(True)
                self.table_widget.setCellWidget(row_index, 2, link_label)

                row_index += 1

        #print(f"Arquivo '{full_path}' carregado. Total de linhas lidas: {self.table_widget.rowCount()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
