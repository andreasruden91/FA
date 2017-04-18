from test import ex_dfa, ex_nfa
import random

nfa = ex_nfa
nfa_start = 'q0'
dfa = ex_dfa
dfa_start = '0'
alphabet = [0, 1]
lenspan = (0, 30)

for i in range(1, 10001):
    if i % 1000 == 0:
        print('Completed %d tests' % i)

    s = ''.join(str(e) for e in random.choices(alphabet, k=random.randint(lenspan[0], lenspan[1])))

    nfa.run(start_state=nfa_start, input=s)
    dfa.run(start_state=dfa_start, input=s)

    if nfa.accepting() != dfa.accepting():
        print('Error! NFA:', nfa.accepting(), ', but DFA:', dfa.accepting(),
              'for input s=', s)
        break
