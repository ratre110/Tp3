'''Module principal'''
from argparse import ArgumentParser
import api


def analyser_commande():
    '''Traitement des arguments passés dans l'invité de commandes'''
    parser = ArgumentParser(description='Jeu Quoridor - Phase 3')
    #Positional arguments
    parser.add_argument('idul', metavar='idul', help='IDUL du joueur', type=str)

    #Optional arguments
    parser.add_argument('-a','--auto', action='store_true', help="Jouer en mode automatique avec l'IDUL spécifié")
    parser.add_argument('-x','--contre_serveur', action='store_true', help="Jouer en mode manuel contre le serveur avec l'IDUL dans un affichage graphique")
    parser.add_argument('-ax', '--auto_contre_serveur', action='store_true', help="Jouer en mode automatique contre le serveur avec l'IDUL dans un affichage graphique")
    return parser.parse_args()

#TODO: Entrer ce que les optional arguments font!!!

if __name__ == "__main__":
    print(analyser_commande())

