import sys
from rembg import remove
from PIL import Image
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("usage: remove_bg.py input output")
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()

    img = Image.open(input_path).convert("RGBA")
    result = remove(img)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path)

    print(f"saved: {output_path}")

if __name__ == "__main__":
    main()
