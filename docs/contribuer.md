# Comment contribuer

**Ne JAMAIS commit directement sur `master`**. La branche `master` est protégée et représente la version stable du projet.

## Workflow de développement

Le projet suit un workflow basé sur des **branches de feature**. Chaque nouvelle fonctionnalité ou correction doit être développée dans sa propre branche, puis mergée directement dans `master` via une Pull Request.

### 1. Créer une branche de feature

Avant de commencer à travailler, assurez-vous d'être à jour avec `master` :

```bash
git checkout master
git pull origin master
```

Créez ensuite votre branche de feature avec un nom descriptif :

```bash
git checkout -b type/nom-de-la-feature
```

**Convention de nommage des branches :**
- `feature/nom-fonctionnalite` : pour une nouvelle fonctionnalité
- `fix/nom-correction` : pour une correction de bug
- `ui/nom-interface` : pour des modifications d'interface
- `docs/nom-documentation` : pour de la documentation
- `refactor/nom-refactoring` : pour du refactoring

**Exemples :**
```bash
git checkout -b feature/add-notifications
git checkout -b fix/login-validation
git checkout -b ui/user-profile
git checkout -b docs/api-documentation
```

### 2. Développer votre feature

Travaillez sur votre branche et committez régulièrement vos modifications :

```bash
git add .
git commit -m "Description claire de vos modifications"
```

**Format des messages de commit :**
```
[type] Description concise

Description détaillée si nécessaire
```

**Exemples :**
- `[feature] Ajout du système de notifications`
- `[fix] Correction de la validation du formulaire de connexion`
- `[ui] Refonte de la page de profil utilisateur`
- `[docs] Mise à jour de la documentation API`

### 3. Pusher votre branche

Une fois votre travail terminé, poussez votre branche sur GitHub :

```bash
git push origin type/nom-de-la-feature
```

### 4. Créer une Pull Request

Sur [GitHub](https://github.com/agnlt64/go-upjv/), créez une Pull Request de votre branche vers `master`.

**Règles de review :**
- Si les changements sont **mineurs** (typos, petites corrections), vous pouvez merger directement
- Si les changements sont **importants** (nouvelle feature, refactoring), demandez une review

### 5. Merger et nettoyer

Une fois la Pull Request approuvée et mergée :

1. Revenez sur `master` et mettez à jour :
```bash
git checkout master
git pull origin master
```

2. Supprimez votre branche locale (optionnel mais recommandé) :
```bash
git branch -d type/nom-de-la-feature
```

### 6. Répéter le cycle

Pour chaque nouvelle feature, repartez de l'étape 1 en créant une nouvelle branche depuis `master` **à jour**.
