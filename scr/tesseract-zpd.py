import click

from main import ocr_by_tesseract, preview_files
from OCR_by_tesseract import OCR
from Type_Alias import Path

# this file is for turning main.py into command line tool by click package.
# just decorating core functions in main.py


@click.group()
def cli():
    pass


@cli.command(help="preview files that will be read by ocr. The first argument must be a path.")
@click.argument("path", nargs=1, type=click.Path(exists=True))
@click.option(
    "-e", "--ext", type=str, default="png", help="file extension without period mark'.'. the default uses 'png'."
)
def preview(path: str, ext: str):
    preview_files(path, ext)


@cli.command(help="ocr file(s in a directory) and save the result in a text file. The first argument must be a path.")
@click.argument("path", nargs=1, type=click.Path(exists=True))
@click.option("-e", "--ext", type=str, help="file extension without period mark'.'. the default uses 'png'")
@click.option("-l", "--lang", type=str, default="eng", help="language. the default uses 'eng'=English.")
@click.option(
    "-p",
    "--psm",
    type=click.IntRange(3, 13),
    default=6,
    help="page segmentation mode. default used 6.",
)
@click.option(
    "-d",
    "--dirout",
    "dir_out",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="path of the output directory. the default uses the same directory input as the argument.",
)
@click.option(
    "-n",
    "--name",
    "name",
    type=str,
    default=None,
    help="file name of the output file. accepts both formats 'name_out.txt' and 'name_out'. the default uses the file name if input is single zip or pdf, and the name of the first file (like 005.png -> 005.txt) in the directory if image files are provided.",
)
@click.option(
    "-a",
    "--auto",
    type=bool,
    is_flag=True,
    help="whether to name output text file after its parent directory. Used only when directory path is provided and name option is not explicitly provided.",
)
def ocr(path: str, ext: str, lang: str, psm: int, dir_out: str | None, name: str | None, auto: bool):
    ocr = OCR(lang=lang, layout=psm)
    dir_out_new: Path | None = Path(dir_out) if dir_out is not None else None
    path_in = Path(path)
    name_new: str | None = path_in.stem if auto and name is None and path_in.is_dir() else name
    ocr_by_tesseract(ocr=ocr, file_or_dir=path, ext=ext, dir_out=dir_out_new, name_out=name_new)


if __name__ == "__main__":
    cli()
