#
# Copyright (c) 2020-2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Main cli entry point."""

from pkg_resources import get_distribution
from typing import Union, Any

import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

def print_version(context: click.Context, param: Union[click.Option, click.Parameter], value: bool) -> Any:
    """Print the version of mbed-tools."""
    if not value or context.resilient_parsing:
        return

    version_string = get_distribution("mbed-tools").version
    click.echo(version_string)
    context.exit()

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Display versions of all Mbed Tools packages.",
)
@click.option(
    "-v",
    "--verbose",
    default=0,
    count=True,
    help="Set the verbosity level, enter multiple times to increase verbosity.",
)
@click.option("-t", "--traceback", is_flag=True, show_default=True, help="Show a traceback when an error is raised.")
def cli(verbose: int, traceback: bool) -> None:
    """Command line tool for interacting with Mbed OS."""
    print(f'verbose = {verbose}')

@click.command()
@click.argument("url")
@click.argument("path", type=click.Path(), default="")
@click.option(
    "--skip-resolve-libs",
    "-s",
    is_flag=True,
    show_default=True,
    help="Skip resolving program library dependencies after cloning.",
)
def import_(url: str, path: Any, skip_resolve_libs: bool) -> None:
    print(url, path, skip_resolve_libs)

cli.add_command(import_, "import")
cli()