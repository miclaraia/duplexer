import cups
import argparse


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

    def print(self, fname, title, hold=True):
        options = {}
        if hold:
            options['job-hold-until'] = 'indefinite'

        self.conn.printFile(self.printer, fname, title, options)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()

    c = Cups('Home2')
    c.open()
    c.print(args.file, 'test')

if __name__ == '__main__':
    main()
