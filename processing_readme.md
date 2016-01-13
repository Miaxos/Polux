### Processing.py
http://py.processing.org

Processing est un langage de programmation dérivé du Java qui permet un accès
facilité à de nombreuses fonctions, notamment dans le domaine graphique. Il
dispose d'un mode Python lui permettant d'exécuter des fonctions avancées
(telles que la modélisation 3D) depuis un simple code Python.

### pypro_POQB3D.pyde

Ce programme permet d'afficher une modélisation 3D d'un Rubik's Cube et de le
faire tourner selon des mouvements prédéfinis. La première ligne du fichier
contient une chaîne formattée ainsi:

`cb = "<position0>/<position1>/<position2>-<mouvement1>-<mouvement2>"`

Le programme ne contient pas de structure de données pouvant simuler le cube,
il a donc besoin de toutes les positions pour pouvoir afficher le cube comme
prévu. L'environnement Processing étant assez lourd à télécharger, une vidéo
de démonstration est disponible ici: https://youtu.be/iyDtLb1tUVo  

Il est techniquement possible de lier cette modélisation à l'algorithme créé,
mais Processing.py est assez fastidieux et Python n'est pas le langage idéal
pour la création d'une telle application.

### processing_cube_camera.pde

Encore créé avec Processing mais cette fois entièrement en Java, cette ébauche
de programme permet de reconnaître les couleurs d'un Rubik's Cube montré à une
webcam ou autre périphérique de capture vidéo instantanée, en admettant que
l'éclairage soit assez bon. Le programme est capable de détecter les couleurs en temps réel.

Captures d'écran:

![](http://i.imgur.com/xfWZHSA.png)

![](http://i.imgur.com/yuuxBac.png)
