import os
import re

# We will scan all .lean files in verification/antigravit2/src/
src_dir = r"c:\Users\badbu\Documents\4.0\wt-TKT-2026-07-13-lean-f1\verification\antigravit2\src"

decl_regex = re.compile(r'^(\s*)(def|lemma|theorem|structure|instance|abbrev|class)\s+([^\s:]+)', re.MULTILINE)

def has_valid_tag(docstring):
    # Search for [A], [A-], [B], [C], [D], [E] anywhere in the docstring
    return bool(re.search(r'\[(A|A\-|B|C|D|E)\]', docstring))

for root, _, files in os.walk(src_dir):
    for f in files:
        if not f.endswith('.lean'): continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # We need to find all declarations
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            match = re.match(r'^(\s*)(def|lemma|theorem|structure|instance|abbrev|class)\s+([^\s:{(]+)', lines[i])
            if match:
                indent = match.group(1)
                decl_type = match.group(2)
                
                # Check if previous lines contain a docstring
                # Go backwards to find the start of the docstring if it exists
                doc_start = -1
                doc_end = i - 1
                has_doc = False
                if doc_end >= 0 and lines[doc_end].strip() == '-/' or lines[doc_end].strip().endswith('-/'):
                    # It has a docstring closing. Find the opening.
                    has_doc = True
                    for j in range(doc_end, -1, -1):
                        if '/--' in lines[j] or '/*-' in lines[j] or '/-' in lines[j]:
                            doc_start = j
                            break
                
                if has_doc and doc_start != -1:
                    docstring = '\n'.join(lines[doc_start:doc_end+1])
                    if not has_valid_tag(docstring):
                        # Replace [DEFINITIONAL] with [D] or [A] depending on type
                        if '[DEFINITIONAL]' in lines[doc_start]:
                            if decl_type in ['theorem', 'lemma']:
                                lines[doc_start] = lines[doc_start].replace('[DEFINITIONAL]', '[A]')
                            else:
                                lines[doc_start] = lines[doc_start].replace('[DEFINITIONAL]', '[D]')
                        elif '[HEURISTIC]' in lines[doc_start]:
                            if decl_type in ['theorem', 'lemma']:
                                lines[doc_start] = lines[doc_start].replace('[HEURISTIC]', '[A]')
                            else:
                                lines[doc_start] = lines[doc_start].replace('[HEURISTIC]', '[D]')
                        else:
                            # Add tag right after /-- or /-
                            tag = '[A]' if decl_type in ['theorem', 'lemma'] else '[D]'
                            lines[doc_start] = lines[doc_start].replace('/--', f'/-- {tag}', 1)
                            if '/--' not in lines[doc_start]:
                                lines[doc_start] = lines[doc_start].replace('/-', f'/- {tag}', 1)
                else:
                    # No docstring, insert one
                    tag = '[A] Machine-verified theorem.' if decl_type in ['theorem', 'lemma'] else '[D] Structural.'
                    lines.insert(i, f"{indent}/-- {tag} -/")
                    i += 1 # shift because we inserted a line
                    
            new_lines.append(lines[i])
            i += 1
            
        with open(path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_lines))
