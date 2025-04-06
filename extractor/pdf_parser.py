import pdfplumber
import os
import csv

def clean_table(table):
    """Clean the table by removing empty rows and columns."""
    return [row for row in table if any(cell and cell.strip() for cell in row)]

def extract_table_from_pdf(file_path: str, output_path: str, start_page=None, end_page=None, separate_files=False, add_table_titles=False):
    if not os.path.exists(file_path):
        print("❌ File not found")
        return

    if start_page and end_page and start_page > end_page:
        print("❌ Invalid page range: start_page cannot be greater than end_page.")
        return

    all_tables = []

    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
        s = start_page - 1 if start_page else 0
        e = end_page if end_page else total_pages

        print(f"📄 Extracting tables from pages {s+1} to {e}")

        for i in range(s, e):
            page = pdf.pages[i]
            tables_on_page = page.extract_tables()
            if tables_on_page:
                all_tables.extend(tables_on_page)

    if not all_tables:
        print("No tables founf")
        return

    # Clean tables
    clean_tables = [clean_table(table) for table in all_tables if clean_table(table)]

    if separate_files:
        base, ext = os.path.splitext(output_path)
        for idx, table in enumerate(clean_tables, start=1):
            table_file = f"{base}_{idx}{ext}"
            with open(table_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(table)
            print(f"✅ Table {idx} saved to {table_file}")
    else:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for idx, table in enumerate(clean_tables, start=1):
                if add_table_titles:
                    writer.writerow([f"Table {idx}"])
                writer.writerows(table)
                writer.writerow([])  # Space between tables
        print(f"✅ All tables saved to {output_path}")
