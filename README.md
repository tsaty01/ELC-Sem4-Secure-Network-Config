# Secure Network Configuration (ELC-EVENSEM-25-26)

This is a solution for the ELC activity.

## Setup

```cmd
pip install uv
uv venv
.venv\Scripts\activate
```

## CLI

For more, run `python main.py -h`.

```cmd
> python main.py --help
usage: main.py [-h] {caesar,playfair,hill,bench} ...
Cryptographic Cipher Toolkit

positional arguments:
  {caesar,playfair,hill,bench}
                        Available commands
    caesar              use Caesar Cipher
    playfair            use Playfair Cipher
    hill                use Hill Cipher
    bench               Benchmark ciphers and generate a graph

options:
  -h, --help            show this help message and exit
```
