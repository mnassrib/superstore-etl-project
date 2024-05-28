# Projet ETL avec Docker, PostgreSQL, pgAdmin et JupyterLab

Ce projet propose une configuration Docker pour exécuter un processus ETL (Extract, Transform, Load) sur des données de vente de la base de données SuperStore. Le processus ETL extrait les données d'un fichier CSV, les transforme selon les besoins et les charge dans une base de données PostgreSQL. Il utilise également pgAdmin pour gérer la base de données via une interface web et JupyterLab pour explorer et visualiser les données.

## Prérequis

- Docker installé sur votre système. [Guide d'installation Docker](https://docs.docker.com/get-docker/)
- Un navigateur web pour accéder aux interfaces utilisateur (pgAdmin et JupyterLab).

## Structure du Répertoire

```
superstore-project/
├── data/
│   └── SuperStoreData.csv
├── etl/
│   ├── Dockerfile
│   ├── etl.py
│   └── requirments.txt
├── images/
│   └── erd.png
├── notebooks/
├── docker-compose.yml
└── README.md
```

## Configuration

1. Clonez ce dépôt sur votre machine :

    ```bash
    git clone https://github.com/mnassrib/superstore-project.git
    cd superstore-project
    ```

2. Ouvrez un terminal dans le répertoire du projet et exécutez la commande suivante pour démarrer les services Docker :

    ```bash
    docker-compose up --build
    ```
    ---
        - Pour savoir les noms des conteneurs Docker en cours d'exécution

        ```bash
        docker-compose ps
        ```

        - Pour vérifier les logs d'un conteneur

        ```bash
        docker logs "nom du conteneur"
        ```
    ---

3. Une fois les conteneurs démarrés, vous pourrez accéder aux services suivants dans votre navigateur web :

    - **pgAdmin** : [http://localhost:8080](http://localhost:8080)
    - **JupyterLab** : [http://localhost:8888](http://localhost:8888)

## Contenu du Projet

- **data/** : Contient le fichier CSV contenant les données de vente.
- **etl/** : Contient le script ETL et son Dockerfile.
    - `Dockerfile` : Fichier Dockerfile pour construire l'image Docker du service ETL.
    - `etl.py` : Script Python exécutant le processus ETL.
    - `requirments.txt` : Fichier texte pour spécifier les dépendances et les packages Python nécessaires au projet.
- **images/** : Contient les images utilisées dans le README.md.
    - `erd.png` : Entity Relationship Diagram (ERD) illustrant la structure des tables de la base de données SuperStore.
- **notebooks/** : Pour contenir les fichiers notebooks pour les analyses et visualisations des données. 
- **docker-compose.yml** : Fichier de configuration Docker définissant les services et leurs paramètres.
- **README.md** : Ce fichier, fournissant des instructions sur la configuration et l'utilisation du projet.

## Utilisation

1. Connectez-vous à pgAdmin avec les informations d'identification suivantes :
    - Email : adresse émail choisie pour votre pgAdmin
    - Mot de passe : mot de passe choisi pour pgAdmin
    - Enregistrer un nouveau serveur :
        - Clic droit sur "Servers" > "Register" > "Server..."
    - Configurer le serveur :
        - Onglet "General" : Name = nom choisi pour votre serveur, exemple : PostgreSQL
    - Onglet "Connection" :
        - Host name/address = nom choisi pour votre service postgres : voir **docker-compose.yml**
        - Port = 5432
        - Maintenance database = nom choisi pour votre base de données
        - Username = nom choisi pour votre user
        - Password = mot de passe choisi pour votre user
        - Save password? = activé
    - Cliquez sur "Save"

2. Utilisez pgAdmin pour explorer, interroger et gérer la base de données PostgreSQL.

3. Connectez-vous à JupyterLab avec le token d'accès affiché dans la console au démarrage.

4. Utilisez JupyterLab pour explorer, analyser et visualiser les données à l'aide de notebooks Python.

## Auteurs

- [B. Mnassri](https://github.com/mnassrib) - Développeur principal

## Note

Les données utilisées dans ce projet, ainsi que la normalisation des tables de la base de données, sont inspirées de l'article intitulé "[DATABASE DESIGN: BUILDING A BUSINESS DATABASE FROM A CSV FILE](https://medium.com/@oluwatobiaina/database-design-building-a-business-database-from-a-csv-file-5698e87b1e78)" rédigé par l'auteur O. Aina. Cet article offre une approche détaillée pour concevoir une base de données à partir d'un fichier CSV, ce qui a servi de base pour la conception de la structure de la base de données SuperStore dans ce projet.

## Entity Relationship Diagram (ERD)

L'Entity Relationship Diagram (ERD) ci-dessous illustre la structure des tables de la base de données SuperStore :

![ERD](images/erd.png)

- **orders** : Table principale contenant les informations sur les commandes.
- **customers** : Table contenant les informations sur les clients.
- **product** : Table contenant les informations sur les produits.
- **sales_team** : Table contenant les informations sur l'équipe de vente.
- **location** : Table contenant les informations sur les emplacements.
