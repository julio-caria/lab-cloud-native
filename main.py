import streamlit as st 
from azure.storage.blob import BlobServiceClient
import os
import pymssql
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
product_description = st.text_area('Nome do Produto')
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
  image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName/blob_name}"
  return image_url

def insert_product(name, price, description, image_url):
  # Conecta ao banco de dados SQL Server
  conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
  cursor = conn.cursor()
  
  # Insere o produto no banco de dados
  cursor.execute("INSERT INTO Products (Nome, Preco, Descricao, Imagem_URL) VALUES ('{product_name}', '{product_price}', '{product_description}', '{product_image}')")
  
  # Salva as alterações e fecha a conexão
  conn.commit()
  cursor.close()
  conn.close()

if st.button('Cadastrar Produto'):
  return_message = 'Produto cadastrado com sucesso'
  
st.header('Produtos Cadastrados')

if st.button('Listar Produtos'): 
  return_message = 'Produtos listados com sucesso'