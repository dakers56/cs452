from main import Period, DFAState, DFA, RightToLeftString


def __make_seq(mod, base=10):
    seq = []
    for pow in range(10):
        seq += [(base ** pow) % mod]
    return seq


def test_period():
    mod = 22
    seq = __make_seq(mod)
    period = Period(seq)
    assert (period.i_seg == [1])
    assert (period.r_seg == [10, 12])
    assert (period.length == 2)
    assert (period.val == 10)

    mod = 25
    seq = __make_seq(mod)
    period = Period(seq)
    assert (period.i_seg == [1, 10])
    assert (period.r_seg == [0])
    assert (period.length == 1)
    assert (period.val == 0)

    mod = 37
    seq = __make_seq(mod)
    period = Period(seq)
    assert (period.i_seg == [])
    assert (period.r_seg == [1, 10, 26])
    assert (period.length == 3)
    assert (period.val == 1)


def __assert_for_dfa_states(n_states, states, state_index):
    assert (n_states == len(states))
    assert (n_states == len(state_index))
    for s in states:
        assert ((s.i, s.j) in state_index)
        for _, s_t in s.tran_func.items():
            assert s_t in state_index


def __assert_for_dfa(n_states, state_index, dfa):
    dfa_n_states = 0
    for i in range(len(dfa.states)):
        for j in range(len(dfa.states[i])):
            dfa_n_states += 1
    assert (n_states == dfa_n_states)
    assert (n_states == len(state_index))
    for i in range(len(dfa.states)):
        for j in range(len(dfa.states[i])):
            assert ((dfa.states[i][j].i, dfa.states[i][j].j) in state_index)
            for _, s_t in dfa.states[i][j].tran_func.items():
                assert s_t in state_index


def test_dfa_states():
    mod = 4
    seq = [(10 ** p) % mod for p in range(2 * (mod + 1))]
    b = 10

    period = Period(seq)
    print("Period for division modulo %s: %s" % (mod, period))
    n_states = 0
    states = set()
    state_index = set()
    w = len(period.i_plus_r_seg)
    for i in range(w):
        for j in range(mod):
            this_state = DFAState(i=i, j=j, m=mod, b=10, period=period)
            states.add(this_state)
            state_index.add((i, j))
            n_states += 1
            print("DFA state with i = %s, j = %s, b = %s, mod = %s: %s" % (i, j, b, mod, this_state))

            print("Number of states: %s" % n_states)

    __assert_for_dfa_states(n_states, states, state_index)


def test_dfa():
    mod = 4
    seq = [(10 ** p) % mod for p in range(2 * (mod + 1))]
    base = 10
    dfa = DFA(mod=mod, base=base, seq=seq)

    period = Period(seq)
    w = 3
    states = set()
    state_index = set()
    for i in range(w):
        for j in range(mod):
            this_state = DFAState(i=i, j=j, m=mod, b=10, period=period)
            states.add(this_state)
            state_index.add((i, j))

    __assert_for_dfa(12, state_index, dfa)

def test_rls():
    test_str = "987654321"
    rls = RightToLeftString(test_str)
    for i in range(len(test_str)):
        assert (rls.__next__() == int(test_str[len(test_str) - i - 1]))

    test_str = "12345"
    read = []
    rls = RightToLeftString(test_str)
    for i in rls:
        read.append(i)
    assert (read == [5,4,3,2,1])


