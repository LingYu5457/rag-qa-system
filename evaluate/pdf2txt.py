import glob
import os

from rag.document_processing.parse import FileParserPipeline


def convert_all_pdfs(eval_dir: str = "data/eval"):
    pipeline = FileParserPipeline()
    pdf_files = glob.glob(os.path.join(eval_dir, "**/*.pdf"), recursive=True)

    for pdf_path in pdf_files:
        txt_path = os.path.splitext(pdf_path)[0] + ".txt"
        print(f"Converting: {pdf_path} -> {txt_path}")

        docs = pipeline.parse_file(pdf_path)
        if docs is None:
            print(f"  FAILED to parse {pdf_path}")
            continue

        text = "\n".join(doc.page_content for doc in docs)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  Done ({len(text)} chars)")

    print(f"\nAll done. {len(pdf_files)} files processed.")


if __name__ == "__main__":
    convert_all_pdfs()
