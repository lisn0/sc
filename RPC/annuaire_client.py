import rfoo


def menu(proxy):
    print("Choix de l’action a effectuer :")
    choice = input("""
                      1: Ajouter une entree dans le repertoire
                      2: Afficher le numero de telephone d’une personne
                      3: Afficher le nombre de numeros enregistres dans le repertoire
                      4: Afficher le contenu de tout le repertoire
                      5: Supprimer du repertoire une personne et son numero
                      6: Effacer tout le contenu du repertoire
                      0: Quitter le programme
                      Veuillez entrer votre choix: """)
    switcher = {
        1: "ajouterEntree",
        2: "trouverNumero",
        3: "nbNumeros",
        4: "getAll",
        5: "supprimerEntree",
        6: "supprimerTout",
        0: 'exit'
    }
    c = switcher.get(int(choice), 'repeat')
    if c == 'exit':
        return
    elif choice == "repeat":
        print("Please try again")
        menu(proxy)

    rpc_function = getattr(proxy, c)
    if c == 'ajouterEntree':
        nom = input('saisir un nom              > ')
        num = input('saisir numero de telephone > ')
        rpc_function(nom, num)

    elif c in ['trouverNumero', 'supprimerEntree']:
        nom = input('saisir un nom              > ')
        print(rpc_function(nom))

    else:
        print(rpc_function())
    menu(proxy)


if __name__ == '__main__':
    port = 52525
    handler = rfoo.InetConnection().connect(port=52525)  # [host=host , port=port] in case the server in another machine
    proxy = rfoo.Proxy(handler)
    menu(proxy)
    handler.close()
