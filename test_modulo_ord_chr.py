lettre_de_depart = "m"
code_depart = ord(lettre_de_depart)
decalage = 5
nouveau_nombre = code_depart + decalage
lettre_arrive = chr(nouveau_nombre)
print(lettre_arrive)

#2

lettre_de_depart = "z"  # On teste avec le 'z' !
code_depart = ord(lettre_de_depart)
decalage = 5

# La formule magique :
nouveau_nombre = ((code_depart - 97 + decalage) % 26) + 97

lettre_arrive = chr(nouveau_nombre)
print(lettre_arrive)
