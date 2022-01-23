import cups
import argparse


class CupsOptions:
    def __init__(self):
        self.options = {}

    @classmethod
    def from_config(cls, config):
        self = cls()
        if config.n_per_page > 1:
            self.n_per_page(config.n_per_page)

        return self

    def reset(self):
        self.options = {}
        return self

    def set(self, k, v):
        self.options[k] = v
        return self

    def unset(self, k):
        if k in self.options:
            del self.options[k]
        return self

    def get(self):
        return self.options.copy()

    ###########################################################################

    def hold(self, hold=True):
        key = 'job-hold-until'

        if hold:
            self.set(key, 'indefinite')
        else:
            self.unset(key)

        return self

    def n_per_page(self, n):
        self.set('number-up', str(n))
        return self


class Cups:
    def __init__(self, printer):
        self.printer = printer

        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self.open()
        return self._conn

    def open(self):
        self._conn = cups.Connection()

    def close(self):
        pass

    def print(self, fname, title, options:CupsOptions=None):
        if options is None:
            options = CupsOptions()
        self.conn.printFile(self.printer, fname, title, options.get())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()

    c = Cups('Home2')
    c.open()
    c.print(args.file, 'test')

if __name__ == '__main__':
    main()
