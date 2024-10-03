Pour lancer le conteneur avec le back :

télécharger docker desktop

se placer dans le dossier /back

lancer le conteneur :

    docker build -t fastapi-app .
    docker run -d -p 5001:5000 --name fastapi-app-container fastapi-app

pour arrêter le conteneur :

    docker stop fastapi-app-container

pour arrêter en supprimant les volumes (supprime données de la bdd)

    docker rm -v fastapi-app-container

après une modif du code :

    docker build -t fastapi-app .
    docker stop fastapi-app-container
    docker rm -v  fastapi-app-container
    docker run -d -p 5001:5000 --name fastapi-app-container fastapi-app

http://localhost:5001/

avoir les logs :

    docker logs -f <container id>
