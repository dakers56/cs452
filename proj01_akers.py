#!/usr/bin/python3
# Devon Akers; UID: 116411837
import sys


class CliArgs:
    def __init__(self, args):
        if (args == None):
            raise RuntimeError("'args' was None. Make sure you provide arguments")
        arg_len = len(args)
        if (arg_len < 5):
            raise RuntimeError("Did not provide enough arguments. Only %s were provided." % arg_len)
        try:
            self.b = int(args[1])
            self.m = int(args[2])
            self.i = int(args[3])
            self.x = self.read_x(args)
        except ValueError as v:
            raise ValueError("Provided invalid arguments. Ensure that they are integers: %s" % args)

    def read_x(self, args):
        x_str = []
        for s in args[4:]:
            x_str.append(s)
        return x_str

    def x_as_rls(self, x):
        return RightToLeftString(x)

    def cli_args(self):
        """ Return arguments given to command line in expected order.
        """
        return self.b, self.m, self.i, self.x

    def __str__(self):
        return "b: %s; m: %s; i: %s; x: %s" % self.cli_args()


class Period:
    def __init__(self, seq):
        self.seq = seq
        self.length, self.val, self.r_seg_start = self.__period(self.seq)
        self.i_seg = seq[:self.r_seg_start]
        self.r_seg = seq[self.r_seg_start:self.r_seg_start + self.length]
        self.i_plus_r_seg = self.i_seg + self.r_seg

    def __period(self, seq):
        found = {}
        for i, j in enumerate(seq):
            if j in found:
                return i - found[j], j, found[j]
            found[j] = i
        raise RuntimeError("No repeating sequence found.")

    def __str__(self, *args, **kwargs):
        return "Seq: %s; Initial segment: %s; Repeating segment: %s; Value: %s; Length: %s" % (
            self.seq, self.i_seg, self.r_seg, self.val, self.length)


class RightToLeftString:
    def __init__(self, normal_str):
        self.str_stack = [int(i) for i in normal_str]

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.str_stack) > 0:
            return self.str_stack.pop()
        else:
            raise StopIteration()




class DFA:
    def __init__(self, mod, base, accept_val):
        self.m = mod
        self.base = base
        self.period = Period(self.__gen_seq())
        self.w = len(self.period.i_plus_r_seg)
        self.accept_val = accept_val
        states_ = []
        for i in range(self.w):
            states_.append([])
            for j in range(self.m):
                states_[i].append(
                    DFAState(i=i, j=j, b=self.base, m=self.m, accept_val=self.accept_val, period=self.period))
        self.states = states_

    def __str__(self):
        _str = ""
        for i in range(self.w):
            for j in range(self.m):
                _str += str(self.state(i, j)) + "\n"
        return _str + str(self.n_states())

    def __gen_seq(self):
        return [(self.base ** p) % self.m for p in range(2 * (self.m + 1))]

    def n_states(self):
        n = 0
        for i in range(self.w):
            for j in range(self.m):
                n += 1
        return n

    def state(self, i, j):
        return self.states[i][j]

    def lt_b(self, x):
        """ Returns whether x is less than the base provided. If not, we may need to examine the next digit"""
        return int(x) < self.base

    def read(self, string):
        this_state = self.states[0][0]  # begin at start state
        states_read = []
        for d in string:
            states_read.append(this_state)
            next_i, next_j = this_state.tran_func[int(d)][0], this_state.tran_func[int(d)][1]
            this_state = self.state(next_i, next_j)
        states_read.append(this_state)
        return states_read


class DFAState:
    def __init__(self, i, j, b, m, accept_val, period=None):
        self.i = i
        self.j = j
        self.b = b
        self.m = m
        self.accept_val = accept_val
        if period is not None:
            self.period = period
        else:
            self.period = Period([(self.b ** p) % mod for p in range(2 * (mod + 1))])
        self.tran_func = {d: self.__calc_delta_of(d) for d in range(b)}

    def delta_of(self, d):
        return self.tran_func[d]

    def __str__(self):
        return self.i_j_str()

    def i_j_str(self):
        return "(%s, %s)" % (self.i, self.j)

    def tf_str(self):
        str_ = '['
        for d in range(self.b - 1):
            str_ += "(%s, %s), " % (self.delta_of(d))
        str_ += "(%s, %s)]" % (self.delta_of(self.b - 1))
        return str_

    def __next_in_init_seg(self):
        return self.i < len(self.period.i_seg) - 1

    def next_in_i_seg(self):
        return self.i + 1

    def next_in_r_seg(self):
        return self.period.r_seg_start + ((self.i + 1) % len(self.period.r_seg))

    def current_period_val(self, in_i_seg=False):
        return self.period.i_plus_r_seg[self.i]

    def next_classifier_val(self, digit):
        res = (self.j + (digit * self.current_period_val())) % self.m
        return (self.j + (digit * self.current_period_val())) % self.m

    def __calc_delta_of(self, d):
        if self.__next_in_init_seg():
            self.next_in_r_seg(), self.next_classifier_val(digit=d)
            res = self.i + 1, self.next_classifier_val(digit=d)
            return self.i + 1, self.next_classifier_val(digit=d)
        res = self.next_in_r_seg(), self.next_classifier_val(digit=d)
        return self.next_in_r_seg(), self.next_classifier_val(digit=d)

    def REJECT(self):
        return "reject"

    def ACCEPT(self):
        return "accept"

    def is_accept(self):
        return self.j == self.accept_val

    def ar_str(self):
        return self.ACCEPT() if self.is_accept() else self.REJECT()


class DFAStateList:
    def __init__(self, dfa_states):
        self.dfa_states = dfa_states

    def __str__(self):
        str_ = '[' + str(self.dfa_states[0])
        for s in self.dfa_states[1:]:
            str_ += ', ' + str(s.i_j_str())
        return str_ + ']'


class CliOutput:
    def __init__(self, dfa, states_read):
        self.dfa = dfa
        self.states_read = states_read

    def init_seg(self):
        return str(self.dfa.period.i_seg)

    def r_seg(self):
        return str(self.dfa.period.r_seg)

    def states_and_deltas(self):
        str_ = ''
        for i in range(len(self.dfa.states)):
            for j in range(len(self.dfa.states[i])):
                this_state = self.dfa.state(i, j)
                str_ += this_state.i_j_str() + " " +  this_state.tf_str() + "\n"
        return str_.rstrip()

    def n_states(self):
        return str(self.dfa.n_states())

    def states_read_str(self):
        return str(DFAStateList(self.states_read))

    def final_state(self):
        return self.states_read[len(self.states_read) - 1]

    def __str__(self):
        return self.init_seg() + "\n" + self.r_seg() + "\n" + self.states_and_deltas() + "\n" \
               + self.n_states() + "\n" + self.states_read_str() + "\n" + self.final_state().ar_str()


if __name__ == "__main__":
    cli_args = CliArgs(sys.argv)
    dfa_4 = DFA(mod=cli_args.m, base=cli_args.b, accept_val=cli_args.i)
    states_read = dfa_4.read(cli_args.x)
    output = CliOutput(dfa_4, states_read)
    print(output)
