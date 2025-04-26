import logging
import re
from pathlib import Path


def process_markdown_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = break_lines_titles(content)
    content = convert_github_admonitions_to_pandoc_divs(content)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def break_lines_titles(content):
    """
    Quebra linhas longas em títulos para evitar quebras de página indesejadas.

    Args:
        content: Uma string contendo o texto Markdown.

    Returns:
        Uma string com as linhas longas quebradas.
    """
    lines = content.splitlines()
    output_lines = []
    for line in lines:
        if line.startswith("#") or line.startswith("##") or line.startswith("###"):
            # Adiciona uma quebra de linha após o título
            output_lines.append('\n' + line + "\n")
        else:
            output_lines.append(line)
    return "\n".join(output_lines)

def convert_github_admonitions_to_pandoc_divs(markdown_text):
    """
    Converte admonitions no estilo GitHub (> [!NOTE]) para
    Divs Cercados do Pandoc (::: {.alert .alert-type}).

    Args:
        markdown_text: Uma string contendo o texto Markdown.

    Returns:
        Uma string com os admonitions convertidos.
    """
    lines = markdown_text.splitlines()
    output_lines = []
    in_admonition = False
    admonition_type = ""
    admonition_content = []
    title = ""

    # Regex para encontrar a linha inicial de um admonition
    # Captura o TIPO (NOTE, WARNING, etc.)
    start_pattern = re.compile(r"^\s*>\s*\[!(\w+)\](\+|-)?\s*(?:\*\*([^\n]*)\*\*)?.*$")


    # Regex para encontrar linhas de continuação do blockquote
    continuation_pattern = re.compile(r"^\s*>\s?(.*)$") # Captura o conteúdo após '> ' ou '>'


    def _start_admonition(start_match):
        nonlocal in_admonition, admonition_type, admonition_content, title
        logging.debug(f"Admonition found: {start_match.group(1)}")
        in_admonition = True
        admonition_type = start_match.group(1).lower()
        title = start_match.group(3) or admonition_type.capitalize()
        admonition_content = [] # Limpa o conteúdo anterior

    def _finish_admonition():
        nonlocal in_admonition, admonition_type, admonition_content, title
        # A linha atual NÃO começa com '>', então o admonition terminou
        # 1. Formatar e adicionar o admonition concluído à saída
        output_lines.append(f"::: {{.callout .callout-{admonition_type}}}")
        #addciona o titulo se houver
        output_lines.append(f"**{title}**\n")
        output_lines.extend(admonition_content)
        output_lines.append(":::")
        # 2. Resetar o estado
        in_admonition = False
        admonition_type = ""
        admonition_content = []

    for line in lines:
        start_match = start_pattern.match(line)
        if not in_admonition:
            # Não estávamos em um admonition, verificar se a linha atual inicia um
            if start_match:
                _start_admonition(start_match)
            else:
                output_lines.append(line)
        else:
            continuation_match = continuation_pattern.match(line)
            if continuation_match:
                content_line = continuation_match.group(1)
                admonition_content.append(content_line)
            else:
                _finish_admonition()
                # 3. IMPORTANTE: Processar a linha atual (que não era continuação)
                start_match_new = start_pattern.match(line)
                if start_match_new:
                    _start_admonition(start_match_new)
                else:
                     # Se não inicia novo admonition, adiciona a linha atual à saída
                    output_lines.append(line)

    # Caso o arquivo termine enquanto ainda estávamos em um admonition
    if in_admonition:
        _finish_admonition()

    return "\n".join(output_lines)



