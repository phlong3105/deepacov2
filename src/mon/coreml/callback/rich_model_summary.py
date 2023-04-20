#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements rich model summary callback."""

from __future__ import annotations

__all__ = [
    "RichModelSummary",
]

from lightning.pytorch import callbacks
from lightning.pytorch.utilities import model_summary

from mon.foundation import console, rich
from mon.globals import CALLBACKS


# region Rich Model Summary

@CALLBACKS.register(name="rich_model_summary")
class RichModelSummary(callbacks.RichModelSummary):
    """Generates a summary of all layers in a
    :class:`~lightning.pytorch.core.module.LightningModule` with `rich text
    formatting <https://github.com/Textualize/rich>`_.
    
    See Also:
    :class:`lightning.pytorch.callbacks.rich_model_summary.RichModelSummary`.
    """
    
    @staticmethod
    def summarize(
        summary_data        : list[tuple[str, list[str]]],
        total_parameters    : int,
        trainable_parameters: int,
        model_size          : float,
    ):
        table = rich.table.Table(header_style="bold magenta")
        table.add_column(" ", style="dim")
        table.add_column("Name", justify="left", no_wrap=True)
        table.add_column("Type")
        table.add_column("Params", justify="right")
        
        column_names = list(zip(*summary_data))[0]
        
        for column_name in ["In sizes", "Out sizes"]:
            if column_name in column_names:
                table.add_column(column_name, justify="right", style="white")
        
        rows = list(zip(*(arr[1] for arr in summary_data)))
        for row in rows:
            table.add_row(*row)
        
        console.log(table)
        
        parameters = []
        for param in [
            trainable_parameters,
            total_parameters - trainable_parameters,
            total_parameters, model_size
        ]:
            parameters.append("{:<{}}".format(model_summary.get_human_readable_count(int(param)), 10))
        
        grid = rich.table.Table.grid(expand=True)
        grid.add_column()
        grid.add_column()
        
        grid.add_row(f"[bold]Trainable params[/]: {parameters[0]}")
        grid.add_row(f"[bold]Non-trainable params[/]: {parameters[1]}")
        grid.add_row(f"[bold]Total params[/]: {parameters[2]}")
        grid.add_row(f"[bold]Total estimated model params size (MB)[/]: {parameters[3]}")
        
        console.log(grid)

# endregion
