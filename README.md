# Château des Ombres

## Description

"Château Hanté" est un jeu de rôle en ligne de commande dans lequel vous explorez un château mystérieux, affrontez des monstres, et résolvez des énigmes pour acquérir des pouvoirs spéciaux. Vous devez choisir judicieusement vos actions pour survivre et, éventuellement, trouver la sortie du château !

## Règles du Jeu

- **Objectif** : Survivez aux dangers du château et trouvez la sortie.
- **Personnage** : Choisissez un personnage avec un avantage et un désavantage contre certains types de monstres.
- **Monstres** : Rencontrez des monstres de différents types. Utilisez vos attaques, bloquez, fuyez, ou employez des pouvoirs spéciaux pour les vaincre.
- **Pouvoirs** : Résolvez des énigmes pour obtenir des pouvoirs qui vous aideront contre des types spécifiques de monstres.
- **Exploration** : Explorez le château, cherchez des indices ou reposez-vous pour récupérer des points de vie.
- **Sortie** : La sortie du château peut être trouvée après un certain nombre d'explorations et de combats.

## Guide d'Utilisation

1. **Lancez le jeu** : `jeu2.py`
2. **Choisissez un personnage** : Chaque personnage possède un avantage contre certains monstres et un désavantage contre d'autres.
3. **Options dans les pièces** :
   - **Explorer la pièce voisine** : Découvrez des objets, rencontrez des monstres, ou trouvez des indices.
   - **Chercher des indices/énigmes** : Résolvez des énigmes pour obtenir des pouvoirs.
   - **Se reposer** : Récupérez des points de vie, mais attention aux interruptions par les monstres.
4. **Affrontez les monstres** :
   - Choisissez d'attaquer, de bloquer, de fuir ou d'utiliser des pouvoirs.
   - Utilisez les pouvoirs pour affaiblir ou vaincre les monstres, en tenant compte des effets spécifiques contre chaque type de monstre.

## Explications du Code

- **Exploration** : La fonction `explorer()` permet de découvrir des événements variés (monstres, objets, vide).
- **Énigmes** : La fonction `enigme()` génère des énigmes aléatoires ; les résoudre confère des pouvoirs.
- **Combat** : La fonction `combat()` offre plusieurs actions, y compris l'utilisation des pouvoirs acquis. Les pouvoirs ont des effets contextuels, maximisés lorsqu'ils sont utilisés contre les monstres auxquels ils sont destinés.
- **Pouvoirs et Avantages/Désavantages** : Chaque personnage a un avantage contre certains monstres, et les pouvoirs peuvent être utilisés pour affecter spécifiquement certains types de monstres.
- **Progression** : La sortie devient accessible après plusieurs explorations et combats, assurant une structure de progression.

## Exemples d'Actions

- **Explorer** : "1. Explorer la pièce voisine."
- **Chercher des indices** : "2. Chercher des indices ou des énigmes."
- **Se reposer** : "3. Se reposer et récupérer des points de vie."

## Quitter le Jeu

- À tout moment, entrez "stop" pour quitter le jeu.

---

Bonne chance et amusez-vous bien dans le Château Hanté !
