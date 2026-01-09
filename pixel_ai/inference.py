import os
from llama_cpp import Llama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text
from rich.theme import Theme
from .config import MODEL_PATH, MAX_TOKENS, TEMPERATURE

# Custom Theme: Orange accent (#C15F3C), Warm off-white (#faf9f5), Charcoal (#2b2b2b)
CUSTOM_THEME = Theme({
    "accent": "#C15F3C",          # Orange
    "text": "#faf9f5",            # Warm off-white
    "ui": "#2b2b2b",              # Charcoal
    "markdown.h1": "bold #C15F3C",
    "markdown.h2": "bold #C15F3C",
    "markdown.h3": "bold #C15F3C",
    "markdown.paragraph": "#faf9f5",
})

console = Console(theme=CUSTOM_THEME)

def run_llm():
    if not os.path.exists(MODEL_PATH):
        console.print(Panel(
            f"[bold red]Error:[/bold red] Model not found at [accent]{MODEL_PATH}[/accent].\n"
            "Please run [bold cyan]pixel-ai install[/bold cyan] first.",
            title="System Error",
            border_style="red"
        ))
        return

    with console.status("[bold accent]Initializing Pixel-AI engine...", spinner="dots"):
        model = Llama(model_path=MODEL_PATH, verbose=False)
    
    console.clear()
    console.print(Panel(
        Markdown("# 🧠 Pixel-AI: Emotion Mirror\n*Professional Grade AI Interface*"),
        subtitle="Type 'exit' to quit",
        border_style="accent",
        title_align="left",
        subtitle_align="left"
    ))

    try:
        while True:
            # Styled User Input - Left aligned
            prompt = Prompt.ask("\n[bold accent]You[/bold accent]")
            
            if prompt.lower() in ["exit", "quit", "bye"]:
                console.print("[bold accent]Exiting Pixel-AI. Have a great day![/bold accent]")
                break

            # Thinking state
            with console.status("[italic accent]Pixel is thinking...", spinner="bouncingBall"):
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
                title="[bold accent]Pixel-AI[/bold accent]",
                border_style="accent",
                padding=(1, 2),
                title_align="left"
            )

            with Live(panel, console=console, refresh_per_second=20) as live:
                for chunk in stream:
                    text = chunk['choices'][0]['text']
                    response_text += text
                    # Update the panel content with markdown
                    panel.renderable = Markdown(response_text, justify="left")
                    live.refresh()
            
    except KeyboardInterrupt:
        console.print("\n[bold accent]Interrupted. Exiting...[/bold accent]")
