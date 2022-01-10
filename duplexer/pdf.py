import PyPDF2 as pypdf
import ghostscript
import os
import math
import argparse
from pathlib import Path


class PDF:

    def __init__(self, fname, outdir):
        self.fname = fname
        self.outdir = outdir

        Path(outdir).mkdir(parents=True, exist_ok=True)

        self._pdf = None
        self._stream = None

    @property
    def name(self):
        fname = os.path.basename(self.fname)
        name = os.path.splitext(fname)[0]
        return name

    @property
    def pdf(self):
        if self._pdf is None:
            self.open()

        return self._pdf

    def open(self):
        self._stream = open(self.fname, 'rb')
        self._pdf = pypdf.PdfFileReader(self._stream)

    def close(self):
        self._stream.close()

    def count_pages(self):
        return self.pdf.getNumPages()

    def split_duplex(self):
        npages = self.count_pages()
        f1 = self.dump_even(npages)
        f2 = self.dump_odd(npages)

        return {'even': f1, 'odd': f2}

    def dump_even(self, npages):
        name = f'{self.name}-even.pdf'
        fname_out = os.path.join(self.outdir, name)

        pages = list(reversed(range(1, npages, 2)))

        writer = pypdf.PdfFileWriter()

        if npages % 2 != 0:
            page = self.pdf.getPage(0)
            box = self.pdf.getPage(0).mediaBox

            w = box.getWidth()
            h = box.getHeight()
            writer.addBlankPage(w, h)

        for page in pages:
            writer.addPage(self.pdf.getPage(page))

        with open(fname_out, 'wb') as f:
            writer.write(f)

        return fname_out

    def dump_odd(self, npages):
        name = f'{self.name}-odd.pdf'
        fname_out = os.path.join(self.outdir, name)

        pages = list(reversed(range(0, npages, 2)))

        writer = pypdf.PdfFileWriter()

        for page in pages:
            writer.addPage(self.pdf.getPage(page))

        with open(fname_out, 'wb') as f:
            writer.write(f)

        return fname_out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('outdir')

    args = parser.parse_args()

    pdf = PDF(args.file, args.outdir)
    pdf.split_duplex()


if __name__ == '__main__':
    main()
