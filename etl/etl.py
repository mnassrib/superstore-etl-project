import psycopg2
import os
import time

# Lire les variables d'environnement
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Le chemin du fichier CSV
csv_file_path = '/data/SuperStoreData.csv'  

# Fonction pour vérifier si la base de données est prête
def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(dbname='postgres', user=db_user, password=db_password, host=db_host)
            conn.close()
            print("Base de données prête")
            break
        except psycopg2.OperationalError:
            print("Attente de la base de données...")
            time.sleep(5)

try:
    # Attendre que la base de données soit prête
    wait_for_db()

    # Connexion initiale pour créer la base de données
    conn = psycopg2.connect(dbname='postgres', user=db_user, password=db_password, host=db_host)
    conn.autocommit = True
    cur = conn.cursor()

    # Suppression et création de la base de données
    cur.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
    print(f'Base de données {db_name} supprimée')
    cur.execute(f'CREATE DATABASE "{db_name}"')
    print(f'Base de données {db_name} créée')
    cur.close()
    conn.close()

    # Connexion à la nouvelle base de données
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
    cur = conn.cursor()

    # Configuration du datestyle
    cur.execute("SET datestyle = 'MDY';")

    # Suppression et création de la table orders
    cur.execute('''
    DROP TABLE IF EXISTS orders;
    CREATE TABLE orders(
        order_id CHAR(14),
        order_date DATE,
        ship_date DATE,
        ship_mode VARCHAR(100),
        customer_id CHAR(8),
        customer_name VARCHAR(50),
        segment VARCHAR(100),
        sales_rep VARCHAR(100),
        sales_team VARCHAR(100),
        sales_team_manager VARCHAR(100),
        location_id VARCHAR(225),
        city VARCHAR(100),
        state VARCHAR(100),
        postal_code CHAR(5),
        region VARCHAR(100),
        product_id CHAR(15),
        category VARCHAR(225),
        sub_category VARCHAR(225),
        product_name VARCHAR(225),
        sales DECIMAL (10,2),
        quantity INT,
        discount DECIMAL(10,2),
        profit DECIMAL(10, 2)
    );
    ''')
    print("Table orders créée")
    conn.commit()

    # Copie des données depuis le fichier CSV
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip the header row
        cur.copy_expert("COPY orders FROM STDIN WITH CSV DELIMITER ','", f)
    conn.commit()
    print("Données importées dans la table orders")

    # Début de la transaction
    cur.execute('BEGIN;')

    # Création des tables dérivées
    cur.execute('''
    DROP TABLE IF EXISTS customers;
    CREATE TABLE customers AS
    SELECT DISTINCT customer_id, customer_name, segment FROM orders;
    ''')
    print("Table customers créée")

    cur.execute('''
    DROP TABLE IF EXISTS product;
    CREATE TABLE product AS
    SELECT DISTINCT product_id, product_name, category, sub_category FROM orders;
    ''')
    print("Table product créée")

    cur.execute('''
    DROP TABLE IF EXISTS sales_team;
    CREATE TABLE sales_team AS
    SELECT DISTINCT sales_rep, sales_team, sales_team_manager FROM orders;
    ''')
    print("Table sales_team créée")

    cur.execute('''
    DROP TABLE IF EXISTS location;
    CREATE TABLE location AS
    SELECT DISTINCT location_id, city, state, postal_code, region FROM orders;
    ''')
    print("Table location créée")
    conn.commit()

    # Suppression des colonnes redondantes de la table orders
    cur.execute('''
    ALTER TABLE orders
    DROP COLUMN customer_name,
    DROP COLUMN segment,
    DROP COLUMN sales_team,
    DROP COLUMN sales_team_manager,
    DROP COLUMN city,
    DROP COLUMN state,
    DROP COLUMN postal_code,
    DROP COLUMN region,
    DROP COLUMN category,
    DROP COLUMN sub_category,
    DROP COLUMN product_name;
    ''')
    conn.commit()
    print("Colonnes redondantes supprimées de la table orders")

    # Ajout de clés primaires et de contraintes de clé étrangère
    cur.execute('''
    ALTER TABLE customers
    ADD CONSTRAINT customers_id PRIMARY KEY (customer_id),
    ALTER COLUMN customer_id SET NOT NULL;
    ''')

    cur.execute('''
    ALTER TABLE location
    ADD CONSTRAINT location_id PRIMARY KEY (location_id),
    ALTER COLUMN location_id SET NOT NULL;
    ''')

    cur.execute('''
    ALTER TABLE product
    ADD CONSTRAINT product_id PRIMARY KEY (product_id),
    ALTER COLUMN product_id SET NOT NULL;
    ''')

    cur.execute('''
    ALTER TABLE sales_team
    ADD CONSTRAINT sales_rep_pk PRIMARY KEY (sales_rep),
    ALTER COLUMN sales_rep SET NOT NULL;
    ''')

    cur.execute('''
    ALTER TABLE orders
    ADD COLUMN order_serial_id SERIAL PRIMARY KEY,
    ADD CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES product (product_id),
    ADD CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES location (location_id),
    ADD CONSTRAINT fk_sales_rep FOREIGN KEY (sales_rep) REFERENCES sales_team (sales_rep);
    ''')
    conn.commit()
    print("Contraintes ajoutées")

    # Création d'index pour améliorer les performances
    cur.execute('''
    CREATE INDEX idx_orders_customer_id ON orders(customer_id);
    CREATE INDEX idx_orders_product_id ON orders(product_id);
    CREATE INDEX idx_orders_location_id ON orders(location_id);
    CREATE INDEX idx_orders_sales_rep ON orders(sales_rep);
    ''')
    conn.commit()
    print("Index créés")

    # Suppression et création de la vue customer_category
    cur.execute('''
    DROP VIEW IF EXISTS customer_category;
    CREATE VIEW customer_category AS
    SELECT 
        c.customer_name,
        COALESCE(SUM(o.sales * o.quantity), 0) AS amount_spent,
        CASE
            WHEN COALESCE(SUM(o.sales * o.quantity), 0) < 5000 THEN 'Silver Customer'
            WHEN COALESCE(SUM(o.sales * o.quantity), 0) <= 10000 THEN 'Gold Customer'
            ELSE 'Diamond Customer'
    END AS customer_category
    FROM orders AS o
    LEFT JOIN customers AS c USING(customer_id)
    GROUP BY c.customer_name
    ORDER BY amount_spent DESC;
    ''')
    conn.commit()
    print("Vue customer_category créée")

finally:
    # Fermeture de la connexion
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Connexion fermée")
