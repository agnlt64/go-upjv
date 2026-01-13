# Go UPJV

App de covoiturage pour l'UPJV t'as capté

## Quickstart
Après avoir cloné le repo, il faut créer un fichier `.env` à la racine du projet. ce fichier contient toutes les variables d'environnement nécessaires. Exemple :
```
DEV_DATABASE_URL=sqlite:///dev.db
SECRET_KEY=une-clé-secrète
```
La `SECRET_KEY` est nécessaire pour les sessions utilisateur. Pour générer une nouvelle clé, vous pouvez utiliser OpenSSL :
```bash
openssl rand -hex 32
```
Ou sous Windows :
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Lors du premier lancement, il faut créer un environnement virtuel, installer les dépendances et seeder la base de données :
```bash
uv venv
source .venv/bin/activate # ou .venv\Scripts\activate sous Windows
uv sync
uv run seeder.py
```

Pour lancer le serveur, il faut activer l'environnement virtuel et lancer le serveur :

```bash
source .venv/bin/activate # ou .venv\Scripts\activate sous Windows
uv run main.py
```
Le serveur sera lancé sur [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Stack technique

- [uv](https://docs.astral.sh/uv/)
- Python 3.13
- Flask
- SQLAlchemy
- TailwindCSS

## Documentation

- [Contribuer](./docs/contribuer.md)