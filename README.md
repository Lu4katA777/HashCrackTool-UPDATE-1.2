# HashCrackBG

Educational hash cracking tool made in Bulgaria.
Built for learning, lab testing and fun.

> This project is for educational purposes only.
> Do NOT use it for illegal activities.

---

## Version 1.2

### What's new

- Brute-force cracking mode
- 3 built-in wordlists:
  - `low.txt`
  - `medium.txt`
  - `high.txt`
- New `-h` help command
- Improved CLI interface
- Improved password mutation system
- Progress and speed statistics
- Automatic saving of found passwords

---

## Features

- Hash generator (MD5, SHA1, SHA256 etc.)
- Wordlist cracking
- Smart mutations:
  - case variations
  - numbers (123456, 2025 etc.)
  - symbols (! @ #)
  - leet (@ 1 0)
  - mixed case variations
  - number interleaving
- Brute-force mode
- Speed display (hashes/sec)
- Progress stats
- Auto-save found passwords → `found.txt`
- Color terminal UI

---

Install dependency:

```bash
pip3 install colorama
```

---

## Help

To see all available commands:

```bash
python3 HashCrackBG.py -h
```

Available commands:

```text
generate    Generate a hash
crack       Crack hash using a wordlist
brute       Brute-force a hash
```

You can also get help for a specific command:

```bash
python3 HashCrackBG.py generate -h
```

```bash
python3 HashCrackBG.py crack -h
```

```bash
python3 HashCrackBG.py brute -h
```

---

## Usage

### Generate hash

Generate a hash from a text:

```bash
python3 HashCrackBG.py generate -t password123 -a md5
```

The default algorithm is MD5, so `-a md5` can also be omitted:

```bash
python3 HashCrackBG.py generate -t password123
```

Other algorithms supported by Python hashlib can also be used:

```bash
python3 HashCrackBG.py generate -t password123 -a sha256
```

---

### Crack hash

Crack a hash using a wordlist:

```bash
python3 HashCrackBG.py crack -hsh HASH -w wordlist.txt -a md5
```

Example:

```bash
python3 HashCrackBG.py crack -hsh 249184d5a8efb213886762d1cc915253 -w wordlist.txt
```

The tool will test the words from the wordlist and automatically generate additional mutations.

---

## Wordlists

HashCrackBG includes three wordlist levels:

```text
wordlists/
├── low.txt
├── medium.txt
└── high.txt
```

### Low

A smaller wordlist designed for quick tests.

### Medium

A larger wordlist containing more words and common password patterns.

### High

The largest wordlist containing a much larger number of candidates.

You can also use your own wordlist:

```bash
python3 HashCrackBG.py crack -hsh HASH -w mywordlist.txt
```

---

## Brute Force

HashCrackBG also includes a brute-force mode.

```bash
python3 HashCrackBG.py brute -hsh HASH -a md5 -m 4
```

Options:

```text
-hsh    Target hash
-a      Hash algorithm
-m      Maximum password length
```

Example:

```bash
python3 HashCrackBG.py brute -hsh HASH -a md5 -m 5
```

The brute-force mode tests combinations from the configured character set.

As password length increases, the number of possible combinations grows very quickly. Long randomly generated passwords may therefore take a very long time to test.

---

## Output

If a password is found:

```text
[+] FOUND: password123
[+] Base: password
[+] Attempts: 247753972
[+] Speed: 229016/s
```

The result is automatically saved to:

```text
found.txt
```
