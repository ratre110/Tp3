'''Contient l'algorithme minimax pour jouer au Quoridor'''

from graphe import construire_graphe
from copy import deepcopy
import networkx as nx
import quoridor


class Node(object):
    '''
    Représente un noeud d'arbre pour l'algorithme minimax.

    Attributes:
        depth (int): Représente la profondeur du noeud dans l'arbre (0+).
        maximizingPlayer (bool): True si le noeud est celui du joueur cherchant à maximiser.
        state (dict): État du jeu correspondant au noeud.
        graphe: graphe networkx de l'état de jeu
        value (int): Valeur du noeud selon la métrique utilisée (ici delta).
        children (list): Liste des enfants du noeuds.
        descendants (int): Nombre de descendants que le noeud doit avoir
    '''

    def __init__(self, depth, maximizingPlayer, state, value=0):

        self.depth = depth
        self.maximizingPlayer = maximizingPlayer
        self.state = state
        self.value = value
        self.graphe = construire_graphe(
            [player['pos'] for player in self.state['joueurs']],
            self.state['murs']['horizontaux'],
            self.state['murs']['verticaux']
        )
        self.children = []
        self.create_children()

    def create_children(self):
        if self.depth > 0:
            walls = self.available_wall_positions()
            for pos in walls["horizontaux"]:
                new_state = self.new_game_state(pos, 'MH')
                if new_state is not None:
                    if self.calcValue(new_state) != 0:
                        self.children.append(Node(
                            self.depth - 1,
                            not (self.maximizingPlayer),
                            new_state,
                            self.calcValue(new_state)
                        ))

            for pos in walls["verticaux"]:
                new_state = self.new_game_state(pos, 'MV')
                if new_state is not None:
                    if self.calcValue(new_state) != 0:
                        self.children.append(Node(
                            self.depth - 1,
                            not (self.maximizingPlayer),
                            new_state,
                            self.calcValue(new_state)
                    ))

            new_state_pos = self.new_game_state(self.best_movement(), 'D')
            self.children.append(Node(
                self.depth - 1,
                not (self.maximizingPlayer),
                new_state_pos,
                self.calcValue(new_state_pos, bias=.1)
            ))

    def new_game_state(self, position, operation):
        '''
        Retourne un nouvel état de jeu après le changement passé en argument, None si le nouvel
        état est invalide.
        '''
        if operation != 'D':
            graphe = deepcopy(self.graphe)
            if not self.blocks_player(graphe, position, operation):
                new_state = deepcopy(self.state)
                if operation == 'MH':
                    new_state["murs"]["horizontaux"].append(position)
                elif operation == 'MV':
                    new_state["murs"]["verticaux"].append(position)
                return new_state
            else:
                new_state = None
        else:
            new_state = deepcopy(self.state)
            if self.maximizingPlayer:
                new_state["joueurs"][0]["pos"] = position
            else:
                new_state["joueurs"][1]["pos"] = position
        return new_state

    def calcValue(self, state, bias=0):
        '''Calcule la valeur selon la différence des deltas'''
        value = 0

        if not self.maximizingPlayer:
            bias *= -1

        graphe = construire_graphe(
            [player['pos'] for player in state['joueurs']],
            state['murs']['horizontaux'],
            state['murs']['verticaux']
        )
        pos_1 = state["joueurs"][0]["pos"]
        pos_2 = state["joueurs"][1]["pos"]
        # Si gagné
        if pos_1[1] == 9:
            value = 1000
        elif pos_2[1] == 1:
            value = -1000
        else:
            delta_1 = len(nx.shortest_path(
                self.graphe, pos_2, 'B2')) - len(nx.shortest_path(self.graphe, pos_1, 'B1'))
            delta_2 = len(nx.shortest_path(
                graphe, pos_2, 'B2')) - len(nx.shortest_path(graphe, pos_1, 'B1'))
            value = delta_2 - delta_1
        return value + bias

    def available_wall_positions(self):
        '''
        Retourne un dictionnaire contenant un liste de positions de murs disponibles
        pour chaque orientation
        '''
        horizontal_positions = [(x, y) for x in range(1, 9) # 9
                                for y in range(2, 10)] # 10
        vertical_positions = [(x, y) for x in range(2, 10) # 10
                              for y in range(1, 9)] # 9

        # Horizontaux invalides
        for position in self.state["murs"]["horizontaux"]:
            pos_list = [
                position,
                (position[0] - 1, position[1]),
                (position[0] + 1, position[1])
            ]
            position_ver = (position[0] + 1, position[0] - 1)
            for pos in pos_list:
                try:
                    horizontal_positions.remove(pos)
                except ValueError:
                    pass
            try:
                vertical_positions.remove(position_ver)
            except ValueError:
                pass

        # Verticaux invalides
        for position in self.state["murs"]["verticaux"]:
            pos_list = [
                position,
                (position[0], position[1] - 1),
                (position[0], position[1] + 1)
            ]
            position_hor = (position[0] - 1, position[0] + 1)
            for pos in pos_list:
                try:
                    vertical_positions.remove(pos)
                except ValueError:
                    pass
            try:
                horizontal_positions.remove(position_ver)
            except ValueError:
                pass

        return {"horizontaux": horizontal_positions, "verticaux": vertical_positions}

    def best_movement(self):
        '''Revoie le tuple du meilleur déplacement que le joueur peut effectuer'''

        if self.maximizingPlayer:
            return nx.shortest_path(self.graphe, self.state["joueurs"][0]["pos"], 'B1')[1]
        else:
            return nx.shortest_path(self.graphe, self.state["joueurs"][1]["pos"], 'B2')[1]

    def blocks_player(self, graphe, position, orientation):
        '''Retourne True si le placement de mur pour l'état bloque un joueur'''
        x, y = position

        if orientation == 'MH':
            graphe.remove_edge((x, y-1), (x, y))
            graphe.remove_edge((x, y), (x, y-1))
            graphe.remove_edge((x+1, y-1), (x+1, y))
            graphe.remove_edge((x+1, y), (x+1, y-1))

        elif orientation == 'MV':
            graphe.remove_edge((x-1, y), (x, y))
            graphe.remove_edge((x, y), (x-1, y))
            graphe.remove_edge((x-1, y+1), (x, y+1))
            graphe.remove_edge((x, y+1), (x-1, y+1))

        is_invalid = False
        if not nx.has_path(graphe, self.state["joueurs"][0]["pos"], 'B1'):
            is_invalid = True
        if not nx.has_path(graphe, self.state["joueurs"][1]["pos"], 'B2'):
            is_invalid = True

        return is_invalid


def minimax(node, depth, alpha, beta, maximizingPlayer):

    if depth == 0  or abs(node.value) >= 1000:
        return node.value, node.state


    if maximizingPlayer:
        maxEval = float("-inf")
        for child in node.children:
            val, state = minimax(child, depth - 1, alpha, beta, False)
            print(val)
            if maxEval < val:
                maxEval = val
                maxState = state
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return maxEval, maxState

    else:
        minEval = float("+inf")
        for child in node.children:
            val, state = minimax(child, depth - 1, alpha, beta, True)
            print(val)
            if minEval > val:
                minEval = val
                minState = state
            beta = min(beta, val)
            if beta <= alpha:
                break
        return minEval, minState

def calc_best_move(currentState, player):
    depth = 2
    if player == 1:
        maximizingPlayer = True
    else:
        maximizingPlayer = False

    node = Node(depth, maximizingPlayer, currentState)
    new_state = minimax(node, depth, float("-inf"),
                        float("+inf"), maximizingPlayer)
    return new_state


def main():
    state = {
        "joueurs": [
            {"nom": "idul", "murs": 9, "pos": (7, 4)},
            {"nom": "automate", "murs": 10, "pos": (5, 7)}
        ],
        "murs": {
            "horizontaux": [(4, 7)],
            "verticaux": []
        }
    }
    new_state = calc_best_move(state, 1)
    print(new_state)


if __name__ == '__main__':
    main()
