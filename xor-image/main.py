import click
from gui import main as gui_main
from core import xor, save
from timer import Timer


@click.group()
def main():
    pass


@main.command()
def gui():
    gui_main()


@main.command()
@click.argument("image")
@click.argument("key_image")
@click.argument("result_image")
def cli(image, key_image, result_image):
    with Timer():
        click.echo("Encrypting.")
        result = xor(image, key_image)
        click.echo("Encrypted.")
        save(result_image, result)
        click.echo(f"Saved as {result_image}")
