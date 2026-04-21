#!/usr/bin/env python3
import sys
import tiktoken

def count_tokens(text):
    # Using cl100k_base encoding (works for most models)
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)

def format_size(num_tokens):
    # Rough conversion: 1 token ≈ 0.75 words, 1 token ≈ 4 bytes
    words = int(num_tokens * 0.75)
    bytes_approx = num_tokens * 4
    kb = bytes_approx / 1024
    
    return {
        "tokens": num_tokens,
        "words": words,
        "kb": round(kb, 2)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: prompt-size.py 'your prompt' [file1] [file2] ...")
        sys.exit(1)
    
    prompt = sys.argv[1]
    files = sys.argv[2:] if len(sys.argv) > 2 else None
    
    full_text = prompt
    
    if files:
        for f in files:
            try:
                with open(f, 'r') as fh:
                    full_text += f"\n--- FILE: {f} ---\n{fh.read()}\n"
            except FileNotFoundError:
                print(f"Error: {f} not found")
                sys.exit(1)
    
    size = format_size(count_tokens(full_text))
    
    print(f"Prompt size:")
    print(f"  Tokens: {size['tokens']:,}")
    print(f"  Words: ~{size['words']:,}")
    print(f"  KB: ~{size['kb']}")
    print()
    print(f"Model limits:")
    print(f"  phi3:mini (128K): {'✓ OK' if size['tokens'] < 128000 else '✗ TOO BIG'}")
    print(f"  qwen/mistral (32K): {'✓ OK' if size['tokens'] < 32000 else '✗ TOO BIG'}")
    print(f"  llama3 (8K): {'✓ OK' if size['tokens'] < 8000 else '✗ TOO BIG'}")