# @Author : Zikai Zhou
# SPDX-License-Identifier: GPL-3.0-only

import argparse
from utils import *
from init import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', type=str, default='./inputs/example5.txt')
    parser.add_argument('--output-path', type=str, default='./saves')
    parser.add_argument('--mode', type=str, default='enfa',
                        help='choose nfa2dfa or enfa2dfa')  # $ represents \eplison
    parser.add_argument('--plot', type=bool, default=True)

    par = parser.parse_args()

    start_state, final_state, state, alphabet, transition = get_file_content(par.file_path)

    if par.mode == 'nfa':
        nfa = NFA(start_state, final_state, state, alphabet, transition, par)
        dfa = convert_nfa_to_dfa(nfa, par)

        nfa.print_nfa_table()
        if par.plot:
            nfa.visualize()
            dfa.visualize()

    elif par.mode == 'enfa':
        enfa = ENFA(start_state, final_state, state, alphabet, transition, par)
        dfa = convert_enfa_to_dfa(enfa, par)

        enfa.print_enfa_table()
        if par.plot:
            enfa.visualize()
            dfa.visualize()

    dfa.print_dfa_table()


if __name__ == '__main__':
    main()