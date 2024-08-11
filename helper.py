from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import fitz  # PyMuPDF
import pandas as pd
from langchain_community.llms import Ollama
import re

def extract_markdown(markdown_text):
    # Extract bullet points using regex
    bullet_points = re.findall(r'\* \*\*(.*?)\*\*: (.*)', markdown_text)
    # Convert to Markdown format
    markdown_lines = [f"* **{subtitle}**: {description}" for subtitle, description in bullet_points]
    # Combine lines into a single Markdown content
    markdown_content = "\n".join(markdown_lines)
    return markdown_content

def prompt(example, text, comment, llm):
    prompt_text = f"Please provide a list of main points using bullet points in Markdown format based on the following {text} and {comment} like {example}. Output Format: Use Markdown format for each bullet point. Each bullet should be a concise summary of the key information. Ensure clarity and relevance to the provided text and comment."
    out = llm.invoke(prompt_text)
    return out

def download_pdf_from_drive(file_id):
    credentials_file = 'credentials.json' #download this from Google Cloud Console 
    # Authenticate using the service account
    creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    file.seek(0)
    return file

def process_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    data = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        comments = page.annots()
        blocks = page.get_text('dict')['blocks']
        all_lines = []
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    line_rect = fitz.Rect(
                        line['bbox'][0], line['bbox'][1],  # x0, y0
                        line['bbox'][2], line['bbox'][3]   # x1, y1
                    )
                    all_lines.append(line_rect)

        if comments:
            for comment in comments:
                rect = comment.rect
                text_around_comment = page.get_text('text', clip=rect).strip()
                comment_content = comment.info.get('content', '') or \
                                  comment.info.get('title', '') or \
                                  comment.info.get('subject', '')
                line_numbers = [i + 1 for i, line_rect in enumerate(all_lines) if rect.intersects(line_rect)]
                if not line_numbers:
                    continue
                min_line_number = min(line_numbers)
                data.append([
                    page_num + 1,
                    min_line_number,
                    text_around_comment,
                    comment_content
                ])
    df = pd.DataFrame(data, columns=['Page Number', 'Line Number', 'Text', 'Comment'])
    df_sorted = df.sort_values(by=['Page Number', 'Line Number'])
    return df_sorted
