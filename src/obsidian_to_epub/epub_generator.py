import subprocess
from pathlib import Path
import logging

def generate_epub(input_dir, output_file, css_file):
    """
    Converts processed Markdown files in the input directory to a single ePub file.

    Args:
        input_dir (str): The directory containing processed Markdown files.
        output_file (str): The path where the generated ePub file will be saved.
        css_file (str): The path to the CSS file to be linked in the ePub.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Convert string paths to Path objects
    input_path = Path(input_dir)
    output_path = Path(output_file)
    css_path = Path(css_file)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get markdown files and sort them
    markdown_files = sorted(str(f) for f in input_path.glob('**/*.md'))
    logging.info(f"Markdown files found: {markdown_files}")
    if not markdown_files:
        logging.warning(f"No markdown files found in {input_path}")
        return False
    
    # Construct the Pandoc command
    command = [
        'pandoc',
        *markdown_files,  # Expand list as separate arguments
        '-o', str(output_path),
        '--css', str(css_path)
    ]

    # Execute the command
    try:
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True
        )
        logging.info(f"ePub generated successfully: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating ePub: {e}")
        logging.error(f"Stderr: {e.stderr}")
        return False