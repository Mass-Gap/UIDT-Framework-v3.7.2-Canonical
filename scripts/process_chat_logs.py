#!/usr/bin/env python3
"""
UIDT Framework v4.0 - AI Knowledge Base Processor
-------------------------------------------------
Parst rohe Chat-Logs (JSON/Markdown) und zerlegt sie in semantische Chunks.
Zwingende Sicherheitsvorgabe: Output MUSS in .uidt-local/ landen (.gitignore).
"""

import os
import json
import re

# Hardcoded lokale Pfade (Anti-Leakage)
INPUT_DIR = "raw_chat_logs"
OUTPUT_DIR = ".uidt-local/ai_knowledge_base"

def ensure_privacy_dir():
    """Garantiert, dass das Zielverzeichnis existiert und privat bleibt."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        # Zusätzliche Sicherheitsmaßnahme: Lokale .gitignore im Ordner
        with open(os.path.join(OUTPUT_DIR, ".gitignore"), "w") as f:
            f.write("*\n")
    print(f"[SEC-CHECK] Output-Verzeichnis {OUTPUT_DIR} gesichert.")

def chunk_text(text, max_words=300):
    """Einfacher semantischer Chunker (zerlegt an doppelten Zeilenumbrüchen)."""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        if len(current_chunk.split()) + len(p.split()) < max_words:
            current_chunk += p + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def process_logs():
    ensure_privacy_dir()
    
    # Beispiel-Struktur für die zu verarbeitenden Dateien
    files_to_process = [
        {"file": "DMT,-Hallucinations,-and-Scientific-Context_gemini-chat-full.json", "type": "json"},
        {"file": "Matrix-Thermodynamik_perpexit-chat-xport.md", "type": "md"}
    ]
    
    chunk_id = 0
    for file_info in files_to_process:
        filepath = os.path.join(INPUT_DIR, file_info["file"])
        if not os.path.exists(filepath):
            print(f"[WARNUNG] Datei nicht gefunden: {filepath}. Überspringe...")
            continue
            
        print(f"[PROCESS] Lese {filepath}...")
        
        # Rohtext extrahieren (stark vereinfacht für das Framework-Beispiel)
        with open(filepath, 'r', encoding='utf-8') as f:
            if file_info["type"] == "json":
                data = json.load(f)
                # Angenommen, der Text liegt in einer flachen Struktur
                raw_text = "\n\n".join([item.get("text", "") for item in data if "text" in item])
            else:
                raw_text = f.read()
                
        chunks = chunk_text(raw_text)
        
        # Chunks als JSONL abspeichern
        for chunk in chunks:
            chunk_data = {
                "id": f"uidt_chunk_{chunk_id:04d}",
                "source": file_info["file"],
                "content": chunk
            }
            out_file = os.path.join(OUTPUT_DIR, f"chunk_{chunk_id:04d}.json")
            with open(out_file, "w", encoding="utf-8") as out_f:
                json.dump(chunk_data, out_f, ensure_ascii=False, indent=2)
            chunk_id += 1

    print(f"[SUCCESS] {chunk_id} Chunks erfolgreich in {OUTPUT_DIR} isoliert.")

if __name__ == "__main__":
    process_logs()
