'''Ce module sert à effectuer des tests reliés à la classe Quoridor'''
from collections.abc import Iterable
import networkx as nx
from graphe import construire_graphe


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.

        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        :raises QuoridorError: si joueurs n'est pas itérable.
        :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est > 10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si murs n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un mur est invalide.
        """

        if not isinstance(joueurs, Iterable):
            raise QuoridorError(
                "L'argument 'joueurs' doit être un itérable")
        if len(joueurs) > 2:
            raise QuoridorError("Seulement 2 joueurs peuvent être spécifiés")

        liste_joueurs = []

        for i in range(len(joueurs)):
            if isinstance(joueurs[i], str):
                liste_joueurs.append(
                    {'nom': joueurs[i], 'murs': 10, 'pos': 'adapt'})
            else:
                liste_joueurs.append(joueurs[i])

        bas_occ = False

        for i in range(len(liste_joueurs)):
            if liste_joueurs[i]['pos'] == (5, 1):
                bas_occ = True

        for i in range(len(liste_joueurs)):
            if liste_joueurs[i]['pos'] == 'adapt':
                if not bas_occ:
                    liste_joueurs[i]['pos'] = (5, 1)
                    bas_occ = True
                else:
                    liste_joueurs[i]['pos'] = (5, 9)

            valid_range = [_ for _ in range(1, 10)]
            valid_pairs = [(x, y) for x in valid_range for y in valid_range]
            valid_pairs += [[x, y] for x in valid_range for y in valid_range]
            if not liste_joueurs[i]['pos'] in valid_pairs:
                raise QuoridorError(f"Position du joueur {i + 1} invalide")
            if not 0 <= liste_joueurs[i]['murs'] <= 10:
                raise QuoridorError(
                    f"Le nombre de murs du joueur {i + 1} est invalide")

        self.joueurs = liste_joueurs

        # Murs

        if murs is None:
            murs = {'horizontaux': [], 'verticaux': []}

        if not isinstance(murs, dict):
            raise QuoridorError(
                "L'argument :murs: doit être un dictionnaire")

        murs_tot = 0
        for i in self.joueurs:
            murs_tot += i['murs']
        murs_tot += len(murs['horizontaux']) + len(murs['verticaux'])
        if murs_tot != 20:
            raise QuoridorError("Le total des murs doit être de 20")

        for i in range(len(murs['horizontaux'])):
            if not (1 <= murs['horizontaux'][i][0] <= 8 and 2 <= murs['horizontaux'][i][1] <= 9):
                raise QuoridorError(
                    f"La coordonnée du mur horizontal {i + 1} est erronée")
        for i in range(len(murs['verticaux'])):
            if not (2 <= murs['verticaux'][i][0] <= 9 and 1 <= murs['verticaux'][i][1] <= 8):
                raise QuoridorError(
                    f"La coordonnée du mur vertical {i + 1} est erronée")

        self.murs = murs
        self.état_partie()

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """

        etat = self.état_partie()

        grid = [
            [' ' if (x - 1) % 4 != 0 else '.' for x in range(35)]
            if (y - 1) % 2 != 0 else
            [' ' for z in range(35)] for y in range(17)
        ]

        header = (
            f'Légende: 1={etat["joueurs"][0]["nom"]}, 2={etat["joueurs"][1]["nom"]}' +
            '\n   -----------------------------------\n'
        )
        footer = '--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9'

        # Insertion des joueurs
        pos = etat["joueurs"][0]["pos"]
        grid[pos[1] * 2 - 2][pos[0] * 4 - 3] = '1'

        pos = etat["joueurs"][1]["pos"]
        grid[pos[1] * 2 - 2][pos[0] * 4 - 3] = '2'

        # Insertion des murs horizontaux
        for i in etat["murs"]["horizontaux"]:
            y = i[1] * 2 - 3
            x = i[0] * 4 - 4
            for j in range(7):
                grid[y][x + j] = '-'

        # Insertion des murs verticaux
        for i in etat["murs"]["verticaux"]:
            y = i[1] * 2 - 2
            x = i[0] * 4 - 5
            for j in range(3):
                grid[y + j][x] = '|'

        # Transformation de la liste en ASCII art
        body = '9 |' + ''.join(grid[16]) + '|\n'
        for i in range(8, 0, -1):
            body += '  |' + ''.join(grid[i * 2 - 1]) + '|\n' + f'{i} |'+''.join(
                grid[i * 2 - 2]) + '|\n'

        tot = header + body + footer

        return tot

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la position est invalide (en dehors du damier).
        :raises QuoridorError: la position est invalide pour l'état actuel du jeu.
        """

        état = self.état_partie()
        self.position = position

        # Erreur si le joueur est autre que 1 et 2
        if joueur not in (1, 2):
            raise QuoridorError(f"Aucun joueur n'est associé à {joueur}")

        # Erreur si la position est en dehors du damier
        if position[0] < 1 or position[0] > 9 or position[1] < 1 or position[1] > 9:
            raise QuoridorError('Les dimensions souhaitées sont incorrectes')

        # Erreur si le déplacement est impossible
        pos_init = état['joueurs'][joueur - 1]['pos']
        if not (abs(position[0] - pos_init[0]) != 1 or abs(position[1] - pos_init[1]) != 1):
            raise QuoridorError(f'Le déplacement {position} est impossible')

         # Déplacer le joueurs
        if joueur == 1:
            état['joueurs'][0]['pos'] = position
        if joueur == 2:
            état['joueurs'][1]['pos'] = position

        self.joueurs = état["joueurs"]

    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {'horizontaux': [...],'verticaux': [...],
            }
        }

        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
        associée à sa position sur le damier. Une position est représentée par un tuple
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes x et x+1.
        """

        return {'joueurs': self.joueurs, 'murs': self.murs}

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la partie est déjà terminée.
        """
        if self.partie_terminée():
            print('HERE')
            raise QuoridorError("La partie est terminée")
        if not 1 <= joueur <= 2:
            raise QuoridorError("Le numéro du joueur spécifié est invalide")

        état = self.état_partie()

        if joueur == 1:
            strJoueur = 'B1'
            nonstrJoueur = 'B2'
        else:
            strJoueur = 'B2'
            nonstrJoueur = 'B1'

        graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux']
        )

        if joueur == 1:
            diff = 1
        else:
            diff = -1

        pos_soi = état['joueurs'][joueur - 1]['pos']
        pos_adversaire = état['joueurs'][joueur - 1 + diff]['pos']

        delta = (
            nx.shortest_path_length(graphe, (pos_adversaire), nonstrJoueur) -
            nx.shortest_path_length(graphe, (pos_soi), strJoueur)
        )

        coup = 'mur' if delta < 0 else 'bouge'

        if coup == 'mur':
            position_prochaine = nx.shortest_path(
                graphe, (pos_adversaire), nonstrJoueur)[0]
            if pos_adversaire[1] - position_prochaine[1] != 0:  # Si bouge verticalement
                orientation = 'horizontal'
                position_mur = pos_adversaire
            else:  # Si bouge horizontalement
                orientation = 'vertical'
                # Si bouge vers la droite
                if pos_adversaire[0] - position_prochaine[0] <= 0:
                    position_mur = (
                        position_prochaine[0], position_prochaine[1] - 1)
                else:  # Si bouge vers la gauche
                    position_mur = (
                        position_prochaine[0] - 1, position_prochaine[1] - 1)

            invalide = False

            if orientation == 'horizontal':
                for mur in état['murs']['horizontaux']:
                    if mur[1] == position_mur[1]:
                        if -1 <= mur[0] - position_mur[0] <= 1:  # Si les murs se chevauchent
                            invalide = True

                for mur in état['murs']['verticaux']:
                    if position_mur == (mur[0] + 1, mur[1] - 1):
                        invalide = True

                if not (1 <= position_mur[0] <= 8 and 2 <= position_mur[1] <= 9):
                    invalide = True

            else:
                for mur in état['murs']['verticaux']:
                    print(position_mur[1], mur[1])
                    if mur[0] == position_mur[0]:
                        print(position_mur[1], mur[1])
                        if -1 <= mur[1] - position_mur[1] <= 1:  # Si les murs se chevauchent
                            print('here')
                            invalide = True

                for mur in état['murs']['horizontaux']:
                    if position_mur == (mur[0] - 1, mur[1] + 1):
                        invalide = True

                if not (2 <= position_mur[0] <= 9 and 1 <= position_mur[1] <= 8):
                    invalide = True

            if not invalide:
                if orientation == 'vertical':
                    print('---', position_mur, orientation, '---')
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
                coup = 'bouge'

        if coup == 'mur':
            print(f'Placer mur en {position_mur}, {orientation}')
            self.placer_mur(joueur, position_mur, orientation)

        else:
            print(
                f'Déplacer joueur {joueur} en {nx.shortest_path(graphe, (pos_soi), strJoueur)[1]}')
            self.déplacer_jeton(joueur, nx.shortest_path(
                graphe, (pos_soi), strJoueur)[1])

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        état = self.état_partie()

        if état['joueurs'][0]['pos'][1] == 9:
            return état['joueurs'][0]['nom']
        if état['joueurs'][1]['pos'][1] == 1:
            return état['joueurs'][1]['nom']
        else:
            return False

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: un mur occupe déjà cette position.
        :raises QuoridorError: la position est invalide pour cette orientation.
        :raises QuoridorError: le joueur a déjà placé tous ses murs.
        """

        état = self.état_partie()

        if joueur == 1:
            # Si l'orientation est horizontale
            if orientation == 'horizontal':
                # on traite l'erreur en premier
                for i in état['murs']['horizontaux']:
                    if tuple(i) == position:
                        raise QuoridorError(
                            'un mur occupe déja cette position')
                état['murs']['horizontaux'].append(list(position))
            # si la boucle est verticale
            if orientation == 'vertical':
                # on traite l'erreur en premier
                for i in état['murs']['verticaux']:
                    if tuple(i) == position:
                        raise QuoridorError(
                            'un mur occupe déja cette position')
                état['murs']['verticaux'].append(list(position))
        if joueur == 2:
            if orientation == 'horizontal':
                # on traite l'erreure en premier
                for i in état['murs']['horizontaux']:
                    if tuple(i) == position:
                        raise QuoridorError(
                            'un mur occupe déja cette position')
                état['murs']['horizontaux'].append(list(position))
            # si la boucle est verticale
            if orientation == 'vertical':
                # on traite l'erreur en premier
                for i in état['murs']['verticaux']:
                    if tuple(i) == position:
                        raise QuoridorError(
                            'un mur occupe déja cette position')
                état['murs']['verticaux'].append(list(position))
        # erreure si le joueur n'est pas 1 ou 2
        if joueur not in (1, 2):
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2')
        # erreur pour les murs
        if orientation == 'horizontal':
            if position[0] < 1 or position[0] >= 8:
                raise QuoridorError
            if position[1] < 1 or position[1] > 9:
                raise QuoridorError(
                    'la position est invalide pour cette orientation.')

        if orientation == 'vertical':
            if position[0] < 1 or position[0] > 9:
                raise QuoridorError
            if position[1] < 1 or position[1] >= 8:
                raise QuoridorError(
                    'la position est invalide pour cette orientation.')

        if (état['joueur'][i]['murs'] for i in range(2)) == 0:
            raise QuoridorError('le joueur a déjà placé tous ses murs.')

        self.murs = état["murs"]

    def available_wall_positions(self):
        '''Retourne un liste de tuples contenant les positions possibles de murs à ajouter'''

class QuoridorError(Exception):
    pass

class QuoridorX(Quoridor):
    pass


if __name__ == "__main__":
    partie = Quoridor(['Simon', 'JS'])
    print(partie)
    while 1:

        partie.jouer_coup(1)
        print(partie)
        partie.jouer_coup(2)
        print(partie)
