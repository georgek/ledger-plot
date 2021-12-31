# Ledger Plot

A plotting tool for ledger.

## Installation

Install with pipx.

## Usage

Pipe the output of a ledger report into it, e.g.:

```sh
ledger reg -f accounts.ledger ^Assets ^Liabilities | ledger-plot
```

The `event_file` option can be used to mark significant events on the plot. This file is
a YAML file with the following structure:

```yaml
--- # Events
- date: 2011-12-11
  type: house
  text: My House

- date: 2011-12-11
  type: job
  text: My new job
```

Type can be one of "job", "house" or "misc", which are colour coded, or anything else. I
use it to show important changes like new jobs, accommodation, and significant world
events.
