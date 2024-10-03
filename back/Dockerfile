# Utiliser une image de base légère avec Python
FROM python:3.9.2-alpine

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer curl pour les health checks
RUN apk add --no-cache curl

# Installer Jinja2 pour le templating
RUN pip install Jinja2

# Installer python-multipart pour gérer les formulaires
RUN pip install python-multipart

# Ajouter un utilisateur non-root pour plus de sécurité
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app

# Définir le répertoire de travail
WORKDIR /home/app

# Copie le répertoire static dans l'image Docker
COPY ./static /home/app/static

# Changer l'utilisateur
USER nonroot

# Copier tous les fichiers dans le conteneur
COPY --chown=nonroot:nonroot . .

# Créer un environnement virtuel
ENV VIRTUAL_ENV=/home/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Mettre à jour pip et installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Exposer le port que l'application utilisera
EXPOSE 5000

# Démarrer uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
