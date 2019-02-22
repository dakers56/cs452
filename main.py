import sys


class CliArgs:
    def __init__(self, args):
        arg_len = len(args)
        if (arg_len < 5):
            raise RuntimeError("Did not provide enough arguments. Only %s were provided." % arg_len)
        self.b = args[1]
        self.m = args[2]
        self.x = args[3]
        self.i = args[4]

    def cli_args(self):
        """ Return arguments given to command line in expected order.
        """
        return self.b, self.m, self.x, self.i

    def __str__(self):
        return "b: %s; m: %s; x: %s; i: %s" % self.cli_args()


if __name__ == "__main__":
    print("Testing command line args. Input: %s" % CliArgs(sys.argv))
