# Comment contribuer

**Ne JAMAIS commit sur `master`**. De toutes façons, la branche `master` est protégée. Personne ne push dessus.

## Gestion des branches

Tout se passe sur la branche `dev`. Pas besoin de créer de nouvelles branches. Pour aller sur la branche `dev`, il faut faire : 
```bash
git checkout dev
```
Après avoir fait vos modifications, il faut faire : 

```bash
git add .
git commit -m "[partie de l'app concernée] Votre message"
git push origin dev
```

Sur [Github](https://github.com/agnlt64/go-upjv/), il faut créer une pull request sur la branche `dev`. Si les changements sont mineurs, vous pouvez les merge directement. Sinon, il faut que quelqu'un d'autre fasse une review. Une fois que la PR aura été merge, il faut synchroniser la branche `master` avec la branche `dev`. Pour cela, il faut faire : 
```bash
# sync master
git checkout master
git pull origin master

# sync dev
git checkout dev
git merge master
git push origin dev
```