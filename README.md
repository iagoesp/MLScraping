# MLScraping

Este projeto consiste em um sistema simples para extrair informações de produtos do Mercado Livre e salvá-las em um arquivo CSV, contando também com uma interface gráfica desenvolvida em PyQt5.
![image](https://github.com/user-attachments/assets/ed303216-a50c-413f-9334-5b631e672eed)

Estrutura de Arquivos
    

- LS_GUI.py :
  
    Código principal que implementa a interface gráfica usando PyQt5.
    Permite inserir uma URL de produto do Mercado Livre, realizar o scraping, exibir as informações como título, preço e URL e salvar em um arquivo CSV.
    Também possibilita carregar o CSV e exibir em tabela os dados dos produtos previamente salvos.

- LS_Webscrapping.py:
        
    Classe MercadoLivreScraper que utiliza o Selenium para fazer o scraping no Mercado Livre.
    Abre a página de produto, obtém título e preço, e retorna junto à URL fornecida.

- LS_CSV.py:
        
    Classe CSVHandler responsável pela criação e/ou manipulação do arquivo CSV.
    Cria o arquivo, caso não exista, e salva os dados


 
## Requisitos

- Python 3.7+
- PyQt5 (para a interface gráfica)
- Selenium (para o scraping)
- webdriver_manager (para gerenciar o driver do Chrome)

Criar um ambiente virtual usando
```python -m venv ls_env```

Utilizar o ambiente definido
```source ./ls_env/bin/activate```

Para instalar as dependências necessárias, utilize:

```pip install pyqt5 selenium webdriver-manager```


 
### Como Executar

Verifique ou defina as dependências de acordo com a lista de requisitos.
Abra um terminal na pasta do projeto.
Execute o arquivo principal da interface gráfica:

```python LS_GUI.p```

- A janela abrirá.
- Insira a URL de um produto do Mercado Livre no campo apropriado e clique em “Scrap” para obter o título e o preço.
- Configure a pasta e o nome do arquivo CSV (por padrão, produtosML.csv), e então clique em “Salvar produto” para gravar as informações no CSV.
- Clique em “Carregar planilha” para visualizar na tabela todos os produtos já salvos no CSV.


 
### Personalização

- Caso deseje utilizar outro nome de arquivo CSV ou outro diretório, altere diretamente na interface o campo “Pasta:” e “Nome do arquivo:”.
- Para redefinir os campos de texto, como a URL, pasta ou nome de arquivo, há um botão “Limpar” ao lado de cada campo.


 
### Observações Importantes:

- A planilha, em formato CSV, será criada automaticamente caso não exista, incluindo o cabeçalho “Título, Preço, URL”.
- As URLs exibidas são clicáveis. Ao clicar, o navegador padrão abrirá o respectivo link.
- O scraping é realizado sem precisar abrir uma janela visível do navegador, por meio do Selenium.
- O projeto utiliza um timer para evitar cliques sucessivos no botão “Scrap” em intervalos muito curtos.
