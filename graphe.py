'''Ce module contient un fonction networkx'''
import networkx as nx
import matplotlib.pyplot as plt


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0],
                          2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

def jouer_coup(état):

    graphe = construire_graphe(
        [joueur['pos'] for joueur in état['joueurs']],
        état['murs']['horizontaux'],
        état['murs']['verticaux']
    )

    pos_soi = état['joueurs'][0]['position']
    pos_adversaire = état['joueurs'][1]['position']

    delta = (
        nx.shortest_path_length(graphe, (pos_adversaire), 'B2') -
        nx.shortest_path_length(graphe, (pos_soi), 'B1')
    )

    coup = 'mur' if delta < 0 else 'bouge'

    if coup == 'mur':
        position_prochaine = nx.shortest_path(
            graphe, (pos_adversaire), 'B2')[0]
        if pos_adversaire[1] - position_prochaine[1] != 0:  # Si bouge verticalement
            orientation = 'horizontal'
            position_mur = pos_adversaire
        else:  # Si bouge horizontalement
            orientation = 'vertical'
            if pos_adversaire[0] - position_prochaine[0] <= 0:  # Si bouge vers la droite
                position_mur = (
                    position_prochaine[0], position_prochaine[1] - 1)
            else:  # Si bouge vers la gauche
                position_mur = (
                    position_prochaine[0] - 1, position_prochaine[1] - 1)

        invalide = False

        if orientation == 'horizontal':
            for mur in état['murs']['horizontaux']:
                if mur[1] == position_mur[1]:
                    if -1 < mur[0] - position_mur[0] < 1:  # Si les murs se chevauchent
                        invalide = True

            for mur in état['murs']['verticaux']:
                if position_mur == (mur[0] + 1, mur[1] - 1):
                    invalide = True

            if not (1 <= position_mur[0] <= 8 and 2 <= position_mur[1] <= 9):
                invalide = True

        else:
            for mur in état['murs']['verticaux']:
                if mur[0] == position_mur[0]:
                    if -1 < mur[1] - position_mur[1] < 1:  # Si les murs se chevauchent
                        invalide = True

            for mur in état['murs']['horizontaux']:
                if position_mur == (mur[0] - 1, mur[1] + 1):
                    invalide = True

            if not (2 <= position_mur[0] <= 9 and 1 <= position_mur[1] <= 8):
                invalide = True

        if orientation == 'vertical':
            nouveau_graphe = construire_graphe(
                [joueur['pos'] for joueur in état['joueurs']],
                état['murs']['horizontaux'],
                état['murs']['verticaux'] + [position_mur]
            )

        else:
            nouveau_graphe = construire_graphe(
                [joueur['pos'] for joueur in état['joueurs']],
                état['murs']['horizontaux'] + [position_mur],
                état['murs']['verticaux']
            )

        if not nx.has_path(nouveau_graphe, (pos_adversaire), 'B2'):
            invalide = True

        if invalide:
            coup = 'déplacement'
    
    if coup == 'mur':
        pass
        # self.placer_mur(1, position_mur, orientation)

    else:
        pass
        # self.déplacer_jeton(1, nx.shortest_path(graphe, (pos_soi), 'B1')[0])




if __name__ == "__main__":
    état = {
        "joueurs": [
            {"nom": "idul", "murs": 7, "pos": [5, 6]},
            {"nom": "automate", "murs": 3, "pos": [5, 7]}
        ],
        "murs": {
            "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
            "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
        }
    }

    graphe = construire_graphe(
        [joueur['pos'] for joueur in état['joueurs']],
        état['murs']['horizontaux'],
        état['murs']['verticaux']
    )
    positions = {'B1': (5, 10), 'B2': (5, 0)}

    colors = {
        'B1': 'red', 'B2': 'green',
        tuple(état['joueurs'][0]['pos']): 'red',
        tuple(état['joueurs'][1]['pos']): 'green',
    }
    sizes = {
        tuple(état['joueurs'][0]['pos']): 300,
        tuple(état['joueurs'][1]['pos']): 300
    }

    nx.draw(
        graphe,
        pos={node: positions.get(node, node) for node in graphe},
        node_size=[sizes.get(node, 100) for node in graphe],
        node_color=[colors.get(node, 'gray') for node in graphe],
    )
    plt.show()


