# Utiliser l'image officielle de Python
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app/work

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Copier le script Python etl dans le conteneur
COPY etl.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande par défaut à exécuter lorsque le conteneur démarre
CMD ["python", "etl.py"]
