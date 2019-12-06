# Projet phase 3

### Instructions pour que tout roule comme sur des roues

#### Sur GitHub
Fork le [projet principal](https://github.com/TP2-Python/Tp3.git).
Copier le lien de votre fork.

Dans votre fork, créer une nouvelle b

#### Sur votre ordinateur
1. Créer un nouveau dossier pour le projet et l'ouvrir avec VS Code.
2. Ouvrir un terminal.
3. Écrire `git clone (url_de_votre_fork)`
4. Ouvrir le nouveau dossier créé par git avec VS Code
5. Exécuter les commandes suivantes:
```
git remote add upstream (url_du_projet_principal)
git checkout -b working_branch
```
Vous avez maintenant une branche local dans laquelle vous pouvez travailler. 
Pour push dans votre fork, vous n'avez qu'à faire `git push origin master`, puis faire une pull request 
sur GitHub.

C'est une peu différent, je me suis rendu compte qu'on a pas besoin de 2 branches dans notre fork (sur GitHub).
On va donc toujours push dans origin master et faire nos pull requests à partir de là.
