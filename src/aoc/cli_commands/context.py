import click

from aoc import _utils


@click.group(name="context")
def context_group():
	"""Manages the persistent puzzle context (year and day)."""
	pass


@context_group.command(name="set")
@click.option("-y", "--year", type=int, required=True, help="The puzzle year to set.")
@click.option("-d", "--day", type=int, required=True, help="The puzzle day to set.")
def context_set(year, day):
	"""Sets and saves the puzzle context with validation."""
	latest_year, latest_day = _utils.get_latest_puzzle_date()

	# Validate the requested date
	if not 2015 <= year <= latest_year:
		click.secho(
			f"Error: Year must be between 2015 and {latest_year}.",
			fg="red",
		)
		raise click.Abort()

	if not 1 <= day <= 25:
		click.secho("Error: Day must be between 1 and 25.", fg="red")
		raise click.Abort()

	if year == latest_year and day > latest_day:
		click.secho(
			f"Error: Puzzle for {year}-{day:02d} is not yet available.",
			fg="red",
		)
		click.secho(f"The latest available puzzle is {latest_year}-{latest_day:02d}.")
		raise click.Abort()

	_utils.write_context(year, day)
	click.secho(f"✅ Context set to Year {year}, Day {day}.", fg="green")


@context_group.command(name="show")
def context_show():
	"""Displays the current puzzle context."""
	context = _utils.read_context()
	if context:
		year, day = context
		click.echo(f"The current context is set to: Year {year}, Day {day}")
	else:
		click.echo("No context is currently set.")
		click.echo("The tool will default to the latest available puzzle.")


@context_group.command(name="clear")
def context_clear():
	"""Clears the saved puzzle context."""
	_utils.clear_context()
	click.secho("✅ Context cleared.", fg="green")
	click.echo("The tool will now default to the latest available puzzle.")
