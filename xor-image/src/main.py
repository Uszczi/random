import click

from src.core.xor import save, xor
from src.gui import main as gui_main
from src.utils import Timer


@click.group()
def main() -> None:
    pass


@main.command()
def gui() -> None:
    gui_main()


@main.command()
@click.argument("image_path", type=str)
@click.argument("key_path", type=str)
@click.argument("path_to_result", type=str)
def cli(image_path: str, key_path: str, path_to_result: str) -> None:
    with Timer():
        click.echo("Encrypting.")
        result_image = xor(image_path, key_path)
        click.echo("Encrypted.")
        actual_path_to_result = save(path_to_result, result_image)
        click.echo(f"Saved as {actual_path_to_result}")
