"""
LSB Steganography Tool - Command Line Interface
Usage examples at bottom of file.
"""

import argparse
import sys
import os
from steganography import encode, decode, get_capacity, compare_images

BANNER = """
  ╔═══════════════════════════════════════╗
  ║     LSB Steganography Tool v1.0       ║
  ║   Hide secrets inside images          ║
  ╚═══════════════════════════════════════╝
"""

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="Hide and extract secret messages in images using LSB steganography",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --- ENCODE ---
    enc_parser = subparsers.add_parser("encode", help="Hide a message in an image")
    enc_parser.add_argument("image",   help="Path to the cover image (PNG/JPG)")
    enc_parser.add_argument("message", help="Secret message to hide")
    enc_parser.add_argument("output",  help="Output image path (must be .png)")
    enc_parser.add_argument("-p", "--password", help="Optional password for encryption", default=None)

    # --- DECODE ---
    dec_parser = subparsers.add_parser("decode", help="Extract a hidden message from an image")
    dec_parser.add_argument("image", help="Path to the encoded image")
    dec_parser.add_argument("-p", "--password", help="Password used during encoding", default=None)

    # --- CAPACITY ---
    cap_parser = subparsers.add_parser("capacity", help="Check how many characters an image can hide")
    cap_parser.add_argument("image", help="Path to the image")

    # --- COMPARE ---
    cmp_parser = subparsers.add_parser("compare", help="Compare original vs encoded image")
    cmp_parser.add_argument("original", help="Path to original image")
    cmp_parser.add_argument("encoded",  help="Path to encoded image")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # --- Route to function ---
    try:
        if args.command == "encode":
            if not os.path.exists(args.image):
                print(f"[!] Error: Image not found: {args.image}")
                sys.exit(1)
            if not args.output.endswith(".png"):
                print("[!] Warning: Output should be .png to avoid compression loss")
            encode(args.image, args.message, args.output, args.password)

        elif args.command == "decode":
            if not os.path.exists(args.image):
                print(f"[!] Error: Image not found: {args.image}")
                sys.exit(1)
            result = decode(args.image, args.password)
            print(f"[+] Hidden message: {result}")

        elif args.command == "capacity":
            if not os.path.exists(args.image):
                print(f"[!] Error: Image not found: {args.image}")
                sys.exit(1)
            cap = get_capacity(args.image)
            print(f"[+] This image can hide up to {cap} characters")

        elif args.command == "compare":
            compare_images(args.original, args.encoded)

    except ValueError as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────
# USAGE EXAMPLES:
#
# Basic encode:
#   python cli.py encode photo.png "Meet at midnight!" output.png
#
# Encode with password:
#   python cli.py encode photo.png "Top secret" output.png -p mypassword
#
# Decode:
#   python cli.py decode output.png
#
# Decode with password:
#   python cli.py decode output.png -p mypassword
#
# Check capacity:
#   python cli.py capacity photo.png
#
# Compare original vs encoded:
#   python cli.py compare photo.png output.png
# ─────────────────────────────────────────────
