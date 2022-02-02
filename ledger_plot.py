from bisect import bisect_left
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from itertools import groupby
from typing import List

import click
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker
from yaml import safe_load as load_yaml


@dataclass
class Event:
    date: date
    type: str
    text: str


def parse_events(event_file):
    data = load_yaml(event_file)
    return [Event(**item) for item in data]


def date_to_value(dates: List[date], values: List[float], date: date) -> float:
    position = bisect_left(dates, date)
    return values[position]


def add_event_grid(ax, dates: List[date], values: List[float], events: List[Event]):
    sorted_events = list(sorted(events, key=lambda e: e.date))
    event_groups = groupby(sorted_events, key=lambda e: e.date.replace(day=1))

    shade = False
    for start, end in zip(sorted_events, sorted_events[1:]):
        if shade:
            ax.fill_betweenx(values, start.date, end.date, color="grey", alpha=0.1)
        shade = not shade
    # do last bit of shade
    if shade:
        ax.fill_betweenx(
            values, sorted_events[-1].date, max(dates), color="grey", alpha=0.1
        )

    min_value = min(values)
    max_value = max(values)
    middle_value = (min_value + max_value) / 2

    for group_date, events in event_groups:
        value_at_date = date_to_value(dates, values, group_date)
        if value_at_date < middle_value:
            offset_amount = (max_value - min_value) * 0.15
            mid = (value_at_date + max_value) / 2
        else:
            offset_amount = -(max_value - min_value) * 0.15
            mid = (min_value + value_at_date) / 2

        offset = -offset_amount

        colours = {"job": "blue", "house": "green", "misc": "red"}

        for event in events:
            y = mid + offset
            colour = colours.get(event.type, "black")
            ax.text(
                event.date,
                y,
                event.text,
                color=colour,
                alpha=0.6,
                rotation="vertical",
                horizontalalignment="center",
                verticalalignment="center",
            )
            offset += offset_amount


@click.command(help="Plot ledger data")
@click.version_option()
@click.option("-t", "--title")
@click.option("--xmin", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--xmax", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--ymin", type=float)
@click.option("--ymax", type=float)
@click.option("-e", "--event_file", type=click.File(mode="r"))
@click.option(
    "--plot-type", type=click.Choice(["line", "bar", "scatter"]), default="line"
)
@click.argument("input_file", type=click.File(mode="r"), default="-")
def main(
    input_file,
    plot_type,
    title=None,
    xmin=None,
    xmax=None,
    ymin=None,
    ymax=None,
    event_file=None,
):
    data = sorted((line.split() for line in input_file), key=lambda t: t[0])
    dates = [datetime.strptime(d[0], "%Y-%m-%d").date() for d in data]
    values = [float(d[1]) for d in data]

    plt.style.use("bmh")

    fig, ax = plt.subplots()

    if plot_type == "line":
        ax.step(dates, values, where="post")
    elif plot_type == "bar":
        ax.bar(x=dates, height=values, width=timedelta(days=7))
    elif plot_type == "scatter":
        ax.scatter(dates, values)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    years = mdates.YearLocator()
    months = mdates.MonthLocator()

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(months)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(20000))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(2000))

    ax.grid(which="major", alpha=0.8)
    ax.grid(which="minor", alpha=0.3)

    events = parse_events(event_file) if event_file else []
    add_event_grid(ax, dates, values, events)

    plt.title(title)

    plt.show()
