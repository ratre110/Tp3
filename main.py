'''Module principal'''
from argparse import ArgumentParser
import api


def analyser_commande():
    '''Traitement des arguments passés dans l'invité de commandes'''
    parser = ArgumentParser(
        description='',
    )
    return parser.parse_args()
