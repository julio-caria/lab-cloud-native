import streamlit as st 
from azure.storage.blob import BlobServiceClient
import os
import pyodbc
import uuid
import json 
from dotenv import load_dotenv

load_dotenv()

blobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobAccountName = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

st.title('Cadastro de Produtos')

# Formulário  
product_name = st.text_input('Nome do Produto')
product_price = st.number_input('Preço do Produto', min_value=0.0, format='%.2f')
product_description = st.text_area('Descrição do Produto')
product_image = st.file_uploader('Imagem do Produto', type=['jpg', 'png', 'jpeg'])

# Salvar Imagem
# file: Arquivo a ser enviado. Deve ter o atributo `name` e ser compatível com leitura binária.
def upload_blob(file):
  # Faz conexão com o serviço de armazenamento da Azure de acordo com Strings de conexão
  blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
  
  # Coleta as informações do container ao qual serão armazenados os blobs
  container_client = blob_service_client.get_container_client(blobContainerName)
  
  # Define o nome do arquivo com um UUID + o nome do Arquivo 
  blob_name = str(uuid.uuid4()) + file.name
  
  # Realiza a criação do arquivo no container
  blob_client = container_client.get_blob_client(blob_name)
  
  # Realiza o envio do arquivo
  blob_client.upload_blob(file.read(), overwrite=True)
  image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
  return image_url

def insert_product(product_name, product_price, product_description, product_image):
  try:
    image_url = upload_blob(product_image)
    # Conecta ao banco de dados SQL Server
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};" f"SERVER={SQL_SERVER};" f"DATABASE={SQL_DATABASE};" f"UID={SQL_USER};" f"PWD={SQL_PASSWORD};")
    cursor = conn.cursor()
    
    # Insere o produto no banco de dados
    insert_sql = f"INSERT INTO Produtos (Nome, Preco, Descricao, Imagem_URL) VALUES (?, ?, ?, ?)"
    cursor.execute(insert_sql, (product_name, product_price, product_description, image_url))
    print(insert_sql)
  
    # Salva as alterações e fecha a conexão
    conn.commit()
    cursor.close()
    conn.close()
  
    return True
  except Exception as e: 
    st.error(f'Erro ao inserir produto: {e}')
    return False

def list_product():
  
  try: 
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};" f"SERVER={SQL_SERVER};" f"DATABASE={SQL_DATABASE};" f"UID={SQL_USER};" f"PWD={SQL_PASSWORD};")
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM [dbo].[Produtos]')
    rows = cursor.fetchall()
    conn.close()
    
    return rows
  except Exception as e:
    st.error(f'Erro ao listar produtos: {e}')

    return []

def list_products_screen():
  products = list_product()
  for product in products:
    st.write(f'Nome: {product[1]}')
    st.write(f'Descrição: {product[2]}')
    st.write(f'Preço: {product[3]}')
    st.write(product[4], width=200)

# Alternativa para def list_products_screen
def list_grid_products_screen():
    products = list_product()
    
    if products:
        card_por_linha = 3
        cols = st.columns(card_por_linha)
        
        for i, product in enumerate(products):
            col = cols[i % card_por_linha]
            with col:
                st.markdown(f"### {product[1]}") 
                st.write(f"**Descrição:** {product[2]}") 
                st.write(f"**Preço:** R${product[3]:.2f}")
                
                if product[4]:
                    html_img = f"<img src='{product[4]}' width='200' height='200' alt='Imagem do Produto {product[1]}'>"
                    st.markdown(html_img, unsafe_allow_html=True)
                
                st.markdown("----")
                
            # Reinicia as colunas a cada nova linha
            if (i + 1) % card_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(card_por_linha)
    else:
        st.info("Nenhum produto encontrado.")

if st.button('Cadastrar Produto'):
  insert_product(product_name, product_price, product_description, product_image)
  st.info("Produto cadastrado com sucesso")
  return_message = 'Produto cadastrado com sucesso'
  
st.header('Produtos Cadastrados')

if st.button('Listar Produtos'): 
  list_grid_products_screen()
  return_message = 'Produtos listados com sucesso'