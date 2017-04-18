from automata import *

# Example NFA which accepts the language where words contain 010
# or have an odd number of 1's.
ex_nfa = NFA.from_table(
    alphabet=['0', '1'],
    transition_function=[
        #                0                    1
        ['q0',         ['q0', 'q1', 'q2'],  ['q1', 'q5']],
        ['q1',         ['q1', 'q2'],        'q1'        ],
        ['q2',         NFA.emptyset,        'q3'        ],
        ['q3',         'q4',                NFA.emptyset],
        [('q4', True), 'q4',                'q4'        ],
        [('q5', True), 'q5',                'q0'        ]
    ]
)

# DFA of the previous NFA
ex_dfa = DFA.from_table(
    alphabet = ['0', '1'],
    transition_function=[
        # NOTE: q dropped in state names for brevity;
        # state 135 is the state for the set {q1, q3, q5} from the NFA
        #          0        1
        [('0',    False),  '012',   '15'  ],
        [('012',  False),  '012',   '135' ],
        [('15',   True),   '125',   '01'  ],
        [('125',  True),   '125',   '013' ],
        [('013',  False),  '0124',  '15'  ],
        [('135',  True),   '1245',  '01'  ],
        [('01',   False),  '012',   '15'  ],
        [('1245', True),   '1245',  '0134'],
        [('0134', True),   '0124',  '145' ],
        [('0124', True),   '0124',  '1345'],
        [('145',  True),   '1245',  '014' ],
        [('014',  True),   '0124',  '145' ],
        [('1345', True),   '1245',  '014' ],
    ]
)

if __name__ == '__main__':
    print(ex_nfa.run(start_state='q0', input='11011'))
    print(ex_nfa.run(start_state='q0', input='01100010010010'))
    print(ex_nfa.run(start_state='q0', input='0110'))
    print(ex_nfa.run(start_state='q0', input='110101'))
    print(ex_nfa.run(start_state='q0', input='1001000111101111101'))

    print()

    print(ex_dfa.run(start_state='0', input='11011'))
    print(ex_dfa.run(start_state='0', input='01100010010010'))
    print(ex_dfa.run(start_state='0', input='0110'))
    print(ex_dfa.run(start_state='0', input='110101'))
    print(ex_dfa.run(start_state='0', input='1001000111101111101'))
