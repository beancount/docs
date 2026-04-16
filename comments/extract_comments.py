"""
Extracts unresolved Google Drive comments and their surrounding document context into Markdown files.

Workflow:
1. Iterates through a list of document names and IDs (DOCS).
2. Processes documents concurrently using asyncio and a semaphore (limit 5).
3. For each document:
   a. Lists comments using 'gws drive comments list'.
   b. Filters for unresolved comments.
   c. Exports the document as 'text/plain' via 'gws drive files export' to a temporary file.
   d. Matches the comment's 'quotedFileContent' against the exported text.
      - Normalization: Unescapes HTML and collapses all whitespace (including \u000b) for robust matching.
      - Context: If a match is found (>3 chars), extracts 3 lines before and after.
   e. Formats the results as Markdown with code blocks for context and bulleted lists for replies.
   f. Saves to '[Document Name].md', sanitizing slashes in filenames and cleaning up temp files.
"""

import asyncio
import json
import subprocess
import os
import html
import re

# List of documents to process
DOCS = [
    ("Beancount - Trading with Beancount", "1WjARst_cSxNE-Lq6JnJ5CC41T3WndEsiMw4d46r2694"),
    ("Beancount - Tracking Medical Claims", "1NyATal9CRrBDsII6sLdwCNNv0qcJmcPxYpNrlnjCjp8"),
    ("Beancount - Language Syntax", "1wAMVrKIA2qtRGmoVDSUBJGmYZSygUaR0uOMW1GV3YE0"),
    ("Beancount - Contributions", "1Z37bQ45wDtjTPaMQ_x-f33p1trH9fNosEAUgbQXwp30"),
    ("Beancount - Precision & Tolerances", "1lgHxUUEY-UVEgoF6cupz2f_7v7vEF7fiJyiSlYYlhOo"),
    ("Beancount - Query Language", "1s0GOZMcrKKCLlP29MD7kHO4L88evrwWdIO0p4EwRBE0"),
    ("Beancount - How Inventories Work", "11a9bIoNuxpSOth3fmfuIFzlZtpTJbvw-bPaQCnezQJs"),
    ("Beancount - Tutorial & Example", "1G-gsmwK551lSyuHboVLW3xbLhh99JfoKIbNnZSJxteE"),
    ("Beancount - Comparison / Differences", "1dW2vIjaXVJAf9hr7GlZVe3fJOkM-MtlVjvCO1ZpNLmg"),
    ("Beancount - Price in Beancount", "1thYRAMell_QT1Da1F_laprSs6BlROZjyK_h3V8qHW9c"),
    ("Beancount - Importing External Data", "11EwQdujzEo2cxqaF5PgxCEZXWfKKQCYSMfdJowp_1S8"),
    ("Beancount - Getting Started", "1P5At-z1sP8rgwYLHso5sEy3u4rMnIUDDgob9Y_BYuWE"),
    ("Beancount - Running & Reports", "1e44jtLyVRl2H2Pj4K3WUc66otAlTOFOc90-tsrFEQdo"),
    ("Beancount - Install", "1FqyrTPwiHVLyncWTf3v5TcooCu9z5JRX8Nm41lVZi0U"),
    ("Beancount - The Double-Entry Counting Method", "100tGcA4blh6KSXPRGCZpUlyxaRUwFHEvnz_k9DyZFn4"),
    ("Beancount - Motivation", "1e4Vz3wZB_8-ZcAwIFde8X5CjzKshE4-OXtVVHm4RQ8s"),
    ("Beancount - C++ version: Install", "1WwZYqsp28Uuk5eFqHQ1u1zqdjghymy8S_Yo-OJENoa4"),
    ("Beangulp - Importing External Data", "1hBfsHZcoHgz5rvhCdP42g2FJ5ouycIMV4H1tfgXpwBU"),
    ("Beancount - Index", "1RaondTJCS_IUPBHFNdT8oqFKJjVJDsfsn6JEjBG04eA"),
    ("Beancount - Beangulp", "1O42HgYQBQEna6YpobTqszSgTGnbRX7RdjmzR2xumfjs"),
    ("Beancount - History and Credits", "17wTH7aKnN_7-6nCxsOad6zIQfHwQgJUdI02RjzQuNi8"),
    ("Beancount - Cookbook", "1Tss0IEzEyAPuKSGeNsfNgb0BfiW2ZHyP5nCFBW1uWlk"),
    ("Beancount - Symbology", "1_52VhapAuR-ej4yB8rFovA8MyMmF8IOcqO44apsdtKU"),
    ("Beancount - C++ version: Dependencies", "10R-msZljuqFY8nckUnR1jVxMX1ol7rJUCMZo7w7QUQs"),
    ("Beancount - Cookbook - How We Share Expenses", "1MjSpGoJVdgyg8rhKD9otSKo4iSD2VkSYELMWDBbsBiU"),
    ("Beancount - Cookbook - HealthCare Expenses", "16RKEl1NJ3qg8VU9vKRRvgIv3CyGs0_4ASS4lD5iBFTw"),
    ("Beancount - Vnext: Booking Rules Redesign", "1H0UDD1cKenraIMe40PbdMgnqJdeqI6yKv0og51mXk-0"),
    ("Beancount - C++ version: Changes from V2", "1Ia4zYmkB6I6IbWPRlcZYYuMS1ZI55T99dp9LiMJqXCE"),
    ("Beancount - Vnext: Goals & Design", "1qPdNXaz5zuDQ8M9uoZFyyFis7hA0G55BEfhWhrVBsfc"),
    ("Beancount - Rust version", "1M1GM4NvXWdSoIfUpexc5b3m72Up2-drqn3gP8TCCySk"),
    ("Beancount - Vnext: How to Use the API", "1hl7g_e2Bgb6mOEJ3nlleWUkmItJXjcXEUbNOM3tLiUk"),
    ("Beancount - For Cryptocurrencies", "1taN9lbcNDf8bKgDwprWOhuaOsOgALZzmsfvec-rdaSk"),
    ("Beancount - Calculating Portfolio Returns", "1nPsMIunLnDvdsg6TSsd0PZb7jngojNpFlqnaX36WRp8"),
    ("Beancount - Payee, Subaccount or Asset", "17_u_cYxeXVsCV4GmaubK_xsTQl_H9rP87E_vnZHKNb0"),
    ("Beancount - User Requests & Prioritization", "1uHonpRkbZ5wMCoZtzCBSBrl959Ciy4gq4aTB7A-m8Uk"),
    ("Beancount - Syntax Cheat Sheet", "1M4GwF6BkcXyVVvj4yXBJMX7YFXpxlxo95W6CpU3uWVc"),
    ("Johnny", "18AfWSRhQ1sWr0S4rd0GvQFy_7bXxCod-TC1qNrPHCEM"),
    ("Beancount - The Beancount Universe", "1K8l4eU3bBFaU1U_7sV9-3XRD0YDXPQP4b8t7ehk5cVk"),
    ("Beancount - Trading Options", "1YcFo17bO98TSxcIOehBQ_zDqm59CI1yyit7tP_Wdjyc"),
    ("Beancount - Ulque", "1hJCIpkl1ngF5v-a63s5HBPZX4aoXMQORR-EJjAQDUvo"),
    ("Beancount - Exporting your Portfolio (New)", "1mNyE_ONuyEkF_I2l6V_AoAU5HJgI654AOBhHsnNPPqw"),
    ("LedgerHub - Post-Mortem", "1Bln8Zo11Cvez2rdEgpnM-oBHC1B6uPC18Qm7ulobolM"),
    ("TRASH", "1lkFz-cUz_j_R3aHNp786ZB9fWcN7wxoZzdSnZ5Z3ILg"),
    ("Exposing Protocol Buffers from C++", "1xiFw7OLsFux8wWrZ3JqofuIsjIcIr4RuYrh7NdgMjeE"),
    ("Questions for haberman@", "1Z9edeb4oldExImuxq4-4ZnW0WnuYQRsstiaBwJuyL8c"),
    ("Beancount - Parsed Comments", "1yestw21g4AEMNrIUsBuOaxucfz3_7eMAR6NYnVnTzV0"),
    ("Beancount - Cookbook - Sharing Expenses", "1FRcJqUfeAMQO6KjG94w6rF7VajMGJaFplmF1Wu0rCHY"),
    ("Beancount - Design Doc", "1N7HDXuNWgLG2PqFS4Kkgv5LzAAtU6c97UVNT7tdTIjA"),
    ("Beancount - Scripting & Plugins", "1QftxNvQPdH-MikMBHupftU6F4IsNZP5FlFh1LCbVgk8"),
    ("LedgerHub - Design Doc", "11u1sWv7H7Ykbc7ayS4M9V3yKqcuTY7LJ3n1tgnEN2Hk"),
    ("Beancount - Cookbook - Vesting", "1mHNlNMTZsKPMjP_qQmedoizZFQy1-GzlR2lX5zy_0ok"),
    ("Beancount - Calculating Portfolio Returns (Old)", "1vEFB44-HFqydYVJXA-QxT4AN0K5xHHfSkhTmRSCPkac"),
    ("Universal Lightweight Query Engine", "1uemjVaZrFa-nnPNojZVMyLYTpWCT17cTPSOkCofuNFg"),
    ("Beancount - Migration to Git", "1B_HgWkrg36B7QoilWbLd2BAEDee8n-WGd7Mh5cT1NLQ"),
    ("Beancount - Solving the Conversions Problem", "1rW7zQyMiv8hKZ0993pwQiu5vTxzEOQf_Q67GvVk6zu0"),
    ("Beancount - Cookbook - In-Progress", "1lAKWL7hbeYVuDd1v5SiccEmj220XNumz8we8znNdx58"),
    ("Beancount - Exporting your Portfolio", "1eZIDRmQZxR6cmDyOJf7U3BnCm4PDMah2twxYFfKPJtM"),
    ("Beancount - Self-Reductions", "16dKnXJ7KZhemPs5NPHmSTNCV7LUPrMD9jFgiV79Npb8"),
    ("Beancount - Options Reference", "1_-T_BvDtUjj9M7liZMNSkrL8pgC60TGMBlYCiV1e4ZM"),
    ("Beancount - Snippets", "191zP806Wlkhv5aKSQ-eYIG9dKbQhw1a5cZRRxh1m6cI"),
    ("Beancount - Interpolation", "1t2AgozNduKEMsFoEfy_i1C_lKKVLArzsnpdzG_IUey4"),
    ("LedgerHub - Instructions & Status", "1vnvqQNGaHOM3opRnEZspvALpv-G6fVQq0bSgAchVpuk"),
    ("Beancount - Documents about CAs", "1m71AKKWKl9j3YhRLFK8C1AHaxXY_VkTFv_aJEQb1ng8"),
    ("Beancount - Contributor Agreement", "1B4KQrUzyhtxzm_RojXLYHL_0xqRRLuR8gxreu3mwv-4"),
    ("Beancount - Contributing", "1nIj00U8wI7rcOo5wHEG54cyQz4X6GoW7G8FWJmF1hrI"),
    ("Beancount - Fetching Prices", "1EZCP8VX3cOuyp2CKECfsq0LAfaXcHTVr7-EKIsRJBa8"),
    ("Beancount - Developer Guidelines", "1l6YmKIPUsucrooofdrollO6Re2rTPJA9KigoS8OBluk"),
    ("Beancount - Converting", "1tkoUeSfZyEhEGdXHwYp5vBrSrNDgC4FVXhReSWsILlw"),
    ("Beancount - Custom Application: Return on Property", "1SnR7BdE2VXFTMEvnkhAd9PwXu_AxytTYpiS1LjXdP0E"),
    ("Beancount - Using Equity Accounts", "1H6C4YNPSe8GvC9Pe4Mp84q7ErPwI2AlZrFfKuNq-TG4"),
    ("Beancount - Wash Sales", "1hByM4oV9Q9BS66SimgRov1gcD72ykn4acmFbWj5g66M"),
    ("Accounting - Links", "1fzsGnYz3r8lthpU6A2O6eddNREOnl5-85zcwsXwMTyU"),
    ("Beancount - Proposal - Inventory Booking Improvements", "1F8IJ_7fMHZ75XFPocMokLxVZczAhrBRBVN9uMhQFCZ4"),
    ("Beancount - Proposal - Rounding & Precision", "1MY2JMiiXUmcwsOT0CkiK-fCo0ZE7nbr8uTcTL50b6X4"),
    ("Beancount - Proposal - Fund Accounting", "1nf_yCiLuewVCEjkXq9Kd9SqbZGWqcs0v0pT5xQnkyzs"),
    ("Beancount - Proposal - Balance Assertions", "1vyemZFox47IZjuBrT2RjhSHZyTgloYOUeJb73RxMRD0"),
    ("Beancount - Proposal - Settlement Dates", "1x0qqWGRHi02ef-FtUW172SHkdJ8quOZD-Xli7r4Nl_k"),
]

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
        # Don't try to find context for very short strings (like "TODO")
        return None

    if normalized_quoted not in normalized_full:
        return None

    lines = full_text.splitlines()
    
    # Pre-normalize all lines for matching
    normalized_lines = [normalize(line) for line in lines]
    
    # Try to find which line(s) contain the quoted text
    for i, n_line in enumerate(normalized_lines):
        if normalized_quoted in n_line:
            start = max(0, i - lines_before)
            end = min(len(lines), i + lines_after + 1)
            return "\n".join(lines[start:end])
    
    # If not found in a single line, it might span multiple lines.
    # Let's search for the first 20 chars of normalized_quoted.
    first_part = normalized_quoted[:20]
    for i, n_line in enumerate(normalized_lines):
        if first_part in n_line:
            start = max(0, i - lines_before)
            end = min(len(lines), i + lines_after + 1)
            return "\n".join(lines[start:end])

    return None

async def process_doc(name, file_id):
    async with semaphore:
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
            return

        try:
            data = json.loads(stdout.decode())
            comments = data.get("comments", [])
            unresolved = [c for c in comments if not c.get("resolved", False)]
            
            if not unresolved:
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

            md_content = []
            for c in unresolved:
                quoted_obj = c.get("quotedFileContent", {})
                quoted_value = quoted_obj.get("value", "")
                
                context = None
                if doc_text and quoted_value:
                    context = get_context(doc_text, quoted_value)
                
                # Always show the highlighted selection
                unescaped_quote = html.unescape(quoted_value) if quoted_value else "[No selection]"
                md_content.append(f"> {unescaped_quote}\n\n")
                
                # Show context block if found
                if context:
                    md_content.append(f"```text\n{context}\n```\n\n")
                
                author = c.get("author", {}).get("displayName", "Unknown")
                content = c.get("content", "")
                md_content.append(f"**{author}**: {content}\n")
                
                for r in c.get("replies", []):
                    r_author = r.get("author", {}).get("displayName", "Unknown")
                    r_content = r.get("content", "")
                    md_content.append(f"  - **{r_author}**: {r_content}\n")
                
                md_content.append("\n---\n")

            if md_content:
                # Replace slashes in filename
                safe_name = name.replace("/", "_").replace("\\", "_")
                filename = f"{safe_name}.md"
                with open(filename, "w") as f:
                    f.write("".join(md_content))
                print(f"Created: {filename}")

        except Exception as e:
            print(f"Exception processing {name}: {e}")

async def main():
    tasks = [process_doc(name, file_id) for name, file_id in DOCS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
