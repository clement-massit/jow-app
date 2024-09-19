# Utiliser une image officielle de Python comme image de base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt (si vous en avez un) ou installer les dépendances directement dans le Dockerfile
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du répertoire local dans le répertoire de travail du conteneur
COPY . .

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Commande pour démarrer l'application avec uvicorn
ENTRYPOINT [ "python", "-m", "uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
# CMD ["ls"]
