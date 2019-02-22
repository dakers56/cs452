import sys


class CliArgs:
    def __init__(self, args):
        if(args == None):
            raise RuntimeError("'args' was None. Make sure you provide arguments")
        arg_len = len(args)
        if (arg_len < 5):
            raise RuntimeError("Did not provide enough arguments. Only %s were provided." % arg_len)
        try:
            self.b = int(args[1])
            self.m = int(args[2])
            self.x = int(args[3])
            self.i = int(args[4])
        except ValueError as v:
            raise ValueError("Provided invalid arguments. Ensure that they are integers: %s" % args)

    def cli_args(self):
        """ Return arguments given to command line in expected order.
        """
        return self.b, self.m, self.x, self.i

    def __str__(self):
        return "b: %s; m: %s; x: %s; i: %s" % self.cli_args()


if __name__ == "__main__":
    print("Testing command line args. Input: %s" % CliArgs(sys.argv))
