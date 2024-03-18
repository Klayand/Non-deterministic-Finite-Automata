# @Author : Zikai Zhou
# SPDX-License-Identifier: GPL-3.0-only

from collections import deque
from init import DFA


def parse_transition_table(file_path):
    """

    :param file_path: the input file path
    :return: the transition table
    """
    transitions = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # extract symbols list
        symbols = lines[0].strip().split('\t')[1:]

        # extract state and transition information
        for line in lines[1:]:
            items = line.strip().split('\t')
            initial_state = items[0].replace('*', '') if '*' in items[0] else items[0]

            for i, symbol in enumerate(symbols):
                if symbol == '$':
                    op = None
                else:
                    op = symbol

                next_states = items[i + 1]
                if next_states != '-':
                    state_set = set(next_states.split(','))
                    transitions[(initial_state, op)] = state_set
                elif next_states == '-':
                    transitions[(initial_state, op)] = set()

    return transitions


def get_file_content(file_path):
    """
    in order to get the basic information about the Non-Deterministic Finite Automata from the input file
    :param file_path: the input file path
    :return: start_state, final_state, state, alphabet, transition
    """
    with open(file_path, 'r') as f:
        data = f.read().split('\n')

        start_state = 'q0'
        final_state = {state.replace('\t', ' ').split(' ')[0][:-1] for state in data[1:] if '*' in state.split(' ')[0]}
        state = {state[:2] for state in data[1:]}
        alphabet = {state for state in data[0].replace('\t', ' ').split(' ')[1:]}
        transition = parse_transition_table(file_path)

        return start_state, final_state, state, alphabet, transition


def convert_nfa_to_dfa(nfa, par):
    """

    :param nfa: NFA object
    :param par: the arugmental parameter
    :return: the generated DFA object
    """
    dfa_start_state = frozenset([nfa.start_state])  # Start state of the DFA is a set containing the start state of the NFA
    dfa_states = [dfa_start_state]  # Set of states of the DFA, initially containing only the start state
    dfa_alphabet = nfa.alphabet  # Alphabet of the DFA is the same as the NFA
    dfa_transitions = {}  # Transition function of the DFA
    dfa_final_states = []  # Set of final states of the DFA

    unmarked_states = [dfa_start_state]  # Set of unmarked states, initially containing only the start state
    while unmarked_states:
        current_state_set = unmarked_states.pop(0)  # Take a state set from unmarked states as the current state set

        for symbol in dfa_alphabet:
            next_state_set = set()
            for state in current_state_set:
                if (state, symbol) in nfa.transitions:
                    next_state_set |= set(nfa.transitions[(state, symbol)])  # For each state in the current state set, find the next state set based on the transition function

            next_state_set = frozenset(next_state_set)  # Convert the next state set to an immutable set (frozenset)

            if next_state_set not in dfa_states:
                dfa_states.append(next_state_set)  # If the next state set is new, add it to the DFA states
                unmarked_states.append(next_state_set)  # Add the next state set to the unmarked states

            dfa_transitions[(current_state_set, symbol)] = next_state_set  # Record the transition from the current state set to the next state set via the symbol

        if any(state in nfa.final_states for state in current_state_set):
            dfa_final_states.append(current_state_set)  # If the current state set contains a final state of the NFA, add it to the DFA final states

    dfa = DFA(dfa_start_state, dfa_final_states, dfa_states, dfa_alphabet, dfa_transitions, par)
    return dfa


def convert_enfa_to_dfa(enfa, par):
    """

    :param enfa: ENFA object
    :param par: argumental parameter
    :return: generated DFA object
    """
    start_state = frozenset(enfa.epsilon_closure({enfa.start_state}))
    dfa_states = {start_state}
    dfa_transitions = {}
    queue = deque([start_state])

    # Convert ENFA to DFA using epsilon closure and move operations
    while queue:
        current_state = queue.popleft()

        for symbol in enfa.alphabet:
            next_state = frozenset(enfa.epsilon_closure(enfa.move(current_state, symbol)))

            if next_state:
                dfa_transitions[(current_state, symbol)] = next_state

                if next_state not in dfa_states:
                    dfa_states.add(next_state)
                    queue.append(next_state)

    dfa_final_states = set()
    for state in dfa_states:
        if enfa.has_accepting_state(state):
            dfa_final_states.add(state)

    dfa = DFA(start_state, dfa_final_states, dfa_states, enfa.alphabet, dfa_transitions, par)

    return dfa