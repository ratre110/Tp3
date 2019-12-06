'''Ce module contient les fonctions permettant de communiquer avec le serveur de jeu.'''
import requests


def lister_parties(idul):
    '''Effectue un requête au serveur de quoridor afin d'obtenir
    les 20 dernières parties de l'idul passé en argument

    '''
    url = 'https://python.gel.ulaval.ca/quoridor/api/lister/'
    req = requests.get(url, params={'idul': idul})
    data = req.json()
    if req.status_code == 200:
        if data.get('message') is not None:
            raise RuntimeError(data['message'])
        return data['parties']
    raise ConnectionError(
        f"La requête vers {url} a échoué. (Code d'erreur: {req.status_code})")


def débuter_partie(idul):
    '''Communique avec le serveur de corridor pour entamer une
     nouvelle partie liée à l'idul passé en argument

    '''
    url = 'https://python.gel.ulaval.ca/quoridor/api/débuter/'
    req = requests.post(url, data={'idul': idul})
    data = req.json()
    if req.status_code == 200:
        if data.get('message') is not None:
            raise RuntimeError(data['message'])
        return data['id'], data['état']
    raise ConnectionError(
        f"La requête vers {url} a échoué. (Code d'erreur: {req.status_code})")


def jouer_coup(id_partie, type_coup, position):
    '''Communique le mouvement du joueur au serveur et reçois le nouvel état de jeu'''
    url = 'https://python.gel.ulaval.ca/quoridor/api/jouer/'
    req = requests.post(
        url, data={'id': id_partie, 'type': type_coup, 'pos': position})
    data = req.json()
    if req.status_code == 200:
        if data.get('message') is not None:
            raise RuntimeError(data['message'])
        if data.get('gagnant') is not None:
            raise StopIteration(data['gagnant'])
        return data['état']
    raise ConnectionError(
        f"La requête vers {url} a échoué. (Code d'erreur: {req.status_code})")
