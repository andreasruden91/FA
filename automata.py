
class FA:
    """Shared functionality of FA"""
    def __init__(self):
        self.started = False
        self.final_states = set()
        self.trans_fun = {}
        self.alphabet = set()

    class __EmptySet:
        def __hash__(self):
            return hash('__EmptySet')
        def __eq__(self, other):
            return type(other) == type(self)
        def __repr__(self):
            return '∅'
    emptyset = __EmptySet()

    def _from_table(self, alphabet, transition_function, one_to_one):
        for row in transition_function:
            state = row[0]
            state = self.add_states(state)
            for i, symbol in enumerate(alphabet):
                to = row[i + 1]
                if type(to) != list:
                    to = [to]
                if one_to_one and len(to) != 1:
                    raise RuntimeError('Transition function needs to be one to one')
                self.add_transitions(state, symbol, to)

    def add_states(self, name):
        """Add state(s)
        
        :param name: list of NameType's OR NameType
            NameType: str of state name OR (str, boolean) denoting (state name, accepting?)
        :return: name of added state
        """
        self.started = False
        if type(name) == list:
            for state in name:
                return self.add_states(state)
        else:
            if type(name) == tuple:
                name, final = name
                if final:
                    self.final_states.add(name)
            if name not in self.trans_fun:
                self.trans_fun[name] = {}
            return name

    def add_transitions(self, state, symbol, to):
        self.started = False
        if type(to) == list:
            for elem in to:
                self.add_transitions(state, symbol, elem)
        else:
            self.alphabet.add(symbol)
            if symbol in self.trans_fun[state]:
                self.trans_fun[state][symbol].append(to)
            else:
                self.trans_fun[state][symbol] = [to]

    def run(self, start_state, input):
        self.start(start_state)
        for symbol in input:
            self.put(symbol)
        return self.accepting()

    def put(self, symbol):
        if symbol not in self.alphabet:
            raise RuntimeError('That is not a valid symbol')
        if not self.started or len(self.final_states) == 0:
            raise RuntimeError('Need to start and add final states')
        self._put(symbol)

    def start(self, start_state):
        raise NotImplementedError()

    def accepting(self):
        raise NotImplementedError()

    def _put(self, symbol):
        raise NotImplementedError()

class DFA(FA):
    def __init__(self):
        super().__init__()
        self.state = None
        self.dead = False

    def from_table(alphabet, transition_function):
        dfa = DFA()
        dfa._from_table(alphabet, transition_function, True)
        return dfa

    def start(self, start_state):
        assert start_state in self.trans_fun
        self.started = True
        self.state = start_state
        self.dead = False

    def accepting(self):
        return not self.dead and self.state in self.final_states

    def _put(self, symbol):
        if not self.dead:
            states = self.trans_fun[self.state][symbol]
            assert len(states) == 1
            self.state = states[0]
            if self.state == FA.emptyset:
                self.dead = True

class NFA(FA):
    """NFA and epsilon-NFA"""
    def __init__(self):
        super().__init__()
        self.threads = set()  # Threads that end up on the same state can be safely merged

    class __Epsilon:
        def __hash__(self):
            return hash('__Epsilon')
        def __eq__(self, other):
            return type(other) == type(self)
        def __repr__(self):
            return 'ε'
    epsilon = __Epsilon()

    def from_table(alphabet, transition_function):
        nfa = NFA()
        nfa._from_table(alphabet, transition_function, False)
        return nfa

    def start(self, start_state):
        assert start_state in self.trans_fun
        self.started = True
        self.threads = self.eclose(start_state)

    def accepting(self):
        for thread in self.threads:
            if thread in self.final_states:
                return True
        return False

    def _put(self, symbol):
        newthreads = set()
        for state in self.threads:
            for to in self.trans_fun[state][symbol]:
                if to != FA.emptyset:
                    newthreads |= self.eclose(to)
        self.threads = newthreads

    def eclose(self, state):
        """Epsilon closure on state"""
        if NFA.epsilon not in self.trans_fun[state]:
            return set([state])
        return set([state] + self.trans_fun[state][NFA.epsilon])
