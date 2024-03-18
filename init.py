import graphviz
from graphviz import Digraph
from collections import deque


class NFA:
    def __init__(self, start_state, final_states, states, alphabet, transitions, par):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.par = par

    def print_nfa_table(self):
        print("State\t\t", end="")
        for symbol in self.alphabet:
            print(symbol + "\t\t", end="")
        print()

        for state in self.states:
            print(state + "\t\t", end="")
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), set())
                print(str(next_states) + "\t\t", end="")
            print()

    def visualize(self):
        # create Graphviz object
        graph = graphviz.Digraph(format='png')

        # add NFA state node
        for state in self.states:
            if state in self.final_states:
                graph.node(state, shape='doublecircle')
            else:
                graph.node(state)

        # add NFA transition edge
        for transition, next_states in self.transitions.items():
            state, symbol = transition
            for next_state in next_states:
                graph.edge(state, next_state, label=symbol)

        # render and save this file
        file_name = self.par.file_path.split("/")[-1].split(".")[0]
        graph.render(f'{self.par.output_path}/NFA_{file_name}', view=True)


class ENFA:
    def __init__(self, start_state, final_states, states, alphabet, transitions, par):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.par = par

    def epsilon_closure(self, states):
        closure = set(states)
        queue = deque(states)

        while queue:
            current_state = queue.popleft()

            epsilon_moves = self.transitions.get((current_state, None), set())
            for next_state in epsilon_moves:
                if next_state not in closure:
                    closure.add(next_state)
                    queue.append(next_state)

        return closure

    def move(self, states, symbol):
        next_states = set()

        for state in states:
            transitions = self.transitions.get((state, symbol), set())
            next_states.update(transitions)

        return next_states

    def has_accepting_state(self, states):
        return bool(states.intersection(self.final_states))

    def print_enfa_table(self):
        print("State\t\t", end="")
        for symbol in self.alphabet:
            print(symbol + "\t\t", end="")
        print("ε\t\t")

        for state in self.states:
            print(state + "\t\t", end="")
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), set())
                print(str(next_states) + "\t\t", end="")
            epsilon_moves = self.transitions.get((state, None), set())
            print(str(epsilon_moves) + "\t\t")

    def visualize(self):
        dot = Digraph(comment='ENFA')

        for state in self.states:
            if state in self.final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state)

        dot.node('start', '', shape='none')
        dot.edge('start', self.start_state)

        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                if symbol is None:
                    dot.edge(state, next_state, label='ε')
                else:
                    dot.edge(state, next_state, label=symbol)


        file_name = self.par.file_path.split("/")[-1].split(".")[0]
        dot.render(f'{self.par.output_path}/ENFA_{file_name}', view=True)


class DFA:
    def __init__(self, start_state, final_states, states, alphabet, transitions, par):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.par = par

    def print_dfa_table(self):
        # 打印DFA的状态表头
        header = "State\t|\t"
        for symbol in self.alphabet:
            header += symbol + "\t|\t"
        header += "Accepting"
        print(header)

        # print DFA state table
        for state in self.states:
            row = str(state) + "\t|\t"
            for symbol in self.alphabet:
                next_state = self.transitions.get((state, symbol), None)
                row += str(next_state) + "\t|\t"
            is_accepting = state in self.final_states
            row += str(is_accepting)
            print(row)

    def visualize(self):
        # create Graphviz object
        graph = graphviz.Digraph(format='png')

        # add DFA state node
        for state in self.states:
            if state in self.final_states:
                graph.node(str(state)[9:-1], shape='doublecircle')
            else:
                graph.node(str(state)[9:-1])

        # add DFA transition edge
        for transition, next_state in self.transitions.items():
            current_state, symbol = transition
            graph.edge(str(current_state), str(next_state), label=symbol)

        # render and save this file
        file_name = self.par.file_path.split("/")[-1].split(".")[0]
        graph.render(f'{self.par.output_path}/DFA_{file_name}', view=True)