import click

from core import save, xor
from gui import main as gui_main
from timer import Timer


@click.group()
def main():
    pass


@main.command()
def gui():
    gui_main()


@main.command()
@click.argument("image_path")
@click.argument("key_path")
@click.argument("path_to_result")
def cli(image_path, key_path, path_to_result):
    with Timer():
        click.echo("Encrypting.")
        result_image = xor(image_path, key_path)
        click.echo("Encrypted.")
        actual_path_to_result = save(path_to_result, result_image)
        click.echo(f"Saved as {actual_path_to_result}")
