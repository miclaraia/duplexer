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

    def split_duplex(self, n_per_sheet):
        npages = self.count_pages()
        pages = self._split_pages(npages, n_per_sheet)

        name = f'{self.name}-odd.pdf'
        f1 = os.path.join(self.outdir, name)
        name = f'{self.name}-even.pdf'
        f2 = os.path.join(self.outdir, name)

        self._dump_pages(f1, pages[0])
        self._dump_pages(f2, pages[1])

        return {'odd': f1, 'even': f2}

    def _add_blank_page(self, writer):
        box = self.pdf.getPage(0).mediaBox

        w = box.getWidth()
        h = box.getHeight()
        writer.addBlankPage(w, h)

    def _split_pages(self, npages, n_per_sheet):
        pages = [[], []]

        k = 0
        idx = 0
        for i in range(npages):
            if k == n_per_sheet:
                k = 0
                idx = 1 - idx

            pages[idx].append(i)
            k = k + 1

        while len(pages[0]) > len(pages[1]):
            pages[1].append('blank')

        return pages

    def _dump_pages(self, fname_out, pages):
        writer = pypdf.PdfFileWriter()

        for page in pages:
            if page == 'blank':
                self._add_blank_page(writer)
            else:
                writer.addPage(self.pdf.getPage(page))

        with open(fname_out, 'wb') as f:
            writer.write(f)

    def dump_even(self, npages):
        name = f'{self.name}-even.pdf'
        fname_out = os.path.join(self.outdir, name)

        pages = list(range(1, npages, 2))
        if npages % 2 != 0:
            pages += ['blank']

        self._dump_pages(fname_out, pages)
        return fname_out

    def dump_odd(self, npages):
        name = f'{self.name}-odd.pdf'
        fname_out = os.path.join(self.outdir, name)

        pages = list(range(0, npages, 2))
        self._dump_pages(fname_out, pages)
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
