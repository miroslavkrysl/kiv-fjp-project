import click


@click.command()
@click.option('--from', 'from_who', prompt='Your name', default="no one", help='Who is saying hello world.')
def hello(from_who):
    """Simple program that prints Hello world!"""
    print(f"Hello world! from {from_who}.")


if __name__ == '__main__':
    hello()
