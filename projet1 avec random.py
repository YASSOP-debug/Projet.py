# projet 1 avec gemini

import random # Aléatoire

print("Xime.nias_225_YASSOP赤")

print("Salut 👋🏼 Bienvenue, je te présente un petit jeu ! ")

nom = input("C'est quoi ton nom ? ")

print(f"Merci {nom} de bien vouloir tester mon code. En vrai, le merci c'est pour moi, je t'ai quand même fait la grâce de te choisir pour tester mon code ! 🙏🏻🤣")

print(f"🚫 Un petit avertissement pour toi {nom} : évite les lettres là où il faut mettre des chiffres, sinon tout le code crame et tu devras recommencer.")

print(f"{nom}, tu vois que je te fais confiance, je t'ai balancé le point faible de mon code donc ne fous pas la merde.")

# while : une grande boucle pour tout le jeu
while True : 
    nombre = random.randint(1, 100)

    utilisateur = input("Tu es prêt ? Réponds par un [oui] ou un [non] : ")
    essais = 1
    if "oui" in utilisateur:
        print(f"Super ! {nom}, choisis un chiffre entre 1 et 100, et si tu trouves le même chiffre que moi, tu as gagné.")
        print("Tu auras 7 chances, donc 7 essais.")
        proposition = int(input("Choisis un nombre entre 1 et 100 : "))
    
        # Ligne 25 : une petite boucle pour la répétition
        while proposition != nombre and essais < 7:
            if proposition > nombre:
                print("C'est plus petit !")
            elif proposition < nombre:
                print("C'est plus grand !")
        
            proposition = int(input("Recommence, tu y es presque : "))
            essais += 1
            print(f"Il te reste {7-essais} chances.")
            
        if proposition == nombre:
            print(f"Bravo {nom} ! Tu as trouvé le nombre secret ! 🎉")
        else:
            print(f"Désolé tu as perdu, le nombre secret était {nombre}.")
            
        rejouer = input(f"Tu veux rejouer {nom} ? Réponds par oui ou non ! ")
        if "non" in rejouer:
            print(f"Merci {nom} d'avoir participé 👋🏼")
            break
        
# Si l'utilisateur répond non, fin du programme grâce à la fonction raise SystemExit
 
    if "non" in utilisateur:
        print(f"D'accord, à la prochaine 👋🏼 {nom}")
        raise SystemExit("Fin du programme")
