import typer
from pathlib import Path
from rich.console import Console
from ragchat.loader import DocumentLoader
from ragchat.search import BM25Search
from ragchat.web import scrape_url
from ragchat.chat import chat_loop

app = typer.Typer(help="RAG Chatbot CLI")
console = Console()

@app.command()
def load(path_or_url: str):
    """
    Load content from a file, directory, or URL and index it.
    """
    loader = DocumentLoader()
    search_engine = BM25Search()
    
    # Try to load existing data first to append if necessary
    # For now, let's keep it simple: new load creates a new index.
    # But search_engine.load() is there if we want persistence.
    
    all_chunks = []
    
    if path_or_url.startswith(("http://", "https://")):
        console.print(f"[blue]Scraping URL: {path_or_url}...[/blue]")
        try:
            text = scrape_url(path_or_url)
            chunks = loader.split_text(text, metadata={"source": path_or_url})
            all_chunks.extend([c.text for c in chunks])
        except Exception as e:
            console.print(f"[red]Error scraping URL: {e}[/red]")
            raise typer.Exit(code=1)
    else:
        path = Path(path_or_url)
        if not path.exists():
            console.print(f"[red]Path does not exist: {path_or_url}[/red]")
            raise typer.Exit(code=1)
            
        if path.is_file():
            console.print(f"[blue]Loading file: {path}...[/blue]")
            try:
                chunks = loader.load_file(path)
                all_chunks.extend([c.text for c in chunks])
            except Exception as e:
                console.print(f"[red]Error loading file: {e}[/red]")
                raise typer.Exit(code=1)
        elif path.is_dir():
            console.print(f"[blue]Loading directory: {path}...[/blue]")
            # Support .txt, .md, .pdf
            for ext in [".txt", ".md", ".pdf"]:
                for file_path in path.glob(f"**/*{ext}"):
                    try:
                        chunks = loader.load_file(file_path)
                        all_chunks.extend([c.text for c in chunks])
                    except Exception as e:
                        console.print(f"[yellow]Skipping {file_path}: {e}[/yellow]")
        else:
            console.print(f"[red]Unknown path type: {path_or_url}[/red]")
            raise typer.Exit(code=1)

    if not all_chunks:
        console.print("[yellow]No content found to index.[/yellow]")
        return

    console.print(f"[green]Indexing {len(all_chunks)} chunks...[/green]")
    search_engine.fit(all_chunks)
    search_engine.save()
    console.print("[bold green]Success![/bold green] Content indexed and saved.")

@app.command()
def chat():
    """
    Start the interactive chat loop.
    """
    chat_loop()

if __name__ == "__main__":
    app()
