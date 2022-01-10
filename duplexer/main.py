import argparse
import string    
import random
import os
import shutil

from duplexer.cups_client import Cups
from duplexer.pdf import PDF


def run(fname, printer, dry):
    cups = Cups(printer)
    name = os.path.splitext(os.path.basename(fname))[0]

    r = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    outdir = os.path.join('/tmp/duplexer', f'{name}-{r}')

    pdf = PDF(fname, outdir)

    files = pdf.split_duplex()

    if not dry:
        cups.print(files['even'], f'{name}-even', hold=False)
        cups.print(files['odd'], f'{name}-odd', hold=True)

    if dry:
        input("Press Enter to continue...")

    shutil.rmtree(outdir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('printer')
    parser.add_argument('--dry', action='store_true')

    args = parser.parse_args()
    run(args.file, args.printer, args.dry)
