import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Lire les variables d'environnement
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DBNAME')
db_user = os.getenv('USER')
db_password = os.getenv('PASSWORD')

# Afficher les valeurs des variables d'environnement pour vérification
print(f"DB_HOST: {db_host}")
print(f"DBNAME: {db_name}")
print(f"USER: {db_user}")
print(f"PASSWORD: {db_password}")