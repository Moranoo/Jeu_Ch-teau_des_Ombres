import random
import time
import sys
import threading

NOM_DU_JEU = "Château des Ombres"

def verifier_arret(entree):
    if entree.lower() == "stop":
        print("Vous avez choisi de quitter le jeu. À bientôt !")
        sys.exit()

personnages = {
    "Guerrier": {"avantage": "Squelette", "desavantage": "Fantôme", "hp": 120},
    "Mage": {"avantage": "Fantôme", "desavantage": "Loup-Garou", "hp": 100},
    "Chasseur": {"avantage": "Loup-Garou", "desavantage": "Squelette", "hp": 110}
}

monstres = [
    {"type": "Squelette", "hp": 20, "attaque": (3, 8), "niveau": 1},
    {"type": "Fantôme", "hp": 30, "attaque": (5, 10), "niveau": 2, "peut_suivre": True},
    {"type": "Loup-Garou", "hp": 50, "attaque": (10, 15), "niveau": 3},
    {"type": "Gobelin", "hp": 15, "attaque": (2, 6), "niveau": 1, "empoisonne": True},
    {"type": "Sorcière", "hp": 40, "attaque": (8, 12), "niveau": 2, "paralyse": True}
]

pouvoirs_possibles = {
    "contre_fantome": "Réduit les attaques des fantômes ou endort d’autres monstres",
    "contre_loup_garou": "Réduit les attaques des loups-garous ou affaiblit d’autres monstres",
    "contre_squelette": "Inflige des dégâts aux squelettes ou ralentit d’autres monstres"
}

pouvoirs_acquis = []

def animation_repos():
    print("💤 Vous vous reposez... 💤")
    for _ in range(3):
        print("💤 ", end="", flush=True)
        time.sleep(1)
    print("\nVous vous sentez rafraîchi et prêt à avancer !\n")

def animation_exploration():
    print("Vous commencez à explorer...")
    for _ in range(3):
        print("🔍 ", end="", flush=True)
        time.sleep(1)
    print("\nExploration terminée !\n")

def animation_ouverture_porte():
    print("\nVous avancez vers la porte suivante...")
    for i in range(3, 0, -1):
        print(f"Ouverture de la porte dans... {i}")
        time.sleep(1)
    print("🚪 La porte s'ouvre lentement... et vous entrez dans la nouvelle pièce ! 🚪\n")

def enigme(joueur_hp):
    enigmes = [
        {"question": "Quel est le pluriel de 'cheval' ?", "reponse": "chevaux", "recompense": "contre_fantome"},
        {"question": "Combien font 7 + 5 ?", "reponse": "12", "recompense": "contre_loup_garou"},
        {"question": "Quel est le masculin de 'chienne' ?", "reponse": "chien", "recompense": "contre_squelette"},
        {"question": "Combien font 6 x 3 ?", "reponse": "18", "recompense": "contre_fantome"},
        {"question": "Quel est le pluriel de 'animal' ?", "reponse": "animaux", "recompense": "contre_loup_garou"},
        {"question": "Quel est le masculin de 'vache' ?", "reponse": "veau", "recompense": "contre_squelette"},
        {"question": "Combien font 9 - 4 ?", "reponse": "5", "recompense": "contre_fantome"},
        {"question": "Quel est le pluriel de 'chien' ?", "reponse": "chiens", "recompense": "contre_loup_garou"},
        {"question": "Quel est le féminin de 'taureau' ?", "reponse": "vache", "recompense": "contre_squelette"}
        ]

    enigme = random.choice(enigmes)
    print("\nVous trouvez une énigme sur le mur :")
    print(enigme["question"])

    reponse = None

    def demander_reponse():
        nonlocal reponse
        reponse = input("Votre réponse (vous avez 10 secondes) : ")

    thread = threading.Thread(target=demander_reponse)
    thread.start()

    thread.join(timeout=10)

    if reponse is None:
        print("\nTemps écoulé ! Vous perdez 5 points de vie.")
        joueur_hp -= 5
    elif reponse.lower() == enigme["reponse"]:
        pouvoirs_acquis.append(enigme["recompense"])
        print(f"Bonne réponse ! Vous avez gagné le pouvoir '{enigme['recompense']}' !")
    else:
        print("Mauvaise réponse ! Vous perdez 5 points de vie.")
        joueur_hp -= 5

    return joueur_hp

def choix(joueur_hp, niveau, personnage, nom_personnage, peut_reposer):
    print("\nQue souhaitez-vous faire ?")
    print("1. Explorer la pièce voisine.")
    print("2. Chercher des indices ou des énigmes dans la pièce actuelle.")
    if peut_reposer:
        print("3. Se reposer et récupérer des points de vie.")
    print("Entrez 'power' pour voir vos pouvoirs et points de vie.")

    action = input("Entrez le numéro de votre choix ou 'stop' pour quitter : ")
    verifier_arret(action)

    if action == "1":
        joueur_hp = explorer(joueur_hp, niveau, personnage, nom_personnage)
    elif action == "2":
        animation_exploration()

        if random.random() < 0.3:
            print("Vous ne trouvez rien d'intéressant ici.")
        elif random.random() < 0.3:
            monstre = random.choice(monstres)
            print(f"Un {monstre['type']} surgit pendant votre recherche !")
            joueur_hp = combat(joueur_hp, monstre, personnage)
        else:
            print("Attendez... ah ! Vous trouvez quelque chose !")
            joueur_hp = enigme(joueur_hp)

    elif action == "3" and peut_reposer:
        animation_repos()

        if random.random() < 0.2:
            monstre = random.choice(monstres)
            print(f"Un {monstre['type']} vous dérange pendant votre repos !")
            joueur_hp = combat(joueur_hp, monstre, personnage)
        else:
            joueur_hp = se_reposer(joueur_hp)
            peut_reposer = False

    elif action.lower() == "power":
        afficher_statistiques(joueur_hp)
    else:
        print("Choix invalide. Veuillez réessayer.")
        return choix(joueur_hp, niveau, personnage, nom_personnage, peut_reposer)

    print("\nVous êtes maintenant dans une nouvelle pièce.\n")
    return joueur_hp, peut_reposer

def explorer(joueur_hp, niveau, personnage, nom_personnage):
    animation_ouverture_porte()

    evenement = random.choice(["monstre", "objet", "vide", "piege", "pnj"])

    if evenement == "monstre":
        possible_monstres = [monstre for monstre in monstres if monstre["niveau"] <= niveau]
        if possible_monstres:
            monstre = random.choice(possible_monstres)
            print(f"Un {monstre['type']} surgit avec {monstre['hp']} points de vie !")
            joueur_hp = combat(joueur_hp, monstre, personnage)
    elif evenement == "objet":
        objet = random.choice(["une potion de soin", "un ancien manuscrit"])
        print(f"Vous trouvez {objet}.")
        if objet == "une potion de soin":
            gain = random.randint(10, 20)
            joueur_hp += gain
            print(f"Vous utilisez la potion et récupérez {gain} points de vie. Points de vie actuels : {joueur_hp}.")
    elif evenement == "piege":
        print("Vous tombez dans un piège ! Vous perdez 10 points de vie.")
        joueur_hp -= 10
    elif evenement == "pnj":
        pnj = random.choice(["un vieux sage", "un marchand", "un aventurier perdu"])
        print(f"Vous rencontrez {pnj}.")
        if pnj == "un vieux sage":
            print("Le sage vous donne un conseil précieux.")
        elif pnj == "un marchand":
            print("Le marchand vous offre un objet spécial.")
            objet = random.choice(["une potion de soin", "un ancien manuscrit"])
            if objet == "une potion de soin":
                gain = random.randint(10, 20)
                joueur_hp += gain
                print(f"Vous utilisez la potion et récupérez {gain} points de vie. Points de vie actuels : {joueur_hp}.")
        elif pnj == "un aventurier perdu":
            print("L'aventurier vous demande de l'aide. Vous gagnez un allié temporaire.")
    else:
        print("La pièce est vide, mais vous sentez une atmosphère étrange.")

    print("\nVous êtes maintenant dans une nouvelle pièce.\n")
    return joueur_hp

def afficher_statistiques(joueur_hp):
    print("\n==== Statistiques ====")
    print(f"Points de vie : {joueur_hp}")
    print("Pouvoirs acquis :")
    for pouvoir in pouvoirs_acquis:
        print(f"- {pouvoir} : {pouvoirs_possibles[pouvoir]}")
    print("======================\n")

def se_reposer(joueur_hp):
    recup_hp = random.randint(5, 20)
    joueur_hp += recup_hp
    print(f"Vous récupérez {recup_hp} points de vie. Points de vie actuels : {joueur_hp}.")
    return joueur_hp

def combat(joueur_hp, monstre, personnage):
    print(f"Vous affrontez un {monstre['type']} avec {monstre['hp']} points de vie.")

    while monstre["hp"] > 0 and joueur_hp > 0:
        print("\nQue souhaitez-vous faire ?")
        print("1. Attaquer le monstre.")
        print("2. Bloquer la prochaine attaque.")
        print("3. Tenter de fuir.")

        if pouvoirs_acquis:
            for idx, pouvoir in enumerate(pouvoirs_acquis, start=4):
                print(f"{idx}. Utiliser '{pouvoir}' ({pouvoirs_possibles[pouvoir]})")

        choix = input("Entrez le numéro de votre choix : ")
        verifier_arret(choix)

        if choix == "1":
            dommage = random.randint(5, 15)
            if monstre["type"] == personnage["avantage"]:
                dommage += 5
                print(f"Avantage ! Vous infligez {dommage} points de dégât au {monstre['type']}.")
            elif monstre["type"] == personnage["desavantage"]:
                dommage -= 3
                print(f"Désavantage... Vous infligez seulement {dommage} points de dégât.")
            monstre["hp"] -= dommage
            if monstre["hp"] <= 0:
                print(f"Vous avez vaincu le {monstre['type']} !")
                break

        elif choix == "2":
            blocage = random.randint(0, 10)
            joueur_hp += blocage
            print(f"Vous bloquez partiellement l'attaque et regagnez {blocage} points de vie.")

        elif choix == "3":
            if random.choice([True, False]):
                print("Vous avez réussi à fuir!")
                return joueur_hp
            else:
                print("La fuite a échoué! Le monstre attaque.")

        elif choix.isdigit() and int(choix) >= 4 and int(choix) - 4 < len(pouvoirs_acquis):
            pouvoir = pouvoirs_acquis[int(choix) - 4]
            if pouvoir == "contre_fantome" and monstre["type"] == "Fantôme":
                print("Vous utilisez votre pouvoir spécial contre le fantôme ! Il disparaît dans un nuage de fumée.")
                monstre["hp"] = 0
            elif pouvoir == "contre_loup_garou" and monstre["type"] == "Loup-Garou":
                print("Vous utilisez votre pouvoir spécial contre le loup-garou ! Il est affaibli et perd l’envie de combattre.")
                monstre["hp"] -= 15
            elif pouvoir == "contre_squelette" and monstre["type"] == "Squelette":
                print("Vous utilisez votre pouvoir contre le squelette, infligeant de lourds dégâts !")
                monstre["hp"] -= 20
            else:
                print("Vous utilisez un pouvoir hors de son contexte : le monstre est confus et perd un tour.")
                monstre["hp"] -= 5 if monstre["hp"] > 5 else 0

            pouvoirs_acquis.pop(int(choix) - 4)

            if monstre["hp"] <= 0:
                print(f"Le {monstre['type']} a été vaincu grâce à votre pouvoir !")
                break

        else:
            print("Choix invalide.")
            continue

        if monstre["hp"] > 0:
            attaque_monstre = random.randint(*monstre["attaque"])
            joueur_hp -= attaque_monstre
            print(f"Le {monstre['type']} vous attaque et inflige {attaque_monstre} points de dégât. Points de vie restants : {joueur_hp}")

    if joueur_hp <= 0:
        print("Vous avez été vaincu... Game Over.")
    return joueur_hp

def choisir_personnage():
    print("Choisissez votre personnage :")
    for idx, (nom, details) in enumerate(personnages.items(), start=1):
        print(f"{idx}. {nom} (HP: {details['hp']}, Avantage: {details['avantage']}, Désavantage: {details['desavantage']})")

    choix = int(input("Entrez le numéro de votre choix : ")) - 1
    nom_personnage = list(personnages.keys())[choix]
    personnage = personnages[nom_personnage]

    return personnage, nom_personnage

def introduction():
    print(f"Bienvenue dans {NOM_DU_JEU} !")
    print("Vous êtes un aventurier intrépide qui a entendu parler d'un trésor légendaire caché dans les profondeurs du château.")
    print("Votre objectif est de survivre aux dangers qui vous attendent et de découvrir le trésor avant qu'il ne soit trop tard.")
    print("Bonne chance, aventurier !\n")

def jouer():
    introduction()
    personnage, nom_personnage = choisir_personnage()
    joueur_hp = personnage["hp"]
    niveau = 1
    peut_reposer = True

    while joueur_hp > 0:
        joueur_hp, peut_reposer = choix(joueur_hp, niveau, personnage, nom_personnage, peut_reposer)
        niveau += 1
        peut_reposer = True
        if joueur_hp <= 0:
            print("Vous avez perdu tous vos points de vie. Fin de l'aventure.")
            break
        if random.choice([True, False, False, False]):
            print("Vous avez trouvé la sortie du château ! Félicitations, vous avez survécu à cette aventure mystérieuse.")
            break

if __name__ == "__main__":
    jouer()
