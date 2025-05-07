import requests
import fitz  # PyMuPDF
import tempfile
import subprocess
import json

def download_pdf(pdf_url: str) -> str:
    response = requests.get(pdf_url)
    response.raise_for_status()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name

def extract_all_paragraphs(pdf_path: str):
    doc = fitz.open(pdf_path)
    result = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        for idx, para in enumerate(paragraphs):
            result.append({
                "page": page_num,
                "index": idx,
                "original": para,
                "translation": ""
            })
    return result

def translate_with_ollama(text: str, target_language: str = "Chinese") -> str:
    prompt = f"Translate the following English text to {target_language}:\n\n{text}"
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise RuntimeError("Ollama translation failed:\n" + result.stderr.decode("utf-8"))
    return result.stdout.decode("utf-8").strip()

def translate_all(paragraphs, target_language: str = "Chinese"):
    for para in paragraphs:
        print(f"翻译第 {para['page']} 页，第 {para['index']} 段...")
        para["translation"] = translate_with_ollama(para["original"], target_language)
    return paragraphs

def save_translation_json(paragraphs, output_path="translated_output.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 翻译副本已保存到 {output_path}")

# 示例主函数
if __name__ == "__main__":
    pdf_url = "https://arxiv.org/pdf/2106.14881.pdf"
    pdf_path = download_pdf(pdf_url)
    all_paragraphs = extract_all_paragraphs(pdf_path)
    
    translated_paragraphs = translate_all(all_paragraphs, target_language="Chinese")
    
    save_translation_json(translated_paragraphs)
