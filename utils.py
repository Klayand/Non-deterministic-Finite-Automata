# @Author : Zikai Zhou
# SPDX-License-Identifier: GPL-3.0-only

from collections import deque
from init import DFA


def parse_transition_table(file_path):
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
    with open(file_path, 'r') as f:
        data = f.read().split('\n')

        start_state = 'q0'
        final_state = {state.replace('\t', ' ').split(' ')[0][:-1] for state in data[1:] if '*' in state.split(' ')[0]}
        state = {state[:2] for state in data[1:]}
        alphabet = {state for state in data[0].replace('\t', ' ').split(' ')[1:]}
        transition = parse_transition_table(file_path)

        return start_state, final_state, state, alphabet, transition


def convert_nfa_to_dfa(nfa, par):
    dfa_start_state = frozenset([nfa.start_state])
    dfa_states = [dfa_start_state]
    dfa_alphabet = nfa.alphabet
    dfa_transitions = {}
    dfa_final_states = []

    unmarked_states = [dfa_start_state]
    while unmarked_states:
        current_state_set = unmarked_states.pop(0)

        for symbol in dfa_alphabet:
            next_state_set = set()
            for state in current_state_set:
                if (state, symbol) in nfa.transitions:
                    next_state_set |= set(nfa.transitions[(state, symbol)])

            next_state_set = frozenset(next_state_set)

            if next_state_set not in dfa_states:
                dfa_states.append(next_state_set)
                unmarked_states.append(next_state_set)

            dfa_transitions[(current_state_set, symbol)] = next_state_set

        if any(state in nfa.final_states for state in current_state_set):
            dfa_final_states.append(current_state_set)

    dfa = DFA(dfa_start_state, dfa_final_states, dfa_states, dfa_alphabet, dfa_transitions, par)
    return dfa


def convert_enfa_to_dfa(enfa, par):
    start_state = frozenset(enfa.epsilon_closure({enfa.start_state}))
    dfa_states = {start_state}
    dfa_transitions = {}
    queue = deque([start_state])

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