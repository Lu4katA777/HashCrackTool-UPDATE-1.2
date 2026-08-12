#!/usr/bin/env python3

import hashlib
import argparse
import sys
import time
from pathlib import Path
from colorama import Fore, init
import itertools

init(autoreset=True)


def banner():
    print(Fore.CYAN + r"""
██╗  ██╗ █████╗ ███████╗██╗  ██╗
██║  ██║██╔══██╗██╔════╝██║  ██║
███████║███████║███████╗███████║
██╔══██║██╔══██║╚════██║╚════██║
██║  ██║██║  ██║███████║███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝

HashCrack Lab Tool
""")

    print(Fore.YELLOW + "Version 1.2")
    print()
    print(Fore.WHITE + "What's new:")
    print()
    print(Fore.GREEN + "  [+] Brute-force option added")
    print(Fore.GREEN + "  [+] 3 new wordlists: low, medium, high")
    print(Fore.GREEN + "  [+] Help command added")
    print()
    print(Fore.BLUE + "  [+] Made by Lu4kata A.K.A WolfSec")

# ===== Warning =====
def warning_prompt():
    print(Fore.RED + "\n[!] Educational use only\n")
    if input("Continue? [y/n]: ").lower() != "y":
        sys.exit()

# ===== EXTRA GENERATORS =====

def interleave_numbers(word):
    results = set()
    nums = "1234567890"

    combo = ""
    for i, ch in enumerate(word):
        combo += ch
        if i < len(nums):
            combo += nums[i]
    results.add(combo)

    return results


def random_case_variants(word, limit=200):
    results = set()
    combos = itertools.product(*[(c.lower(), c.upper()) for c in word])

    for i, combo in enumerate(combos):
        if i > limit:
            break
        results.add("".join(combo))

    return results


def insert_symbol_number(word):
    results = set()
    symbols = ["#", "@", "!", "$"]

    for i in range(len(word)):
        for sym in symbols:
            for n in ["1","12","123","1234"]:
                results.add(word[:i] + sym + word[i:] + n)

    return results

def advanced_mutations(word):
    results = set()

    numbers = "1234567890"
    symbols = ["!", "@", "#", "$", "!@", "@!", "#!", "$!"]

    # q1w2e3r4t5y6
    combo = ""
    for i, ch in enumerate(word):
        combo += ch
        if i < len(numbers):
            combo += numbers[i]

    results.add(combo)

    # q1w2e3r4t5y6!@
    for symbol in symbols:
        results.add(combo + symbol)

    return results


# ===== MUTATIONS =====
def generate_mutations(word):
    variations = set()

    numbers = ["1","12","123","1234","885","000","133","12345"]
    symbols = ["#", "@", "!", "$"]

    # base forms
    base_forms = {
        word,
        word.lower(),
        word.upper(),
        word.capitalize(),
        word.swapcase(),
    }

    # mixed case variants
    mixed_variants = set()
    for combo in itertools.product(*[(c.lower(), c.upper()) for c in word]):
        mixed_variants.add("".join(combo))
        if len(mixed_variants) > 200:  # limit
            break

    base_forms.update(mixed_variants)

    for base in base_forms:
        variations.add(base)

        # numbers at end
        for n in numbers:
            variations.add(base + n)

        # symbol anywhere + numbers
        for sym in symbols:
            for i in range(1, len(base)):
                mid = base[:i] + sym + base[i:]
                variations.add(mid)

                for n in numbers:
                    variations.add(mid + n)

        # advanced mutations for every base form
        variations.update(advanced_mutations(base))

        # numbers at end
        for n in numbers:
            variations.add(base + n)

        # symbol anywhere + numbers
        for sym in symbols:
            for i in range(1, len(base)):
                mid = base[:i] + sym + base[i:]
                variations.add(mid)

                for n in numbers:
                    variations.add(mid + n)

    # interleave
    nums = "1234567890"
    combo = ""
    for i, ch in enumerate(word):
        combo += ch
        if i < len(nums):
            combo += nums[i]
    variations.add(combo)


    return variations




# ===== HASH =====
def make_hash(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()

# ===== CRACK =====
def crack_hash(target_hash, wordlist, algo):
    path = Path(wordlist)

    if not path.exists():
        print("Wordlist not found")
        sys.exit()

    print(Fore.CYAN + "\n[*] Cracking...\n")

    start = time.time()
    attempts = 0

    with open(path,"r",errors="ignore") as f:
        for word in f:
            word = word.strip()
            mutations = generate_mutations(word)

            for variant in mutations:
                attempts += 1

                if make_hash(variant, algo) == target_hash:
                    speed = int(attempts/(time.time()-start+0.001))

                    print(Fore.GREEN + f"\n[+] FOUND: {variant}")
                    print(Fore.YELLOW + f"[+] Base: {word}")
                    print(Fore.CYAN + f"[+] Attempts: {attempts}")
                    print(Fore.MAGENTA + f"[+] Speed: {speed}/s")

                    with open("found.txt","a") as out:
                        out.write(f"{variant} | {target_hash}\n")

                    print(Fore.GREEN + "[+] Saved to found.txt\n")
                    return

                if attempts % 5000 == 0:
                    speed = int(attempts/(time.time()-start+0.001))
                    print(Fore.MAGENTA + f"Checked: {attempts} | {speed}/s")

    print(Fore.RED + "\n[-] Hash not found")

    # ===== BRUTEFORCE =====
def brute_force(target_hash, algo, max_length):
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()~,."

        print(Fore.CYAN + "\n[*] Brute-force mode")
        print(Fore.YELLOW + f"[*] Max length: {max_length}\n")

        start = time.time()
        attempts = 0

        for length in range(1, max_length + 1):

            for combo in itertools.product(charset, repeat=length):

                candidate = "".join(combo)
                attempts += 1

                if make_hash(candidate, algo) == target_hash:
                    speed = int(
                        attempts / (time.time() - start + 0.001)
                    )

                    print(Fore.GREEN + f"\n[+] FOUND: {candidate}")
                    print(Fore.CYAN + f"[+] Attempts: {attempts}")
                    print(Fore.MAGENTA + f"[+] Speed: {speed}/s")

                    with open("found.txt", "a") as out:
                        out.write(f"{candidate} | {target_hash}\n")

                    return

                if attempts % 5000 == 0:
                    speed = int(
                        attempts / (time.time() - start + 0.001)
                    )

                    print(
                        Fore.MAGENTA +
                        f"Checked: {attempts} | {speed}/s"
                    )

        print(Fore.RED + "\n[-] Hash not found")

# ===== GENERATE =====
def generate_hash(text, algo):
    print(Fore.GREEN + f"\nHash: {make_hash(text, algo)}\n")

# ===== CLI =====
def main():

    parser = argparse.ArgumentParser(
        prog="HashCrack",
        description="HashCrack Lab Tool"
    )

    sub = parser.add_subparsers(dest="cmd")

    g = sub.add_parser(
        "generate",
        help="Generate a hash"
    )

    g.add_argument(
        "-t",
        "--text",
        required=True
    )

    g.add_argument(
        "-a",
        "--algo",
        default="md5"
    )

    c = sub.add_parser(
        "crack",
        help="Crack hash using a wordlist"
    )

    c.add_argument(
        "-hsh",
        "--hash",
        required=True
    )

    c.add_argument(
        "-w",
        "--wordlist",
        required=True
    )

    c.add_argument(
        "-a",
        "--algo",
        default="md5"
    )

    b = sub.add_parser(
        "brute",
        help="Brute-force a hash"
    )

    b.add_argument(
        "-hsh",
        "--hash",
        required=True
    )

    b.add_argument(
        "-a",
        "--algo",
        default="md5"
    )

    b.add_argument(
        "-m",
        "--max-length",
        type=int,
        default=4
    )

    args = parser.parse_args()
    args = parser.parse_args()

    if args.cmd is None:
        banner()
        return

    if args.cmd == "generate":
        warning_prompt()
        generate_hash(args.text, args.algo)

    elif args.cmd == "crack":
        warning_prompt()
        crack_hash(
            args.hash,
            args.wordlist,
            args.algo
        )

    elif args.cmd == "brute":
        warning_prompt()
        brute_force(
            args.hash,
            args.algo,
            args.max_length
        )

if __name__ == "__main__":
    main()
