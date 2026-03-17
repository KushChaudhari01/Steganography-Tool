"""
LSB Steganography Tool - Core Module
Hides and extracts secret messages in PNG images using Least Significant Bit technique.
"""

from PIL import Image
import os

DELIMITER = "$$END$$"


def get_capacity(image_path):
    """Returns max number of characters that can be hidden in the image."""
    img = Image.open(image_path).convert("RGB")
    pixels = img.size[0] * img.size[1]
    max_bits = pixels * 3
    max_chars = max_bits // 8
    return max_chars - len(DELIMITER)


def encode(image_path, message, output_path, password=None):
    """
    Hides a secret message inside an image using LSB steganography.

    Args:
        image_path  : Path to the cover image (PNG recommended)
        message     : The secret text to hide
        output_path : Where to save the encoded image (must be .png)
        password    : Optional password for XOR encryption
    """
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    if password:
        message = xor_encrypt(message, password)

    full_message = message + DELIMITER
    binary_msg = ''.join(format(ord(c), '08b') for c in full_message)

    max_bits = len(pixels) * 3
    if len(binary_msg) > max_bits:
        raise ValueError(
            f"Message too large! Max capacity: {(max_bits // 8) - len(DELIMITER)} chars, "
            f"your message: {len(message)} chars."
        )

    new_pixels = []
    bit_idx = 0

    for pixel in pixels:
        r, g, b = pixel
        channels = [r, g, b]
        new_channels = []
        for channel in channels:
            if bit_idx < len(binary_msg):
                # Clear LSB and set it to the message bit
                channel = (channel & ~1) | int(binary_msg[bit_idx])
                bit_idx += 1
            new_channels.append(channel)
        new_pixels.append(tuple(new_channels))

    new_img = Image.new("RGB", img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path, "PNG")
    print(f"[+] Message encoded successfully!")
    print(f"[+] Output saved to: {output_path}")
    print(f"[+] Bits used: {len(binary_msg)} / {max_bits}")


def decode(image_path, password=None):
    """
    Extracts a hidden message from an encoded image.

    Args:
        image_path : Path to the encoded image
        password   : Optional password for XOR decryption (must match encode password)

    Returns:
        The hidden message string, or an error message.
    """
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    binary_str = ""
    for pixel in pixels:
        for channel in pixel:
            binary_str += str(channel & 1)  # Extract LSB

    # Convert bits back to characters
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))

    message = ''.join(chars)

    if DELIMITER in message:
        hidden = message[:message.index(DELIMITER)]
        if password:
            hidden = xor_encrypt(hidden, password)  # XOR is symmetric
        return hidden

    return "[!] No hidden message found in this image."


def xor_encrypt(text, key):
    """XOR encryption/decryption (symmetric — same function for both)."""
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))


def compare_images(original_path, encoded_path):
    """Compares two images and shows pixel difference stats."""
    orig = Image.open(original_path).convert("RGB")
    enc = Image.open(encoded_path).convert("RGB")

    if orig.size != enc.size:
        print("[!] Images are different sizes, cannot compare.")
        return

    orig_pixels = list(orig.getdata())
    enc_pixels = list(enc.getdata())

    changed = sum(1 for a, b in zip(orig_pixels, enc_pixels) if a != b)
    total = len(orig_pixels)
    print(f"[*] Total pixels: {total}")
    print(f"[*] Changed pixels: {changed} ({100 * changed / total:.2f}%)")
    print(f"[*] Max possible channel difference: ±1 (invisible to human eye)")
