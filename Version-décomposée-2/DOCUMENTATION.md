# Documentation Complète - Bataille Spatiale Navale

##  Vue d'ensemble du projet

**Bataille Navale Spatiale**, connue aussi sous le nom de code Nebula Strike, est un jeu de bataille navale futuriste développé entièrement en Python avec Tkinter comme framework graphique. Ce projet ambitieux offre une expérience de jeu complète avec deux modes de jeu principaux : un mode multijoueur permettant à deux joueurs humains de s'affronter directement, et un mode contre l'ordinateur avec une intelligence artificielle adaptive. Le jeu se distingue par ses mécaniques avancées incluant un système d'animations visuelles fluide, des pouvoirs spéciaux stratégiques, et une ambiance immersive basée sur le thème futuriste de Star Trek.



##  Architecture du Projet

Le projet est organisé de manière modulaire autour de neuf fichiers Python distincts, chacun responsable d'une fonction spécifique. Le fichier principal **main.py** sert de point d'entrée et initialise l'application. **main_menu.py** gère le menu principal avec une animation d'introduction spectaculaire inspirée de Star Wars. Les deux modes de jeu sont implémentés respectivement dans **Humain_VS_Humain.py** et **Humain_VS_Ordinateur.py**, offrant chacun une expérience de jeu distincte. L'interface de placement manuel des bateaux est gérée par **placement.py**, tandis que **Fonction_Bataille.py** contient les fonctions utilitaires essentielles pour les mécaniques de bataille. L'interface utilisateur utilise **Boutons.py** pour la gestion centralisée des éléments interactifs, **utils.py** fournit les configurations globales et les utilitaires, et **Noms.py** stocke toutes les données textuelles dynamiques. Enfin, **main.spec** est le fichier de configuration utilisé pour compiler l'application en exécutable autonome avec PyInstaller.



##  Documentation détaillée des fichiers

### 1. **main.py** - Point d'entrée de l'application

Le fichier **main.py** est extrêmement simple et épuré. Il serve uniquement de point d'entrée à l'application en initialisant une fenêtre Tkinter principale, puis en créant une instance de la classe `MenuPrincipal` pour afficher le menu de sélection. Enfin, il démarre la boucle principale d'événements Tkinter avec `root.mainloop()`, qui reste bloquée jusqu'à la fermeture de l'application. Ce fichier dépend uniquement de `tkinter` et du module `main_menu` pour la classe `MenuPrincipal`. Le flux d'exécution est simple et linéaire : initialisation de Tk, création du menu, puis lancement de la boucle d'événements.



### 2. **main_menu.py** - Menu principal avec animation spectaculaire

Le fichier **main_menu.py** gère l'interface de menu principal et l'animation d'introduction du jeu. La classe `MenuPrincipal` est responsable de tous les éléments du menu, notamment le système d'animation des étoiles de fond, le texte d'introduction inspiré de Star Wars qui monte et disparaît progressivement, et les boutons de sélection des modes de jeu.

En termes d'attributs, la classe stocke la fenêtre principale (`root`), un canvas dédié aux animations (`canvas`), un ensemble de cent vingt étoiles générées aléatoirement (`nb_etoiles` et `etoiles`), et l'identifiant du texte d'introduction (`texte_id`). Les principales méthodes incluent le constructeur qui initialise tous les éléments visuels, une fonction de génération des positions d'étoiles `creer_etoiles()`, une fonction d'animation du scintillement `animer_etoiles()`, et une séquence d'animation du texte d'introduction qui monte graduellement tout en s'estompant. L'utilisateur peut sauter l'introduction en appuyant sur la touche "X".

Ce qui rend ce fichier particulièrement intéressant d'un point de vue technique, c'est la gestion de l'asynchronisme Tkinter pour les animations fluides, le lecteur audio asynchrone qui joue le son Intro.wav sans bloquer l'interface, et l'intégration thématique complète avec le univers futuriste de Star Trek. Le thème visuel combine un fond noir avec des étoiles scintillantes et un texte jaune qui s'estompe progressivement, créant une atmosphère immersive dès le démarrage de l'application.


### 3. **Humain_VS_Humain.py** - Mode deux joueurs humains

Le fichier **Humain_VS_Humain.py** implémente le mode de jeu pour deux joueurs humains qui s'affrontent directement. La classe `BatailleNavaleHumainVSHumain` gère l'intégralité de cette expérience, depuis la préparation des grilles jusqu'à la détermination du gagnant en fin de partie.

La classe stocke les noms des deux joueurs, les deux grilles de jeu de dimension 10×10, les deux flottes correspondantes avec toutes leurs informations (positions, noms, cases touchées), l'indice du joueur dont c'est le tour, des booléens pour contrôler la visibilité des bateaux pour chaque joueur, et un historique détaillé de tous les événements du jeu.

Un aspect particulièrement important de cette classe est sa validation intelligente des grilles fournies. L'initialisation accepte deux formats d'appels distincts : soit passer deux grilles séparément comme `__init__(root, grille1, grille2)`, soit passer une liste contenant les deux grilles comme `__init__(root, [grille1, grille2])`. Avant d'utiliser les grilles, la classe vérifie que chaque grille est bien une liste à deux dimensions de taille 10×10, et lève une exception explicite si le format ne correspond pas. Cette validation est cruciale pour éviter des bugs silencieux qui apparaîtraient seulement après plusieurs tours de jeu.

Une autre fonctionnalité complexe est l'extraction intelligente des positions des bateaux depuis la grille reçue. Le code parcourt la grille complète pour chacun des cinq bateaux attendus, identifier les cases marquées avec la valeur 1 (indiquant un bateau), en s'assurant qu'aucune case n'est assignée à plusieurs bateaux. Les doubles boucles sont synchronisées avec soin pour sortir correctement dès que le bon nombre de cases est trouvé. Cette extraction est délicate car elle doit respecter l'ordre des bateaux et détecter les erreurs de configuration.

Le système de rendu des grilles utilise une architecture en couches pour éviter les problèmes visuels courants. D'abord, un point gris est dessiné pour chaque case pour servir de référence visuelle de base. Ensuite, si une case contient un bateau touché, un rectangle arrondi rouge la couvre. Si une case contient un bateau intact et que l'affichage des bateaux est activé pour ce joueur, un rectangle blanc ou gris la couvre. Enfin, si une case représente un tir manqué, un point blanc opaque la couvre. Cet ordre d'affichage est critique pour que les visuels s'empilent correctement et ne créent pas de confusions visuelles.


### 4. **Humain_VS_Ordinateur.py** - Mode joueur contre l'ordinateur

Le mode Humain versus Ordinateur implémente un système de jeu pour un joueur humain affrontant une intelligence artificielle. La classe `BatailleNavaleHumainVSOrdinateur` gère cet affrontement avec des mécaniques plus avancées que le mode HvH, incluant notamment un système d'IA adaptative et un pouvoir spécial unique : la bombe de zone.

La classe maintient des attributs distincts pour le joueur humain et l'IA : le nom du joueur saisi au démarrage, un nom aléatoire pour l'IA choisi parmi un ensemble de six noms futuristes, les grilles et flottes respectives, et plusieurs booléens gérant le pouvoir spécial de bombe. Un attribut crucial est `tirs_ia_en_attente`, une queue de tirs prioritaires que l'IA utilise pour hunter les bateaux qu'elle a déjà touchés.

L'intelligence artificielle fonctionne selon une stratégie adaptative en deux niveaux. Initialement, l'IA génère une liste de toutes les cases non encore jouées sur la grille du joueur, puis en choisit une aléatoirement. Cependant, dès qu'elle effectue un tir qui touche un bateau, elle ajoute les quatre cases adjacentes (haut, bas, gauche, droite) à sa queue de tirs prioritaires. Lors des tours suivants, elle priorise ces tirs en attente plutôt que de choisir aléatoirement, ce qui crée un comportement intelligent sans nécessiter une véritable intelligence artificielle complexe. Cette stratégie simple mais efficace donne l'impression que l'IA est capable de raisonnement stratégique.

Le pouvoir spécial de bombe de zone est une mécanique importante du mode HvIA. Activable une seule fois par partie avec la touche Z, ce pouvoir permet au joueur de sélectionner une case cible et de frapper une zone 3×3 autour de celle-ci, affectant jusqu'à neuf cases en un seul coup. Cela représente un élément stratégique majeur qui peut transformer le cours de la partie s'il est utilisé judicieusement. Le code gère la validation des limites, s'assurant que les tirs ne sortent pas de la grille, et met à jour la grille pour chaque case touchée dans la zone.


### 5. **placement.py** - Interface interactive de placement des bateaux

Le fichier **placement.py** implémente une interface graphique interactive permettant aux joueurs de placer manuellement leurs bateaux avant de commencer une partie. La classe `PlacementManuel` gère toute la logique de positionnement, offrant une expérience fluide et intuitive avec plusieurs fonctionnalités convenientes.

L'interface stocke la grille en cours de construction, la liste des cinq bateaux à placer avec leurs tailles respectives, une liste des bateaux déjà placés avec leurs positions et couleurs, l'indice du bateau actuellement en cours de placement, une orientation booléenne (true pour vertical, false pour horizontal), et une fonction de rappel (callback) à invoquer une fois le placement terminé.

La détection des interactions clavier utilise une technique subtile mais efficace basée sur les bitmasks. Lorsqu'un événement souris est déclenché, l'attribut `event.state` contient un bitmask de tous les modifieurs actuellement appuyés. Pour détecter si la touche Shift est appuyée, le code effectue une opération AND binaire entre `event.state` et la constante `0x0001`, qui représente le bit de Shift. Si le résultat est non zéro, cela signifie que Shift était appuyée au moment du clic. Cette approche est bien plus fiable que des vérifications de chaînes de caractères et reflète le fonctionnement bas niveau du système de fenêtrage X11 et Windows.

L'ordre des vérifications lors du placement d'un bateau est critique pour la performance et la correction. Le code d'abord vérifie que le bateau ne dépasse pas les limites de la grille (une opération rapide O(n) sur les n cases du bateau). Ensuite seulement, il vérifie qu'aucune des positions n'est déjà occupée par un autre bateau (une opération plus coûteuse qui parcourt la grille). Cette séquence est importante car une vérification d'accès array hors limites créerait une exception, tandis que vérifier les collisions d'abord pourrait causer des accès invalides mémoire.


### 6. **Fonction_Bataille.py** - Fonctions utilitaires pour la mécanique de jeu

Le fichier **Fonction_Bataille.py** contient un ensemble de fonctions utilitaires critiques pour les mécaniques fondamentales du jeu. Ces fonctions gèrent le rendu graphique avancé, la gestion des grilles, et les vérifications d'état du jeu.

La fonction la plus complexe est probablement `rectangle_arrondi()`, qui dessine des rectangles aux coins arrondis sur le canvas Tkinter. Cette tâche apparemment simple est compliquée par les limitations de Tkinter, qui n'offre pas nativement de support pour les rectangles avec coins arrondis. La solution utilise une technique élégante en trois passes. D'abord, on dessine un contour épais de la couleur du fond pour masquer les chevauchements qui apparaîtraient autrement. Ensuite, on dessine le remplissage réel combinant des rectangles et des ovales pour créer la forme arrondie. Enfin, on dessine le contour visible final avec des lignes fines et des arcs. Cette approche en trois passes est un exemple classique de technique de rendu graphique pour contourner les limitations d'une API.

Le fichier contient également des fonctions de vérification d'état du jeu, notamment `case_deja_jouee()` qui détecte si une case a déjà été jouée (marquée comme touée ou ratée), `tous_coules()` qui vérifie si tous les bateaux d'une flotte sont entièrement coulés, et `trouver_bateau()` qui localise quel bateau occupe une position donnée. La fonction `tous_coules()` est particulièrement instructive car elle utilise la comparaison de sets pour déterminer l'égalité : elle compare l'ensemble de toutes les positions d'un bateau avec l'ensemble de ses cases touchées. Si ces deux sets sont identiques, le bateau est entièrement coulé. Cette approche est bien plus efficace qu'une boucle explicite.

### 7. **Boutons.py** - Création des éléments interactifs

Le fichier **Boutons.py** centralise la création et la gestion des éléments interactifs de l'interface utilisateur. Il fournit des fonctions pour créer les boutons, ouvrir les dialogues de règles, et gérer les confirmations de quitter.

Ce fichier utilise les fenêtres modales Tkinter (`tk.Toplevel`) pour créer des dialogues qui bloquent l'interaction avec la fenêtre principale jusqu'à leur fermeture. Les dialogues utilisent `grab_set()` pour empêcher les clics sur la fenêtre parent, et `wait_window()` pour mettre le programme en attente jusqu'à la fermeture du dialogue. Chaque dialogue inclut des sons appropriés pour renforcer le feedback utilisateur, et pour les règles du jeu, un widget Text avec une scrollbar est utilisé pour permettre de lire un contenu textuel long.

### 8. **utils.py** - Configuration globale et utilitaires

Le fichier **utils.py** centralise tous les éléments de configuration et les fonctions utilitaires globales. Il contient les définitions des cinq bateaux avec leurs tailles (USS Enterprise de 5 cases, USS Defiant de 4 cases, etc.), et un dictionnaire complet des couleurs utilisées dans le thème graphique. Les couleurs suivent un schéma cohérent inspiré par Star Trek, avec un fond noir (#000000), des accents jaunes (#ffd60a) et rouges (#ef233c) pour signaler les états importants.

Une fonction critique dans ce fichier est `resource_path()`, qui gère les chemins d'accès aux fichiers ressources de manière compatible avec PyInstaller. Lors de l'exécution normale en mode développement, la fonction retourne simplement le chemin relatif fourni. Cependant, quand le code est compilé avec PyInstaller, cet outil crée une archive temporary et définit `sys._MEIPASS` pour pointer vers ce répertoire. La fonction détecte la présence de cet attribut et reconstruit le chemin approprié. Sans cette gestion, tous les fichiers audio et ressources seraient introuvables dans l'exécutable compilé.

Le fichier contient également `placer_bateau_aleatoire()`, qui génère des positions aléatoires pour placer un bateau sur une grille sans chevauchement. Cette fonction itère jusqu'à cinq cents fois au maximum, essayant aléatoirement différentes orientations et positions jusqu'à trouver un emplacement valide. Cette limite de tentatives évite les boucles infinies si la grille devient trop encombragée.

### 9. **Noms.py** - Données textuelles dynamiques

Le fichier **Noms.py** stocke toutes les données textuelles dynamiques du jeu, particulièrement les phrases générées aléatoirement pour le mode HvIA. Ce fichier contient six noms d'IA différents comme « General Chang », « Sybok », et « Section 31 », choisis aléatoirement au démarrage d'une partie. Il contient aussi quarante-six phrases ou plus d'encouragement qui s'affichent après que l'IA manque un tir, et des phrases de réaction pour divers événements du jeu. Tous ces textes sont basés sur le thème Star Trek, renforçant l'immersion dans l'univers futuriste du jeu. Les phrases sont générées aléatoirement à chaque événement pertinent, fournissant de la variété et de la rejouabilité.


##  Flux de jeu et expérience utilisateur

Le jeu offre deux chemins distincts selon le mode choisi par le joueur. Dans le mode Humain versus Humain, après avoir sélectionné l'option correspondante depuis le menu principal, chaque joueur accède à son interface de placement personnel où il positionne ses cinq bateaux selon ses préférences stratégiques. Une fois le placement validé pour les deux joueurs, le jeu démarre avec la demande des noms de chaque joueur et l'affichage des deux grilles côte à côte. Les joueurs alternent les tirs, chacun sélectionnant une case de la grille adverse. Les animations et sons se déclenchent à chaque événement, et l'historique affiche tous les événements de la partie. La partie se termine quand tous les bateaux d'un joueur sont coulés.

Le mode Humain versus Ordinateur suit un flux similaire pour le placement, avec le joueur humain sélectionnant manuellement ses positions tandis que l'ordinateur génère aléatoirement ses bateaux. Une fois la partie commencée, le joueur tire sur la grille de l'IA, puis l'ordinateur effectue son propre tir en utilisant sa stratégie adaptative. Ce mode offre des mécaniques supplémentaires comme le pouvoir de bombe de zone et les dialogues dynamiques qui changent selon le contexte de la partie.


##  Système visuel et rendu graphique

Le jeu utilise un système visuel fondé sur un canvas Tkinter unique pour chaque grille. Les dimensions du canvas s'adaptent dynamiquement à la taille de la fenêtre, et le système de rendu recalcule les paramètres d'affichage à chaque redimensionnement. Chaque grille est divisée en cent cases de 10 par 10 cellules, et chaque cellule peut être dans l'un de quatre états visuels distincts : l'eau non jouée (point gris petit), un bateau intact (rectangle blanc opaque si visible), un bateau touché (rectangle rouge), ou un tir manqué (point blanc).

Une subtilité importante du système est que le dimensionnement du canvas en Tkinter n'est pas instantané. Au démarrage de l'application, la méthode `winfo_width()` retourne souvent 1 pixel parce que Tkinter n'a pas encore calculé les dimensions réelles de l'élément. Pour contourner ce problème, le code utilise une fonction spéciale `redessiner_grilles_safe()` qui boucle avec `root.after()` jusqu'à ce que les dimensions soient supérieures à cinq pixels, puis procède au rendu réel. Sans cette attente, les calculs de cellule_size produiraient des divisions par zéro ou des grilles hors limites.


##  Système audio et feedback sensoriel

Le jeu intègre six fichiers audio distincts qui renforcent l'immersion et le feedback utilisateur. L'introduction Star Wars joue au démarrage du menu, l'ouverture des règles déclenche un son spécifique, et chaque interaction de jeu émet un son : tir manqué produit un « splash » informatif, bateau touché génère une explosion, et bateau coulé crée un effet sonore dramatique. Un dernier son s'ajoute à la tentative de quitter, servant comme confirmation auditive.

Tous les sons sont lus de manière asynchrone avec le drapeau `SND_ASYNC` de winsound, ce qui signifie que la lecture du son ne bloque pas l'interface. Sans cet drapeau, l'application se figerait jusqu'à la fin du son, créant une mauvaise expérience utilisateur. De plus, toutes les opérations audio sont encapsulées dans des blocs try-except pour gérer gracieusement les situations où les fichiers audio manqueraient en mode développement. La fonction `resource_path()` est utilisée pour tous les appels audio, garantissant que les fichiers sont trouvés à la fois en mode développement et dans l'exécutable compilé PyInstaller.


##  Contrôles et raccourcis clavier

L'interface propose plusieurs raccourcis clavier pour améliorer l'expérience utilisateur. Dans le menu principal, appuyer sur "X" (minuscule ou majuscule) saute l'introduction Star Wars, permettant aux utilisateurs impatients d'accéder rapidement au menu de sélection du mode. Pendant la phase de placement manuel, la touche "R" et le clic droit togglent l'orientation du bateau actuel entre horizontal et vertical. Pour supprimer accidentellement un bateau mal placé, l'utilisateur maintient Shift et clique sur une case contenant le bateau à supprimer. En mode Humain versus Ordinateur, la touche "Z" active le pouvoir spécial de bombe de zone, si celui-ci n'a pas déjà été utilisé dans la partie.


##  Architecture de l'intelligence artificielle

L'intelligence artificielle du mode HvIA fonctionne selon un modèle hiérarchique de sélection de cible. Au démarrage, l'IA génère une liste de toutes les cases non encore jouées et en choisit une aléatoirement. Cette approche basale crée un défi raisonnable pour les joueurs débutants. Cependant, dès qu'un tir de l'IA touche un bateau, le comportement change fondamentalement. L'IA ajoute les quatre cases orthogonalement adjacentes (haut, bas, gauche, droite) à une file de priorité appelée `tirs_ia_en_attente`. Lors des tours subsequents, l'IA priorise systématiquement ces tirs en attente, recherchant à exterminer complètement le bateau touché avant de revenir à la sélection aléatoire.

Cette stratégie crée une illusion efficace d'intelligence : l'IA semble capable de raisonnement tactique et de patience stratégique, alors qu'en réalité elle implémente simplement une queue de priorité bien gérée. Le comportement est prédictible pour les joueurs expérimentés mais suffisamment efficace pour créer du challenge. L'implémentation est intentionnellement simple pour éviter une sur-complexité inutile tout en maintenant une expérience de jeu engageante.


##  Caractéristiques et mécanique principales

Le projet Nebula Strike offre une expérience de jeu complète avec plusieurs couches de fonctionnalités soigneusement intégrées. L'interface graphique est moderne et réactive, utilisant un thème noir avec des accents jaunes et rouges inspirés de Star Trek, accompagnée d'animations fluides qui rendent les interactions visuellement satisfaisantes. Le jeu propose deux modes de jeu distincts permettant à deux joueurs humains de s'affronter directement ou à un joueur de défier l'ordinateur avec une IA adaptative.

Le système de placement manuel des bateaux offre une interface interactive complète où les joueurs contrôlent précisément la position et l'orientation de chacun de leurs cinq vaisseaux. Le moteur de rendu utilise une technique en couches pour afficher correctement les différents états des cases de grille, garantissant une clarté visuelle même avec des grilles complexes. En mode Humain versus Ordinateur, un système de son immersif fournit un feedback auditif pour chaque événement majeur, et les dialogues générés aléatoirement basés sur Star Trek créent une ambiance narrée et engageante.

Le pouvoir spécial de bombe de zone en mode HvIA ajoute une dimension stratégique supplémentaire, forçant les joueurs à décider s'ils veulent économiser ce pouvoir pour les moments critiques ou l'utiliser tôt dans la partie. L'historique détaillé de tous les événements de jeu permettant une revue complète de la partie, et le système de redimensionnement dynamique garantissant que le jeu s'adapte à n'importe quelle taille de fenêtre.


##  Dépendances du projet

Le projet repose sur un ensemble minimaliste de dépendances, la plupart étant incluses nativement avec Python. Tkinter fournit l'intégralité du framework graphique et vient inclus avec la plupart des distributions Python sur Windows, macOS, et Linux. Le module winsound offre la fonctionnalité audio sur Windows, permettant la lecture asynchrone de fichiers WAV sans blocage de l'interface. Les modules standard random, math, sys, et os fournissent les utilitaires nécessaires pour la génération aléatoire, les opérations mathématiques, et la gestion du système de fichiers.

Cette sélection minimaliste de dépendances contribue à la portabilité du projet et réduit les risques de compatibilité future. Aucune dépendance tiers n'est nécessaire au-delà de ce que Python fournit nativement, ce qui signifie que le projet peut être exécuté sur pratiquement n'importe quelle installation Python moderne sans installations supplémentaires.


##  Guide de démarrage rapide

Lancer le projet est straightforward. Après avoir cloné ou téléchargé l'archive du projet, naviguez vers le répertoire racine dans un terminal. Assurez-vous que Python 3.7 ou une version plus récente est installée en exécutant `python --version`. Lancez simplement `python main.py` pour démarrer l'application. L'interface démarrera avec l'animation d'introduction Star Wars, que vous pouvez sauter en appuyant sur la touche X.

Pour personnaliser le jeu, les principaux fichiers à modifier sont identifiés facilement. Pour changer les bateaux ou leurs tailles, éditez `utils.py` en modifiant la constante `NOMS_BATEAUX`. Pour ajouter des dialogues ou des phrases aléatoires supplémentaires, augmentez les listes dans `Noms.py`. Pour ajuster les couleurs du thème, modifiez le dictionnaire `COULEURS` dans `utils.py`. Pour modifier le comportement de l'IA ou sa difficulté, éditez les fonctions `tour_ia()` et la logique de la queue `tirs_ia_en_attente` dans `Humain_VS_Ordinateur.py`.


##  Modifications avancées et personnalisations

Le système de grille peut être modifié en changeant la constante de taille de 10 à toute autre valeur, bien que cela nécessite une synchronisation avec les tailles des bateaux. Pour ajouter de nouveaux bateaux ou en supprimer, modifiez simplement la liste `NOMS_BATEAUX` dans `utils.py` et le reste du code s'adaptera automatiquement. Pour augmenter la puissance de la bombe de zone, changez la plage des boucles `for dl in (-1, 0, 1)` à une plage plus large comme `range(-2, 3)` pour une zone 5×5.

Pour ajuster la difficulté de l'IA, réduisez le pourcentage de temps où l'IA priorise la queue de tirs en attente, ou implémentez une stratégie de recherche en croix plutôt que simplement aléatoire. Les animations peuvent être rendues plus rapides ou plus lentes en ajustant les paramètres de délai dans les appels `root.after()`, et leur taille peut être modifiée en changeant les rayons et les paramètres géométriques. Les sons peuvent être remplacés en fournissant des fichiers WAV portant les mêmes noms dans le répertoire du projet.


## Patterns Python et bonnes pratiques

Le code utilise plusieurs patterns Python avancés qui méritent d'être compris. Les list comprehensions imbriquées génèrent efficacement des ensembles de données complexes en une seule ligne, réduisant la verbosité tout en restant lisible. L'unpacking de tuples dans les boucles rend le code plus intuitif pour manipuler des données structurées. Les lambda avec arguments par défaut capturent correctement les valeurs au moment de la création plutôt que du l'appel, évitant les pièges courants de fermeture. L'utilisation de sets pour les comparaisons d'égalité est bien plus performante que les boucles imbriquées pour vérifier si deux collections contiennent les mêmes éléments.

Le pattern modal avec `grab_set()` et `wait_window()` démontre comment créer des dialogues qui bloquent l'interaction avec la fenêtre parente tout en maintenant la boucle d'événements active. L'utilisation de bitmasks pour détecter les modifieurs clavier est plus fiable que les vérifications de chaînes et reflète le fonctionnement bas-niveau du système. Le stockage de métadonnées de rendu directement sur les objets canvas (comme `canvas.cell_size` et `canvas.offset_x`) est un pattern Python courant pour étendre les objets sans surcharger.


##  Statistiques et performances

Le projet compte approximativement 1500 lignes de code Python distribuées sur neuf fichiers, avec trois classes principales gérant les modes de jeu. Le système supporte cinq bateaux de tailles variées sur une grille 10×10 générant 100 cases individuelles. L'IA peut générer jusqu'à 46 phrases dynamiques différentes, et les six noms d'IA offrent une variété suffisante pour créer une sensation de rejouabilité. Le système graphique redessine complètement les grilles à chaque interaction, ce qui reste performant pour des grilles de cette taille en Tkinter.

Les durées de jeu varient significativement selon le mode et les joueurs. En mode Humain versus Humain, une partie typique dure entre cinq et dix minutes selon l'expérience des joueurs et leur style de jeu. En mode contre l'ordinateur, une partie avec une IA aléatoire dure approximativement trois à cinq minutes, tandis qu'une IA intelligente crée un défi qui prolonge les parties à cinq à huit minutes en moyenne.


##  Concepts implémentés

Le projet implémente plusieurs concepts avancés de programmation. Le double buffering implicite de Tkinter évite le clignotement en regroupant tous les changements au canvas et en les appliquant en une seule mise à jour d'écran. Le pattern asynchrone avec `root.after()` crée des animations fluides sans bloquer la boucle d'événements, ce qui est crucial pour une interface graphique réactive. Le système en couches pour le rendu du canvas démontre comment surmonter les limitations d'une API graphique en utilisant des techniques créatives.

Le stockage d'états de jeu dans des structures de dictionnaires imbriquées offre une flexibilité à la fois pour les données et les manipulations. L'utilisation de sets pour les opérations d'égalité de collections montre comment exploiter les caractéristiques mathématiques des structures de données pour optimiser les performances. Le système de gestion des ressources avec `resource_path()` et la détection de `sys._MEIPASS` démontre comment créer du code portable entre le mode développement et les exécutables compilés.

##  Compilation et distribution avec PyInstaller

Le projet inclut un fichier `main.spec` pré-configuré pour la compilation avec PyInstaller, un outil qui transforme les scripts Python en exécutables autonomes. Pour compiler le jeu en exécutable, exécutez simplement la commande `pyinstaller main.spec` à partir du répertoire racine du projet. PyInstaller lira la configuration du fichier spec, empaquera tous les dépendances Python nécessaires, inclura les fichiers ressources audio, et générера un dossier `dist/` contenant l'exécutable final.

Ce processus résout tous les chemins de ressources automatiquement en définissant `sys._MEIPASS` de manière appropriée, signifiant que la fonction `resource_path()` fonctionne correctement dans l'exécutable compilé. L'exécutable résultant est véritablement autonome et peut être distribué à des utilisateurs n'ayant pas Python installé. La première exécution peut être légèrement lente car Windows analyse l'exécutable pour la sécurité, mais les exécutions suivantes sont rapides. Pour accélérer les démarrages futurs, PyInstaller crée également un cache bytecode optimisé.


##  Notes de développement et architecture

La gestion des grilles suit une convention cohérente : les grilles sont des listes Python imbriquées de taille 10×10, avec les indices utilisés comme `grille[ligne][colonne]`. Les bateaux sont stockés comme des dictionnaires contenant le nom, la taille, une liste de positions en tuples, et un set des positions touchées pour faciliter les comparaisons. Cette structure permet une flexible représentation tout en maintenant les performances pour les opérations courantes.

Le système de validation des grilles en entrée dans la classe `BatailleNavaleHumainVSHumain` démontre une approche défensive à la validation des données : plutôt que de supposer que l'entrée est correcte, le code vérifie explicitement que chaque grille a les bonnes dimensions et lance des exceptions détaillées si ce n'est pas le cas. Cette approche évite les bugs silencieux qui apparaîtraient seulement plusieurs tours après l'initialisation.

Le redimensionnement dynamique utilise une approche robuste en trois étapes. D'abord, `redessiner_grilles_safe()` boucle jusqu'à ce que Tkinter ait dimensionné le canvas. Deuxièmement, `redessiner_grilles()` recalcule les paramètres de rendu basés sur les dimensions actuelles. Troisièmement, les paramètres sont stockés sur le canvas lui-même pour éviter les recalculs à chaque clic. Cette approche multi-niveaux garantit que le système est robuste même face aux subtilités du timing d'asynchronisme de Tkinter.

Les animations utilisent un pattern de callback recursive avec `root.after()` plutôt que des boucles blocking, permettant à la boucle d'événements Tkinter de continuer à traiter les entrées utilisateur. Les closures capturent l'état de l'animation (numéro de frame, positions intermédiaires) sans avoir besoin d'attributs d'instance séparés pour chaque animation en cours.

## Optimisations possibles pour le futur

Bien que le code actuel soit performant pour la portée du projet, plusieurs améliorations futures pourraient être considérées. L'utilisation de `canvas.itemconfig()` pour mettre à jour les propriétés d'objets existants plutôt que de supprimer et redessiner complètement pourrait réduire le flickering et améliorer les performances. L'implémentation d'un vrai système de cache pour les métriques de rendu pourrait réduire les calculs redondants. L'ajout de support pour les parties réseau permettrait aux joueurs à distance de se faire concurrence. Le remplacement de Tkinter par un framework graphique plus moderne pourrait offrir de meilleures animations et des graphiques plus riches.

L'optimisation du code IA avec des algorithmes de pathfinding avancés créerait un défi plus intéressant pour les joueurs expérimentés. L'ajout d'un système de niveaux de difficulté ajousteble permettrait aux joueurs de progressivement augmenter le défi. L'implémentation d'un éditeur de thème permettrait la personnalisation complète des couleurs et de l'apparence. L'enregistrement et la lecture de parties permettrait aux joueurs de rejouer leurs matchs mémorables.


##  Checklist pour la production et le déploiement

Avant de publier le jeu ou de le distribuer à des utilisateurs, plusieurs vérifications finales doivent être effectuées. Confirmez que tous les six fichiers audio WAV sont présents dans le répertoire du projet avec les bonnes noms de fichiers. Validez le code Python avec `python -m py_compile *.py` pour capturer les erreurs de syntaxe. Testez complètement le mode Humain versus Humain avec deux joueurs réels, vérifiant que toutes les transitions d'état fonctionnent correctement. Testez le mode Humain versus Ordinateur jusqu'au bout, en jouant quelques parties pour vérifier l'équilibre de difficulté de l'IA.

Vérifiez que le raccourci X saute bien l'introduction Star Wars. Testez le pouvoir de bombe de zone en mode HvIA pour vérifier son fonctionnement et son équilibre. Testez le redimensionnement de fenêtre pour vous assurer que l'interface s'adapte correctement à différentes tailles d'écran. Compilez avec PyInstaller et testez l'exécutable résultant sur une machine sans Python pour vérifier que toutes les dépendances sont incluses correctement. Vérifiez que les sons jouent dans l'exécutable compilé, pas seulement en mode développement. Documentez tous les raccourcis clavier et les contrôles dans le fichier d'aide utilisateur.

Pour commencer à développer sur ce projet, commencez par cloner ou télécharger l'archive. Naviguez vers le répertoire racine Version-décomposée-2 et vérifiez que Python 3.1 ou plus récent est installé. Lancez le jeu simplement avec `python main.py` pour vérifier que tout fonctionne correctement. Vous devriez voir l'introduction Star Wars, que vous pouvez sauter avec X, puis le menu de sélection du mode de jeu.

Les fichiers critiques à comprendre pour les modifications courantes sont clairement identifiés. Pour ajuster les bateaux du jeu, éditez la constante `NOMS_BATEAUX` dans `utils.py` qui stocke le nom et la taille de chaque vaisseau. Pour enrichir les dialogues du jeu, augmentez les listes de phrases dans `Noms.py`, particulièrement `A_TOI_DE_JOUER` et `A_TOI_DE_RATER` qui fournissent le feedback contextuel pendant les parties. Pour personnaliser l'apparence visuelle, modifiez le dictionnaire `COULEURS` dans `utils.py` en changeant les codes hexadécimaux pour chaque élément. Pour modifier le comportement de l'intelligence artificielle, examinez et éditez les fonctions `tour_ia()` et la logique de gestion de `tirs_ia_en_attente` dans `Humain_VS_Ordinateur.py`.

## Problèmes rencontrés et solutions
### Problème : Rendu en couches (grille)

Le système de rendu des grilles a présenté des défis subtils mais critiques. Le code doit dessiner les points de base (eau) en premier, puis ajouter les rectangles arondis rouges pour les cases touchées, puis les rectangles pour les bateaux intacts (si leur affichage est activé), et finalement les points blancs pour les tirs ratés. Cet ordre d'affichage n'est pas arbitraire mais fondamental pour que les visuels s'empilent correctement.

Le problème initial était que les points gris utilisés pour représenter l'eau non jouée étaient invisibles sur le fond noir de la grille. La solution consistait à utiliser une couleur distincte comme `#38383b` (gris sombre) au lieu du noir pur, ce qui crée un contraste suffisant pour que les points restent visibles. Cependant, une fois cette correction appliquée, un nouveau problème apparut : les rectangles rouges pour les bateaux touchés étaient dessinés sous les points gris plutôt que par-dessus. Cela créait une confusion visuelle où les touches n'étaient pas clairement identifiables.

La vraie solution requérait une refonte complète du système de rendu en une technique à trois passes. D'abord, Tkinter dessine une première couche de contours épais de la couleur du fond pour masquer les chevauchements désordonnés qui autrement apparaîtraient. Deuxièmement, elle dessine le remplissage réel en combinant des rectangles et des ovales aux angles pour créer la forme arrondie. Troisièmement, elle dessine les contours visibles finals avec des lignes fines. Sans cette approche en trois passes, les lignes de contour se chevaucheraient de manière désordonnée et l'alignement semblerait incorrec. Après environ huit tentatives pour trouver la bonne combinaison de formes et de positions, le rendu était finalement correct mais extrêmement fragile : tout petit changement à l'ordre des appels ou aux positions cassait tout.

### Problème 2 : Conversion souris → indices grille

La conversion des coordonnées absolues en pixels de la souris vers les indices logiques de la grille s'est avérée plus complexe que prévu, principalement en raison des pièges subtils liés à l'asynchronisme de Tkinter. Le canvas doit être dimensionné correctement, centré sur l'écran pour permettre les animations en mode responsive, et les offsets de ce centrage doivent être stockés quelque part pour l'utilisation ultérieure lors du clic.

La chaîne de problèmes commençait au démarrage : l'attribut `canvas.offset_x` n'existait pas parce que la fonction de dimensionnement n'avait pas encore été appelée. Cliquer sur le canvas avant qu'il ne soit dimensionné générait une exception `AttributeError` ou une division par une valeur incorrecte. La deuxième difficulté était que les clics en dehors de la grille devaient être gérés gracieusement plutôt que de crasher avec une `IndexError`. La solution incluait la vérification que les indices calculés restaient dans la plage [0, 10[ avant d'accéder au tableau.

La confusion entre les coordonnées pixel et les indices de grille était une source constant d'erreurs. La formule correcte était `indice = int((pixel - offset) // cell_size)`, où `int()` tronquait plutôt que d'arrondir. Un détail critique était l'utilisation de `int()` au lieu de `round()`, car arrondir causerait des clics au bord exact de la grille (par exemple, au pixel 200 sur une grille de 10×200) de mapper vers l'indice 10 au lieu de 9, ce qui dépasserait les limites. La résolution finale nécessitait cinq heures de débogage, en grande partie parce qu'il y avait un bug secondaire dans la fonction `redessiner_grilles()` qui ne stockait pas les offsets sur le canvas, créant une situation où les offsets seraient recalculés à chaque clic avec potentiellement des valeurs différentes.

### Problème 3 : Système IA avec file d'attente

L'IA de Bataille Navale devait utiliser une file d'attente de tirs en attente pour poursuivre les navires qu'elle détectait, plutôt que de simplement choisir des cases aléatoires. Cependant, la gestion de cette file présentait plusieurs pièges qui affectaient à la fois l'équité du jeu et ses performances. 

La première difficulté était une confusion simple mais coûteuse sur la mécanique de la liste Python. Utiliser `pop()` retirait du dernier élément ajouté (mode LIFO ou pile), alors que la logique voulait une stratégie FIFO (file d'attente). Cela signifiait que les premiers tirs ciblant les navires détectés n'étaient jamais atteints ; la file s'accumulait de façon chaotique. La solution était simplement d'utiliser `pop(0)` pour une vraie file d'attente. Cependant, cela créait un deuxième problème : des doublons s'accumulaient dans la file parce que les quatre voisins d'une case touchée étaient ajoutés sans vérifier si l'un d'entre eux était déjà là. La file explosait à des centaines de cases, causant des calculs inutiles.

Le troisième problème était l'équilibre des jeux. Une fois que ces bugs étaient corrigés, l'IA devint pratiquement invincible ; elle trouvait et coulait les navires avec une efficacité presque théorique. Cela ruinait l'expérience pour les joueurs humains. La solution incluait réduire la probabilité d'utiliser la file d'attente à 80% du temps, ce qui signifiait que 20% du temps, l'IA revenaît à un choix aléatoire pour une certaine imprédictibilité. Enfin, générer la liste complète de coups non joués à chaque tour était coûteux en CPU, car cela s'exécutait comme une compréhension de liste O(100) à chaque tour. La solution finale maintenait une liste mise à jour increméntalement, supprimant les cases au fur et à mesure qu'elles étaient jouées plutôt que de la recalculer.


### Problème 4 : Bombe de zone avec validation

Code difficile :
```python
def tirer_bombe_zone(self, l, c):
    self.bombe_en_cours = False
    self.bombe_disponible = False
    
    cibles = []
    for dl in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nl, nc = l + dl, c + dc
            if 0 <= nl < self.taille and 0 <= nc < self.taille:
                cibles.append((nl, nc))
    
    for nl, nc in cibles:
        if self.grille_ia[nl][nc] not in (2, 3):
            self.jouer_tir(self.grille_ia, self.flotte_ia, nl, nc)
```

La bombe spéciale permettait un tir qui touchait toutes les cases dans une zone 3×3 autour du point d'impact. Cela semblait simple en théorie, mais en pratique, la puissance du pouvoir cassait complètement l'équilibre du jeu. La boucle double qui implémentait le tir de zone incluait accidentellement la case centrale deux fois ; techniquement une redondance sans importance puisque la même case ne pouvait pas être frappée deux fois (elle était déjà marquée après le premier tir), mais c'était un indice d'une conception chaotique.

Le vrai problème était la taille de la zone. Une zone 3×3 signifiait que neuf cases étaient touchées en un seul coup, ce qui était absolument dévastatrice. Un navire de taille trois (le sous-marin) pouvait être coulé instantanément même si l'utilisateur cliquait n'importe où à proximité. Cela rendait la bombe complètement game-breaking, transformant chaque partie en une compétition pour voir qui pouvait obtenir la bombe en premier. La solution incluait réduire la zone à 2×2 (quatre cases) ou implémenter une validation d'impact qui limitait les dégâts à seulement certains types de cibles.

Un deuxième problème était la découverte du pouvoir lui-même. Le joueur n'avait aucune indication visuelle qu'il avait déverrouillé une bombe de zone lors du placement des navires. La solution était d'ajouter un bouton dédié et un label expliquant le pouvoir spécial. Enfin, l'animation de la bombe n'était pas distinguée ; le joueur voyait simplement neuf explosions apparaître simultanément, ce qui était visuellement confus. Ajouter une animation d'impact différente ou une onde de choc centrale rendait l'effet plus spectaculaire et plus compréhensible.

### Problème 5 : Dimensionnement du canvas

Le canvas de Tkinter présentait une race condition subtile liée à l'asynchronisme du framework. Au démarrage du jeu, la fenêtre n'avait pas encore été fully dimensionnée par le gestionnaire de fenêtres du système d'exploitation, ce qui signifiait que `canvas.winfo_width()` retournait une valeur inutile (souvent 1) plutôt que les dimensions réelles. Si le code tentait de calculer la taille des cellules immédiatement, il diviserait par un nombre trop petit ou générerait une division par zéro si la taille calculée était zéro.

La solution était d'implémenter une boucle de vérification qui attendait que le canvas soit réellement dimensionné. La fonction `redessiner_grilles_safe()` vérifiait si la largeur était inférieure à cinq pixels ; si c'était le cas, elle se rappelait elle-même dans 20 millisecondes, créant une boucle de polling gentille jusqu'à ce que Tkinter ait dimensionné la fenêtre. Une fois que le canvas avait une taille raisonnable, la vraie fonction de redessinage s'exécutait. Comme fallback de sécurité, si même `winfo_reqwidth()` retournait des valeurs insignifiantes, le code utilisait une dimension par défaut de 400×400 pixels.

Un problème connexe était la redondance des appels de redessinage. Chaque événement `<Configure>` (redimensionnement de fenêtre) déclenchait une redraw complète, ce qui causait du lag si l'utilisateur redimensionnait rapidement la fenêtre. La solution était d'utiliser un throttle avec `root.after()` plutôt que de redessiner de manière synchrone. Après chaque appel de redessinage, un timer attendait quelques millisecondes avant de permettre un autre redessinage, réduisant considérablement la consommation de CPU pendant les redimensionnements fluides.

### Problème 6 : Gestion des animations sans bloquer l'UI

Les animations des tirs et des explosions devaient s'exécuter sur plusieurs frames sans geler l'interface utilisateur. L'approche naïve était d'utiliser `time.sleep()` pour attendre entre les frames d'animation, ce qui était catastrophique pour l'UX ; pendant qu'une animation de trois secondes se jouait, l'application entière était non-réactive. L'événement de souris ne serait pas traité, les touches clavier seraient ignorées, et le jeu semblerait gelé. La solution correcte était d'utiliser le système de callback planifiés de Tkinter avec `root.after()`, qui permettait à la boucle d'événements de continuer entre les frames d'animation.

Cependant, utiliser `root.after()` creusait un piège subtil concernant les fermetures de variables. Chaque appel à la fonction étape d'animation devrait incrémenter un compteur `i` pour suivre le stade de l'animation. Si le code tentait simplement de modifier `i` directement, la variable changerait dans tous les closures précédents, créant un chaos chronologique. La solution était de faire de `i` un paramètre par défaut dans la fonction étape, ce qui capturait sa valeur à ce moment-là plutôt que de la chercher dans la portée externe.

Un autre défi était les couleurs. Tkinter ne supportait pas les valeurs alpha (transparence) dans les couleurs hexadécimales, donc pour créer l'effet d'une explosion s'estompant, le code devait approximer en variant la valeur hex de la couleur elle-même. Une couleur s'estomperait en devenant progressivement plus grise ou plus sombre. Enfin, il était facile de tenter de modifier un objet canvas après qu'il n'existe plus ; le code devait vérifier que l'objet n'avait pas déjà été supprimé avec `canvas.delete()` avant de tenter d'appeler `canvas.itemconfig()` sur lui.

### Problème 7 : Modération des touches clavier (Shift+clic)

Code difficile :
```python
def placer_ou_supprimer(self, event):
    if not hasattr(self, "cell_size") or self.cell_size == 0:
        return
    c = int(event.x // self.cell_size)
    l = int(event.y // self.cell_size)
    
    if event.state & 0x0001:  # Shift + clic gauche
        self.supprimer_bateau(l, c)
```

Déterminer si l'utilisateur tenait Shift tout en cliquant semblait simple sur le papier mais révélait rapidement comment Tkinter codait les modificateurs. L'approche naïve était de vérifier `if "Shift" in event.keysym`, mais cela ne fonctionnait que pour les événements clavier, pas les clics. Pour les événements de souris, Tkinter stockait les modificateurs dans `event.state` en tant que bitmask, où chaque bit représentait un modificateur différent.

Le problème était que la valeur de ce bitmask n'était pas intuitif ou automatique. Shift était bit 0 (valeur 0x0001), Ctrl était bit 2 (valeur 0x0004), Alt était différent selon la plateforme. La documentation était rare et les développeurs finissaient souvent à copier-coller des valeurs magiques sans comprendre ce qu'elles signifiaient. Pour vérifier Shift, le code utilisait `if event.state & 0x0001:`, qui testait si le bit 0 était activé en utilisant une opération ET au niveau des bits. Un test similaire requérait une compréhension de la manipulation des bits en Python.

Un deuxième piège était oublier les offsets du canvas. Lors de la gestion du clic, le code devait soustraire `canvas.offset_x` et `canvas.offset_y` des coordonnées de la souris, sinon le calcul des indices de grille serait décalé. C'était facile à oublier, surtout dans une version plus simple du code où les offsets n'existaient pas du tout. La solution était d'ajouter une vérification pour voir si les offsets existaient en tant qu'attributs du canvas, sinon utiliser 0. Enfin, bien que le code utilisait `<Button-1>` pour le clic gauche, les clics droits utilisaient `<Button-3>` (et même les clics molette utilisaient `<Button-2>`), ce qui était encore moins intuitif. Lier les deux événements séparement plutôt que d'essayer de les différencier dans un seul handler était plus clair et moins sujet aux erreurs.


##  Étapes de réalisation du projet

### Jour 1 : Conception et Architecture

Le projet a débuté par une phase cruciale de conception où la structure globale a été définie. La décision première concernait la représentation des grilles : des listes Python 2D de 10×10 ont été choisies pour leur simplicité et leur efficacité. La convention `grille[ligne][colonne]` a été établie avec un système d'indexation zéro, et les états des cases ont été codés numériquement (0 pour l'eau, 1 pour les bateaux intacts, 2 pour les cases touchées, 3 pour les tirs manqués). 

La modélisation des bateaux requérait une structure capable de stocker plusieurs informations : le nom du navire, sa taille, sa liste de positions sur la grille, et l'ensemble des cases touchées pour suivre les dégâts. Cette structure a été définie dans `utils.py` comme une liste de tuples dans `NOMS_BATEAUX` et exploitée dans `Fonction_Bataille.py`.

L'architecture des modes de jeu a ensuite été conceptualisée. Deux modes principaux émergaient : le mode Humain versus Humain nécessitant deux joueurs avec deux grilles complètes, et le mode Humain versus Ordinateur où un joueur affronte une IA. Cette architecture produisait une hiérarchie claire où `main.py` lançait le menu principal, qui établissait deux interfaces de placement (une pour chaque joueur en HvH, une seule en HvIA), avant de diriger vers la classe de jeu appropriée (`Humain_VS_Humain.py` ou `Humain_VS_Ordinateur.py`).

### Jours 2-3 : Système de base

Les deux jours suivants ont été consacrés à l'implémentation des mécaniques core du jeu. Le placement aléatoire des bateaux était un élément critique, nécessitant un algorithme robuste qui générait une orientation aléatoire (verticale ou horizontale), une position de départ aléatoire, et vérifiait ensuite qu'aucune position du bateau n'entrait en collision avec les bateaux déjà placés. L'algorithme incluait un mécanisme de retry avec un maximum de 500 tentatives, évitant les boucles infinies tout en garantissant presque certainement un placement réussi.

Le système de grille lui-même exigeait des méthodes de création et de stockage. Les grilles devaient être initialisées, puis synchronisées entre la représentation logique et le rendu visuel. Chaque classe de jeu maintenait ses propres instances de grille, et la cohérence entre ce qui était affiché à l'écran et ce qui existait logiquement était critique.

Le système de tir formait le cœur du gameplay. Chaque tir nécessitait une vérification pour s'assurer que la case n'avait pas déjà été jouée, une mise à jour de la grille avec le code de résultat approprié (2 pour un coup touchant, 3 pour un miss), et une évaluation pour déterminer si le bateau visé avait été coulé. Le système retournait alors un message descriptif : "raté", "touché", ou "coulé [nom du bateau]". Ces résultats permettaient aux animations et aux retours visuels appropriés d'être déclenchés.

### Jours 4-5 : Interface Tkinter basique

L'interface graphique commençait par une structure Tkinter simple. Le menu principal initialisait une fenêtre avec un canvas noir comme fond, sur lequel trois boutons permettaient au joueur de choisir le mode de jeu (Humain vs Humain, Humain vs IA) ou de quitter l'application.

Le système d'affichage des grilles utilisait des canvas Tkinter, un pour chaque grille de jeu. Ces canvas devaient s'adapter à la taille de la fenêtre, ce qui signifiait que le code devait lier un gestionnaire à l'événement de redimensionnement et recalculer la taille des cellules de manière dynamique. Lors du redessinage, le code récupérait les dimensions actuelles du canvas, divisait l'espace par dix pour obtenir la taille de chaque cellule, boulcait sur les cent cases, et dessinait soit un point pour l'eau soit des rectangles pour les bateaux selon l'état logique. Les métriques (taille de cellule, offsets) étaient stockées comme attributs du canvas pour utilisation ultérieure.

La conversion des clics de souris en indices de grille était un défi subtil qui serait amélioré plus tard. Initialement, le code prenait les coordonnées de la souris, soustrayait les offsets du canvas, et divisait par la taille de cellule pour obtenir les indices (ligne, colonne). Des vérifications de limites s'assuraient que l'indice restait dans la plage [0, 10).

### Jour 6 : Placement manuel

Le jour six introduisait une interface de placement manuel permettant aux joueurs de disposer eux-mêmes leurs bateaux plutôt que d'accepter un placement aléatoire. Cette interface affichait un canvas avec une grille vide, l'identifier du bateau courant à placer, et le symbole d'orientation actuelle (horizontal ou vertical). 

La logique de placement fonctionnait ainsi : le clic gauche plaçait un bateau, Shift+clic le supprimait, et le clic droit ou la touche R basculaient l'orientation. Le système détectait le modificateur Shift à travers le bitmask `event.state & 0x0001`, une technique qui reviendrait afin de changer la détection. Chaque placement était validé pour s'assurer que le bateau entier restait dans les limites de la grille et ne se chevauchait pas avec d'autres bateaux.

### Jours 7-8 : Système de rendu avancé

Après deux jours, le projet était passé de brutes formes géométriques à des visuels professionnels. Les rectangles avec coins arrondis constituent un élément visuel commun qui, en Tkinter, ne peut pas être dessiné directement. La solution impliquait une technique des trois passes : d'abord, un contour de fond masquait les chevauchements ; ensuite, un remplissage était créé en combinant des rectangles et des ovales ; enfin, un contour visible appliquait les lignes fines.

Le système de rendu en couches était crucial pour la clarté visuelle. L'eau était dessinée en premier (points de base), suivie par les rectangles rouges indiquant les coups touchés, puis les rectangles blancs pour les bateaux intacts, et enfin les points blancs pour les tirs manqués. L'ordre était non-arbitraire ; dessiner dans le mauvais ordre résultait en bateaux occultés ou en indicateurs invisibles. Les couleurs ont été choisies à partir d'une palette thématisée Star Trek : noir profond pour le fond, jaune vif pour les textes importants, rouge éclatant pour les touches, et bleu ciel pour les raté.

### Jours 9-10 : Animations

Le feedback visuel s'améliorait avec l'ajout d'animations asynchrones. Quand un tir manquait, une animation d'éclaboussure se déroulait : des cercles concentriques s'élargissaient depuis le point d'impact sur environ 400 millisecondes, tandis que leur opacité décroissait. Quand un bateau était touché, une explosion éclatait avec des rayons s'étendant depuis le centre en huit ou douze directions selon si le bateau coulait complètement.

L'aspect critique ici était l'asynchronisme. Le code devait utiliser `root.after()` pour planifier les prochaines images d'animation plutôt que d'utiliser `time.sleep()`, qui aurait gelé l'interface entière. Les animations étaient codées comme des fonctions récursives utilisant une variable compteur pour suivre le stade actuel, avec une fermeture correcte pour capturer la valeur du compteur au moment du callback plutôt que plus tard.

### Jours 11-12 : Système IA

L'implémentation de l'IA commençait simple : générer une liste de toutes les cases non jouées et en choisir une aléatoirement. Cependant, cette approche résultait en une IA qui semblait stupide, incapable de concentrer le feu sur les bateaux détectés.

L'optimisation passait par un système de file d'attente. Chaque fois que l'IA touchait un bateau, elle ajoutait les cases adjacentes à une file de tirs en attente. À chaque tour, si la file contenait des entrées, l'IA priait la prochaine case de la file ; sinon elle choisissait aléatoirement. Cette amélioration rendait l'IA remarquablement plus compétente, capturant et coulant les bateaux avec une efficacité quasi-théorique. Pour maintenir le gameplay équitable, la probabilité d'utiliser la file était réduite à 80%, forçant l'IA à choisir aléatoirement les 20% du temps restant pour l'imprédictibilité. Un délai de 700 millisecondes était ajouté avant le tir IA pour donner l'impression que l'IA réfléchissait.

### Jour 13 : Système de son

L'ambiance était améliorée par l'ajout de retours sonores. Une fonction `resource_path()` gérait les chemins de fichiers de manière compatible avec PyInstaller, permettant l'utilisation à la fois en mode développement normal et en mode compilé. Les fichiers audio étaient chargés asynchronement avec le drapeau `SND_ASYNC` pour éviter de bloquer le gameplay. Six fichiers audio distincts créaient une bande sonore riche : un intro dramatique au démarrage, un bruit d'éclaboussure pour les tirs manqués, des sons de coque pour les touches de bateau, un bruit de destruction pour les bateaux coulés, et des signaux sonores pour diverses interactions.

### Jours 14-15 : Menu et dialogues

Le menu principal s'enrichissait d'une animation d'introduction évocatrice. Cent vingt étoiles étaient dessinées aléatoirement sur un canvas noir, scintillant de manière subtile en variant leur opacité. Simultanément, un texte d'introduction montait depuis le bas de l'écran, s'estompant à la fin de la séquence avant que les boutons du menu principal n'apparaissent. Les dialogues modaux demandaient aux joueurs d'entrer leurs noms, utilisant des fenêtres `Toplevel()` avec `grab_set()` pour bloquer l'interaction avec la fenêtre principale jusqu'à ce que le dialogue se ferme.

### Jour 16 : Bombe de zone

Un pouvoir spécial était implémenté : la bombe de zone. Activable une seule fois par partie avec la touche Z, elle causait un tir qui explosait en une zone 3×3 autour du point d'impact, frappant jusqu'à neuf cases. Ce pouvoir était extrêmement puissant et nécessitait un équilibrage minutieux ; il était intentionnellement limité à une utilisation unique pour éviter l'abus. Le rayon de la zone (3×3, 5×5, 7×7) pouvait être ajusté facilement dans le code pour affiner le gameplay.

### Jour 17 : Historique et texte dynamique

L'immersion était augmentée par l'ajout d'un historique scrollable qui enregistrait chaque coup joué et son résultat. Un texte dynamique basé sur Star Trek fournissait des commentaires contextuels : plus de quarante-six phrases différentes prononçaient des observations humoristiques ou dramatiques selon la situation du jeu. L'IA elle-même recevait un nom choisi aléatoirement parmi six options, rendant chaque partie unique et plus narrative.

### Jours 18-19 : Tests et polissage

La phase de stabilisation incluait des tests systématiques de toutes les mécaniques : validations de placement, synchronisation des grilles, validité des tirs, coulée de bateaux, tours IA, intégrité sonore, et comportement du redimensionnement. Des optimisations critiques étaient appliquées, comme le stockage des métriques de canvas pour éviter les recalculs répétés à chaque redessinage. Le code était nettoyé, les imports organisés, les noms de variables uniformisés, et les docstrings ajoutées aux fonctions complexes. La gestion des erreurs était renforcée, particulièrement pour les fichiers audio manquants qui ne devaient pas crasher le jeu.

### Jour 20 : Compilation PyInstaller

La phase finale produisait un exécutable standalone. Un fichier `main.spec` configurait PyInstaller pour inclure tous les fichiers audio (WAV) nécessaires et générait un binaire autonome. Le dossier `dist/` contenant l'exécutable était alors testable sur n'importe quelle machine Windows sans requérir une installation Python, préparant le projet pour la distribution utilisateur.


## Licence et Auteur

Développement par Lighty

**Dernière mise à jour** : Décembre 2025



