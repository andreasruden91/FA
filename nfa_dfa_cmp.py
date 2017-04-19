from test import ex_dfa, ex_nfa
import random, re

nfa = ex_nfa
nfa_start = 'q0'
dfa = ex_dfa
dfa_start = '0'
alphabet = [0, 1]
lenspan = (0, 30)
regexp = r'TODO'
do_nfa, do_dfa, do_re = True, True, False

for i in range(1, 10001):
    if i % 1000 == 0:
        print('Completed %d tests' % i)

    s = ''.join(str(e) for e in random.choices(alphabet, k=random.randint(lenspan[0], lenspan[1])))

    res = set()
    if do_nfa:
        res.add(nfa.run(start_state=nfa_start, input=s))
    if do_dfa:
        res.add(dfa.run(start_state=dfa_start, input=s))
    if do_re:
        re_res = re.fullmatch(regexp, s) != None
        res.add(re_res)

    if len(res) != 1:
        print('Error on input=%s after %d tests! %s %s %s' % (
            s, i,
            'NFA:' + str(nfa.accepting()) if do_nfa else '',
            'DFA:' + str(dfa.accepting()) if do_dfa else '',
            'RE:' + str(re_res) if do_re else ''
        ))
        break
