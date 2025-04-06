import typer
from extractor.pdf_parser import extract_table_from_pdf

app = typer.Typer()

@app.command()
def main(
    file: str = typer.Option(..., help="Path to the PDF file"),
    output: str = typer.Option(..., help="Path to output CSV"),
    start_page: int = typer.Option(None, help="Start page"),
    end_page: int = typer.Option(None, help="End page"),
    titles: bool = typer.Option(False, help="Add table titles"),
    separate_files: bool = typer.Option(False, help="Save each table to separate file"),
):
    """Extract table from PDF and save to CSV."""
    extract_table_from_pdf(file, output, start_page, end_page,separate_files,titles)

if __name__ == "__main__":
    app()
