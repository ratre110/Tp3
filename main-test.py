'''Module principal, gère la logistique du jeu quoridor'''
from argparse import ArgumentParser
import api
import minimax


def analyser_commande():
    '''Traitement des arguments passés dans l'invité de commandes'''
    parser = ArgumentParser(
        description='Jeu Quoridor - phase 1',
    )

    parser.add_argument(
        'idul', nargs='+', metavar='IDUL', help='IDUL du joueur.',
    )

    parser.add_argument(
        '-l', '--lister',
        help='Lister les identifiants de vos 20 dernières parties.',
        action="store_true"
    )

    return parser.parse_args()


def afficher_damier_ascii(game_state):
    '''Décodage d'un dictionnaire de jeu en art ASCII'''
    grid = make_grid_list()
    header = f'Légende: 1={IDUL_ARG[0]}, 2=robot\n   -----------------------------------\n'
    footer = '--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9'

    # Insertion des joueurs
    for i in game_state["joueurs"]:
        if i["nom"] == 'simar86':
            pos = i["pos"]
            grid[pos[1] * 2 - 2][pos[0] * 4 - 3] = '1'
        else:
            pos = i["pos"]
            grid[pos[1] * 2 - 2][pos[0] * 4 - 3] = '2'

    # Insertion des murs horizontaux
    for i in game_state["murs"]["horizontaux"]:
        y = i[1] * 2 - 3
        x = i[0] * 4 - 4
        for j in range(7):
            grid[y][x + j] = '-'

    # Insertion des murs verticaux
    for i in game_state["murs"]["verticaux"]:
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

    print(tot)


def make_grid_list():
    '''Retourne une liste 2d correspondant à un jeu vide'''
    return [
        [' ' if (x - 1) % 4 != 0 else '.' for x in range(35)]
        if (y - 1) % 2 != 0 else
        [' ' for z in range(35)] for y in range(17)
    ]


if __name__ == '__main__':

    ARGS = analyser_commande()

    IDUL_ARG = ARGS.idul

    EN_JEU = True

    if not ARGS.lister:
        print('\n' + '='*40 + '\n' + ' '*14 + 'Jeu Quoridor\n' + '='*40 + '\n')

        try:
            ID_PARTIE, ETAT = api.débuter_partie(IDUL_ARG)

            print(
                f'''Une partie a été entamée avec le serveur de jeu.
        ID: {ID_PARTIE}
        IDUL: {IDUL_ARG}'''
            )
            print("\nVoici l'état initial du jeu:")
            afficher_damier_ascii(ETAT)

        except RuntimeError as err:
            print(
                f'''Une erreur est survenue lors du lancement de la partie.
                Le message d'erreur suivant a été communiqué par le serveur:
                {str(err)}'''
            )

        while EN_JEU:
            try:
                LIST_POS_COUP, TYPE_COUP = minimax.calc_best_move(ETAT, 1)
                try:
                    POS_COUP = (int(LIST_POS_COUP[0]), int(LIST_POS_COUP[1]))
                except Exception:
                    raise AssertionError("Le format entré est invalide")

                # if TYPE_COUP == 'D':
                #     assert 1 <= POS_COUP[0] <= 9 and 1 <= POS_COUP[1] <= 9, "Indice invalide"
                # else:
                #     assert 2 <= POS_COUP[0] <= 9 and 1 <= POS_COUP[1] <= 8, "Indice invalide"

                ETAT = api.jouer_coup(ID_PARTIE, TYPE_COUP, POS_COUP)

                afficher_damier_ascii(ETAT)

            except AssertionError as err:
                print(LIST_POS_COUP, TYPE_COUP)
                print(err)

            except RuntimeError as err:
                print(err)

            except StopIteration as gagnant:
                print(str(gagnant) + 'a gagné la partie!')
                EN_JEU = False

            except KeyboardInterrupt:
                print("\nPartie annulée par l'utilisateur\n")
                EN_JEU = False
    else:
        print(api.lister_parties(IDUL_ARG))
