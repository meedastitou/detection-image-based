# # Utiliser une image de base Python officielle
# FROM python:3.9-slim

# # Définir le répertoire de travail dans le conteneur
# WORKDIR /app

# # Copier le fichier requirements.txt dans le conteneur
# COPY requirements.txt .

# # Installer les dépendances
# RUN pip install --no-cache-dir -r requirements.txt

# # Définir la variable d'environnement pour indiquer que Flask est en mode production
# ENV FLASK_ENV=production

# # Copier le reste de l'application dans le conteneur
# COPY . .

# # Exposer le port sur lequel l'application va fonctionner
# EXPOSE 5000

# # Définir la commande pour exécuter l'application
# CMD ["python", "app.py"]
FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]