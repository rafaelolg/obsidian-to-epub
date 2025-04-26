import argparse
import logging
from pathlib import Path
from obsidian_to_epub.markdown_parser import process_markdown_file
from obsidian_to_epub.epub_generator import generate_epub
import tempfile

def main():
    parser = argparse.ArgumentParser(
        description="Convert Obsidian Markdown files into an EPUB."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Path to the directory containing Markdown files.",
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to the output EPUB file.",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_file = Path(args.output_file)

    if not input_dir.is_dir():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Temporary directory to store processed Markdown files
    temp_dir = Path(tempfile.mkdtemp())
    
    # Process all Markdown files in the input directory
    for file_path in input_dir.glob("*.md"):
        output_file_path = temp_dir / file_path.name
        print(f"Processing: {file_path}")
        process_markdown_file(file_path, output_file_path)

    # Generate the EPUB file
    print(f"Generating EPUB: {output_file} from {temp_dir}")
    css_path = Path(__file__).parent / "default.css"
    logging.info(f"Using CSS file: {css_path}")
    generate_epub(temp_dir, output_file, css_path)


    print("EPUB generation complete!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()
