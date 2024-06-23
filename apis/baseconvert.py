import base64


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        # Decode bytes to string and add padding if needed
        encoded_string = encoded_bytes.decode(
            'utf-8').rstrip("=") + "=" * (3 - (len(encoded_bytes) % 3))
    return encoded_string


if __name__ == "__main__":
    image_path = r"C:\Users\adars\OneDrive\Desktop\mecl\test_ocr.jpg"
    base64_string = image_to_base64(image_path)
    print("Base64 Encoded String:")
    print(base64_string)
