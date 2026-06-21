#!/usr/bin/env python3
"""
Converts the UIDT_Ontology LaTeX manuscript into a machine-readable JSON format,
preserving all content strictly without changes.
"""
import json
import re
import sys
from pathlib import Path

def parse_tex_to_json(tex_path: Path, json_path: Path):
    text = tex_path.read_text(encoding="utf-8")
    
    # We will build a structured representation.
    # To keep it "strictly without changes", we simply chunk the document by structural commands,
    # preserving all raw text.
    
    blocks = []
    
    # Split by lines to process sequentially
    lines = text.splitlines(keepends=True)
    
    current_block = {"type": "preamble", "content": ""}
    
    section_pattern = re.compile(r'\\(part|section|subsection|subsubsection)\*?\{([^}]+)\}')
    env_begin = re.compile(r'\\begin\{([^}]+)\}')
    env_end = re.compile(r'\\end\{([^}]+)\}')
    
    env_stack = []
    
    for line in lines:
        # Check if document starts
        if '\\begin{document}' in line:
            if current_block["content"]:
                blocks.append(current_block)
            current_block = {"type": "document_start", "content": line}
            blocks.append(current_block)
            current_block = {"type": "text", "content": ""}
            continue
            
        # Match sections if we are not deep in an environment that shouldn't be split (like verbatim, but we just split anyway to keep it simple, actually let's just split sections if env_stack is empty)
        sec_match = section_pattern.search(line)
        if sec_match and not env_stack:
            if current_block["content"].strip():
                blocks.append(current_block)
            current_block = {
                "type": sec_match.group(1),
                "title": sec_match.group(2),
                "content": line
            }
            continue
            
        b_match = env_begin.search(line)
        if b_match:
            env_stack.append(b_match.group(1))
            if len(env_stack) == 1: # Outermost environment
                if current_block["content"].strip():
                    blocks.append(current_block)
                current_block = {"type": f"env_{b_match.group(1)}", "content": line}
                continue
                
        e_match = env_end.search(line)
        if e_match and env_stack:
            if e_match.group(1) == env_stack[-1]:
                env_stack.pop()
                if len(env_stack) == 0:
                    current_block["content"] += line
                    blocks.append(current_block)
                    current_block = {"type": "text", "content": ""}
                    continue
        
        # Accumulate
        current_block["content"] += line

    # Append last block
    if current_block["content"].strip():
        blocks.append(current_block)
        
    # Post-process: clean up empty text blocks and assemble the final dictionary
    output = {
        "source_file": tex_path.name,
        "document_structure": []
    }
    
    for b in blocks:
        # Strip trailing newlines from content to make it slightly cleaner, but preserve internal ones.
        if b["content"].strip():
            output["document_structure"].append(b)

    # Write out as highly formatted JSON
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully wrote JSON to {json_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    tex_file = base_dir / "manuscript" / "UIDT_Ontology_v3_9_9.tex"
    json_file = base_dir / "manuscript" / "UIDT_Ontology_v3_9_9.json"
    
    if not tex_file.exists():
        print(f"Error: {tex_file} not found.")
        sys.exit(1)
        
    parse_tex_to_json(tex_file, json_file)
