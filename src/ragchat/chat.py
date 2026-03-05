from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from ragchat.search import BM25Search
from ragchat.llm import LLMInterface

console = Console()

def chat_loop():
    search_engine = BM25Search()
    # Try to load existing index
    try:
        search_engine.load()
    except Exception:
        console.print("[yellow]No index found. Please load some content first using 'ragchat load'.[/yellow]")

    llm = LLMInterface()

    console.print(Panel.fit("Welcome to [bold blue]RAG Chat[/bold blue]! Type 'exit' or 'quit' to stop.", title="Chat"))

    while True:
        try:
            query = Prompt.ask("[bold green]You[/bold green]")
            if query.lower() in ["exit", "quit"]:
                break
            
            if not query.strip():
                continue

            with console.status("[bold blue]Searching and generating...[/bold blue]"):
                # 1. Search for context
                results = search_engine.search(query, n=5)
                context = "\n---\n".join(results)

                # 2. Generate response
                if not context:
                    response = llm.generate_response("No context found.", query)
                else:
                    response = llm.generate_response(context, query)

            console.print(Panel(Markdown(response), title="[bold blue]Assistant[/bold blue]", border_style="blue"))
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    chat_loop()
