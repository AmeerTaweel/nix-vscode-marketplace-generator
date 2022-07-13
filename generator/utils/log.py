from rich.console import Console

console = Console()

def success(msg):
    console.log(f"[bold green]SUCCESS:[/bold green] {msg}.")

def error(msg):
    console.log(f"[bold red]ERROR  :[/bold red] {msg}.")

def info(msg):
    console.log(f"[bold blue]INFO   :[/bold blue] {msg}.")
