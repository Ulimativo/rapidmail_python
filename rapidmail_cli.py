########################################
# Python Module for the RapidMail API. #
# CLI Version                          #
# v. 0.2 - Alpha                       #
########################################

# IMPORTS
import click
import rapidmail as rm


@click.group()
def cli():
    pass


@click.command()
@click.argument('list_id')
def savesubs(list_id):
    """ 
    Save Subscribers from List to csv file. 
    """
    click.echo(f"List ID is : {list_id}")
    filename = click.prompt("Please enter filename to store data", type=str)
    click.echo(rm.save_recipients_stats(filename, list_id))


@click.command()
def main():
    """
    The CLI Version of the RapidMail API Python Module.
    Functionality to be added here.
    """
    click.echo("")
    click.echo("-------------------------------------------")
    click.secho("# Welcome to the Rapidmail API Python CLI #", fg="cyan")
    click.echo("-------------------------------------------")
    filename = click.prompt("Please enter filename to store data", type=str)
    click.secho(f"File to store data: {filename}", fg="blue")
    click.echo("Starting data retrieval...")
    click.confirm('Do you want to continue?', abort=True)
    #click.secho("OK. Exiting now.", fg="green")
    """
    filename = input("What filename do you want to save the data to? ")
    list_id = input("Which List ID to pull data from? ")
    # list_id=5677
    print(f"Data from {list_id} will be saved to {filename}.csv)")
    print(save_recipients_stats(filename, list_id))
    """


cli.add_command(main)
cli.add_command(savesubs)

if __name__ == "__main__":
    cli()
