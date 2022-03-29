# Author: Snow Yang
# Date  : 2022/03/21

import os
from typing import List, Any

import pathlib

import click
import tabulate

from rich.console import Console
from rich.table import Table
from rich import box

from mdev.project import initialise_project, import_project, get_known_libs, deploy_project, sync_project
from mdev.project._internal import git_utils

@click.command()
@click.option(
    "--create-only", 
    "-c", 
    is_flag=True, 
    show_default=True, 
    help="Create a program without fetching mxos."
)
@click.argument("path", type=click.Path(resolve_path=True))
def new(path: str, create_only: bool) -> None:
    """Creates a new MXOS project at the specified path.

    Arguments:

        PATH: Path to the destination directory for the project. Will be created if it does not exist.

    Example:

        $ mdev new helloworld
    """
    click.echo(f"Creating a new MXOS program at path '{path}'.")
    if not create_only:
        click.echo("Downloading mxos and adding it to the project.")
        click.echo("This may take a long time, please be patient 😊, you can have a cup fo tea 🍵")

    initialise_project(pathlib.Path(path), create_only)
    
@click.command()
@click.argument("url")
@click.argument("path", type=click.Path(), default="")
@click.option(
    "--skip-resolve-libs",
    "-s",
    is_flag=True,
    show_default=True,
    help="Skip resolving program component dependencies after cloning.",
)
def import_(url: str, path: Any, skip_resolve_libs: bool) -> None:
    """Clone an MXOS project and component dependencies.

    Arguments:

        URL : The git url of the remote project to clone.

        PATH: Destination path for the clone. If not given the destination path is set to the project name in the cwd.

    Example:

        $ mdev import helloworld
    """
    click.echo(f"Cloning MXOS program '{url}'")
    if not skip_resolve_libs:
        click.echo("Resolving program component dependencies ...")
        click.echo("This may take a long time, please be patient 😊, you can have a cup fo tea 🍵")

    if path:
        click.echo(f"Destination path is '{path}'")
        path = pathlib.Path(path)

    dst_path = import_project(url, path, not skip_resolve_libs)
    if not skip_resolve_libs:
        libs = get_known_libs(dst_path)
        _print_dependency_table(libs, dst_path)

@click.command()
@click.argument("path", type=click.Path(), default=os.getcwd())
@click.option(
    "--force",
    "-f",
    is_flag=True,
    show_default=True,
    help="Forces checkout of all component repositories at specified commit in the .component file, overwrites local changes.",
)
def deploy(path: str, force: bool) -> None:
    """Checks out MXOS program component dependencies at the revision specified in the ".component" files.

    Ensures all dependencies are resolved and the versions are synchronised to the version specified in the component
    reference.

    Arguments:
    
        PATH: Path to the MXOS project [default: CWD]

    Example:

        $ mxos deploy
    """
    click.echo("Checking out all componets to revisions specified in .component files. Resolving any unresolved componets.")
    click.echo("This may take a long time, please be patient 😊, you can have a cup fo tea 🍵")
    root_path = pathlib.Path(path)
    deploy_project(root_path, force)
    libs = get_known_libs(root_path)
    _print_dependency_table(libs, root_path)

@click.command()
@click.argument("path", type=click.Path(), default=os.getcwd())
def sync(path: str) -> None:
    """Synchronize component references

    Synchronizes all component and dependency references (.component files) in the current program or component.

    Note that this will remove all invalid component references.

    Arguments:
    
        PATH: Path to the MXOS project [default: CWD]

    Example:

        $ mxos sync
    """
    click.echo("Synchronizing all .component files to revision of it's componet.")
    root_path = pathlib.Path(path)
    sync_project(root_path)
    libs = get_known_libs(root_path)
    _print_dependency_table(libs, root_path)

def _print_dependency_table(libs: List, root: pathlib.Path) -> None:
    table = Table(title="Components List", box = box.ROUNDED, style='blue')

    table.add_column("Library", style="cyan")
    table.add_column("URL", style="magenta")
    table.add_column("Path", style="green")
    table.add_column("Commit", style="blue")

    for lib in libs:
        table.add_row(
            lib.reference_file.stem,
            lib.get_git_reference().repo_url,
            str(lib.source_code_path.relative_to(str(root))).replace('\\', '/'),
            git_utils.get_default_branch(git_utils.get_repo(lib.source_code_path))
            if not lib.get_git_reference().ref
            else lib.get_git_reference().ref[:6],
        )

    console = Console()
    console.print(table, justify="left")