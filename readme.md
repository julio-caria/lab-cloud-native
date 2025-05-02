# BootCamp - Azure Cloud Native

## Introdução

O projeto foi desenvolvido com o intuito de aprofundar os conhecimentos adquiridos no bootcamp de Cloud Native, da plataforma DIO.

O projeto é uma solução que visa utilizar os serviços fornecidos pelo Microsoft Azure, voltado para o armazenamento de imagens e gerenciamento de dados de um e-commerce com foco na escalabilidade, segurança e eficiência.

Mentor: Henrique Eduardo Souza

## Objetivo

Criar um storage para armazenar as imagens dos produtos de um e-commerce.

## Requisitos

- Streamlit
- Azure-Storage-Blob
- Pymssql
- .env

## Tabelas

- Produtos

```sql
CREATE TABLE Produtos (
  ID INT IDENTITY(1, 1) PRIMARY KEY,
  Nome NVARCHAR(255),
  Descricao NVARCHAR(MAX),
  Preco DECIMAL (18,2),
  Imagem_URL NVARCHAR(2083)
)
```

### Comandos a Executar

```bash
pip install -r requirements.txt
streamlit run main.py
```
