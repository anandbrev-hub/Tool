#!/usr/bin/env python
import sys
import argparse
from PyPDF2 import PdfMerger
from tkinter import Tk, filedialog, messagebox

def merge_pdfs(input_files, output_path):
    """Core PDF merging functionality"""
    merger = PdfMerger()
    try:
        for pdf in input_files:
            merger.append(pdf)
        with open(output_path, "wb") as f:
            merger.write(f)
        return True, "PDFs merged successfully!"
    except Exception as e:
        return False, str(e)
    finally:
        merger.close()

def gui_mode():
    """Graphical user interface mode"""
    root = Tk()
    root.withdraw()

    # File selection
    input_files = filedialog.askopenfilename(
        title="Select PDF Files to Merge",
        filetypes=[("PDF Files", "*.pdf")],
        multiple=True
    )
    if not input_files:
        messagebox.showinfo("Info", "No files selected!")
        return

    # Output selection
    output_path = filedialog.asksaveasfilename(
        title="Save Merged PDF As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not output_path:
        messagebox.showinfo("Info", "No output file specified!")
        return

    # Merge and show result
    success, msg = merge_pdfs(input_files, output_path)
    if success:
        messagebox.showinfo("Success", f"{msg}\nSaved at: {output_path}")
    else:
        messagebox.showerror("Error", f"Merge failed:\n{msg}")

def cli_mode(args):
    """Command-line interface mode"""
    success, msg = merge_pdfs(args.inputs, args.output)
    if success:
        print(f"Success: {msg}")
        print(f"Output file: {args.output}")
    else:
        sys.stderr.write(f"Error: {msg}\n")
        sys.exit(1)

if __name__ == "__main__":
    # CLI argument parsing
    parser = argparse.ArgumentParser(description='PDF Merger Tool')
    parser.add_argument('-o', '--output', help='Output PDF file')
    parser.add_argument('inputs', nargs='*', help='Input PDF files')
    
    # Check if CLI mode should be used
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if not args.output or len(args.inputs) < 1:
            parser.print_help()
            sys.exit(1)
        cli_mode(args)
    else:
        gui_mode()
