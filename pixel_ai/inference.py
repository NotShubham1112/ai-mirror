import os
from llama_cpp import Llama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text
from .config import MODEL_PATH, MAX_TOKENS, TEMPERATURE

console = Console()

def run_llm():
    if not os.path.exists(MODEL_PATH):
        console.print(Panel(
            f"[bold red]Error:[/bold red] Model not found at [yellow]{MODEL_PATH}[/yellow].\n"
            "Please run [bold cyan]pixel-ai install[/bold cyan] first.",
            title="System Error",
            border_style="red"
        ))
        return

    with console.status("[bold green]Initializing Pixel-AI engine...", spinner="dots"):
        model = Llama(model_path=MODEL_PATH, verbose=False)
    
    console.clear()
    console.print(Panel(
        Markdown("# 🧠 Pixel-AI: Emotion Mirror\n*Production-grade offline LLM interface*"),
        subtitle="Type 'exit' to quit",
        border_style="blue"
    ))

    try:
        while True:
            # Styled User Input
            prompt = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if prompt.lower() in ["exit", "quit", "bye"]:
                console.print("[bold yellow]Exiting Pixel-AI. Have a great day![/bold yellow]")
                break

            # Thinking state
            with console.status("[italic blue]Pixel is thinking...", spinner="bouncingBall"):
                stream = model(
                    prompt, 
                    max_tokens=MAX_TOKENS, 
                    temperature=TEMPERATURE,
                    stop=["<|im_end|>", "You:", "Pixel-AI:"],
                    stream=True
                )

            # Real-time Typing Effect with Rich Live
            response_text = ""
            panel = Panel(
                Markdown(""),
                title="[bold blue]Pixel-AI[/bold blue]",
                border_style="bright_blue",
                padding=(1, 2)
            )

            with Live(panel, console=console, refresh_per_second=20) as live:
                for chunk in stream:
                    text = chunk['choices'][0]['text']
                    response_text += text
                    # Update the panel content
                    panel.renderable = Markdown(response_text)
                    live.refresh()
            
    except KeyboardInterrupt:
        console.print("\n[bold yellow]KeyboardInterrupt detected. Exiting...[/bold yellow]")
