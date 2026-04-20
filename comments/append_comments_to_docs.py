"""
Extracts unresolved Google Drive comments and appends them to the end of the Google Doc itself.
Takes a document ID as a command-line argument.
"""

import asyncio
import json
import os
import html
import re
import sys
import argparse

# Limit concurrency
semaphore = asyncio.Semaphore(5)

def normalize(text):
    if not text:
        return ""
    # Unescape HTML entities
    text = html.unescape(text)
    # Replace \u000b and other whitespace with standard space for matching
    text = re.sub(r'[\s\u000b]+', ' ', text).strip()
    return text

def get_context(full_text, quoted_text, lines_before=3, lines_after=3):
    normalized_full = normalize(full_text)
    normalized_quoted = normalize(quoted_text)
    
    if not normalized_quoted or len(normalized_quoted) < 4:
        return None

    if normalized_quoted not in normalized_full:
        return None

    lines = full_text.splitlines()
    normalized_lines = [normalize(line) for line in lines]
    
    for i, n_line in enumerate(normalized_lines):
        if normalized_quoted in n_line:
            start = max(0, i - lines_before)
            end = min(len(lines), i + lines_after + 1)
            return "\n".join(lines[start:end])
    
    first_part = normalized_quoted[:20]
    for i, n_line in enumerate(normalized_lines):
        if first_part in n_line:
            start = max(0, i - lines_before)
            end = min(len(lines), i + lines_after + 1)
            return "\n".join(lines[start:end])

    return None

async def process_doc(file_id):
    async with semaphore:
        # 0. Get document name
        name_cmd = ["gws", "drive", "files", "get", "--file-id", file_id, "--fields", "name"]
        name_proc = await asyncio.create_subprocess_exec(
            *name_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        name_stdout, _ = await name_proc.communicate()
        name = file_id
        if name_proc.returncode == 0:
            name_data = json.loads(name_stdout.decode())
            name = name_data.get("name", file_id)

        # 1. List comments
        params = {
            "fileId": file_id,
            "fields": "comments(content,author(displayName),resolved,quotedFileContent,replies(content,author(displayName)))"
        }
        cmd = ["gws", "drive", "comments", "list", "--params", json.dumps(params)]
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            print(f"Error listing comments for {name}: {stderr.decode()}")
            return

        try:
            data = json.loads(stdout.decode())
            comments = data.get("comments", [])
            unresolved = [c for c in comments if not c.get("resolved", False)]
            
            if not unresolved:
                print(f"No unresolved comments for {name}")
                return

            # 2. Export doc for context
            export_params = {
                "fileId": file_id,
                "mimeType": "text/plain"
            }
            tmp_filename = f"tmp_{file_id}.txt"
            export_cmd = ["gws", "drive", "files", "export", "--params", json.dumps(export_params), "-o", tmp_filename]
            
            export_proc = await asyncio.create_subprocess_exec(
                *export_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await export_proc.communicate()
            
            doc_text = ""
            if os.path.exists(tmp_filename):
                with open(tmp_filename, "r", encoding="utf-8", errors="ignore") as f:
                    doc_text = f.read()
                os.remove(tmp_filename)

            text_content = ["\n\n----------------------------------------------------------------\n",
                            "User Comments\n",
                            "----------------------------------------------------------------\n\n"]
            for c in unresolved:
                quoted_obj = c.get("quotedFileContent", {})
                quoted_value = quoted_obj.get("value", "")
                
                context = None
                if doc_text and quoted_value:
                    context = get_context(doc_text, quoted_value)
                
                unescaped_quote = html.unescape(quoted_value) if quoted_value else "[No selection]"
                text_content.append(f"Selection: \"{unescaped_quote}\"\n")
                
                if context:
                    text_content.append(f"Context:\n---\n{context}\n---\n")
                
                author = c.get("author", {}).get("displayName", "Unknown")
                content = c.get("content", "")
                text_content.append(f"Comment by {author}: {content}\n")
                
                for r in c.get("replies", []):
                    r_author = r.get("author", {}).get("displayName", "Unknown")
                    r_content = r.get("content", "")
                    text_content.append(f"  - Reply by {r_author}: {r_content}\n")
                
                text_content.append("\n---\n")

            if text_content:
                full_text_to_append = "".join(text_content)
                append_cmd = ["gws", "docs", "+write", "--document", file_id, "--text", full_text_to_append]
                
                append_proc = await asyncio.create_subprocess_exec(
                    *append_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await append_proc.communicate()
                
                if append_proc.returncode == 0:
                    print(f"Appended comments to: {name}")
                else:
                    error_msg = stderr.decode()
                    print(f"Failed to append to {name}")
                    if "insufficient authentication scopes" in error_msg.lower():
                        print("\nERROR: Insufficient authentication scopes to write to the document.")
                        print("FIX: Please re-authenticate gws with the required scopes by running:")
                        print("     gws auth login --services drive,docs")
                    else:
                        print(f"Error: {error_msg}")

        except Exception as e:
            print(f"Exception processing {name}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Extract unresolved Google Drive comments and append to the doc.")
    parser.add_argument("document_id", help="The Google Doc ID to process.")
    args = parser.parse_args()
    
    await process_doc(args.document_id)

if __name__ == "__main__":
    asyncio.run(main())
