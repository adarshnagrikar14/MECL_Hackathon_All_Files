import requests
import tempfile
import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import re


def fetch_pdf_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(response.content)
            temp_filename = temp_file.name

        text = pdf_to_text(temp_filename)
        os.remove(temp_filename)

        return text

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch PDF: {e}")
        return ""


def pdf_to_text(pdf_path):
    try:
        text = extract_text(pdf_path, laparams=LAParams())
        return text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def remove_non_english(text):
    english_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    english_text = ' '.join(english_text.split())
    return english_text


def chunk_text_into_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences


def chunk_into_4_sentences(sentences):
    chunks = []
    for i in range(0, len(sentences), 4):
        chunks.append(" ".join(sentences[i:i + 4]))
    return chunks


if __name__ == "__main__":
    pdf_url = r'https://firebasestorage.googleapis.com/v0/b/mecl-chatbot.appspot.com/o/uploads%2F652cc26c47f961697432172.pdf?alt=media&token=a325b769-dff1-4e5e-84c9-075d44359f5b'
    extracted_text = fetch_pdf_text(pdf_url)
    if extracted_text:
        normalized_text = (extracted_text)
        english_text = remove_non_english(normalized_text)
        sentences = chunk_text_into_sentences(english_text)
        sentence_chunks = chunk_into_4_sentences(sentences)
        for index, chunk in enumerate(sentence_chunks):
            print(f"Chunk {index + 1}:")
            print(chunk)
            print('\n')
