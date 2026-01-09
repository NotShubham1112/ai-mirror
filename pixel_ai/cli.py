import click
import os
from rich.console import Console
from rich.panel import Panel
from .inference import run_llm
from .utils import download_model_if_needed

console = Console()

@click.group()
def cli():
    """🚀 Pixel-AI: Professional Emotion Mirror LLM for Raspberry Pi"""
    pass

@cli.command()
def run():
    """Run the AI companion in a beautiful terminal interface"""
    # download_model_if_needed() is now handled inside run_llm or here
    # To keep it clean, we'll call it here with a nice status
    with console.status("[bold blue]Checking model status...", spinner="bouncingBar"):
        download_model_if_needed()
    run_llm()

@cli.command()
def install():
    """Download local weights and set up the environment"""
    with console.status("[bold green]Downloading Pixel-AI model weights...", spinner="earth"):
        download_model_if_needed()
    console.print(Panel(
        "[bold green]Success![/bold green] Model installed and ready for local inference.",
        title="Installation Complete",
        border_style="green"
    ))

if __name__ == "__main__":
    cli()
