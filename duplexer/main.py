import argparse
import string    
import random
import os
import shutil

from duplexer.cups_client import Cups, CupsOptions
from duplexer.pdf import PDF
from duplexer.config import Config


def run(config: Config):
    cups = Cups(config.printer)
    name = os.path.splitext(os.path.basename(config.file))[0]

    r = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    outdir = os.path.join('/tmp/duplexer', f'{name}-{r}')

    pdf = PDF(config.file, outdir)

    files = pdf.split_duplex(config.n_per_page)

    if not config.dry:
        options = CupsOptions.from_config(config)
        cups.print(files['even'], f'{name}-even', options)
        cups.print(files['odd'], f'{name}-odd', options.hold())

    if config.dry:
        print(files)
        input("Press Enter to continue...")

    shutil.rmtree(outdir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('printer')
    parser.add_argument('--dry', action='store_true')
    parser.add_argument('--double-per-page', action='store_true')

    args = parser.parse_args()

    config = Config()
    config.dry = args.dry
    if args.double_per_page:
        config.n_per_page = 2

    config.printer = args.printer
    config.file = args.file

    try:
        run(config)
    except Exception:
        import pdb; import traceback
        traceback.print_exc()
        pdb.post_mortem()
