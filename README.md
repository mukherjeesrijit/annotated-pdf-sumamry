# Annotated PDF Summary

**Annotated PDF Summary** is a web application designed to process and summarize annotated PDF documents using advanced language models. This app enables users to upload PDFs, extract and organize comments and text, generate summaries, and download the results in Markdown format. It's particularly useful for research purposes, where users need to manage and analyze large volumes of annotated documents. This uses Llama3.1 to extract your annotated texts and comments to generate a summary of your observations into a markdown file.

## Features

- **PDF Upload**: Upload your PDF files directly from your local system.
- **PDF Processing**: Extract text and annotations from the PDF.
- **Markdown Summary**: Generate a summary of annotations and text in Markdown format using a language model.
- **Preview and Download**: Preview the generated Markdown summary and download it for further use.

## Installation

To run this app locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/mukherjeesrijit/annotated-pdf-summary.git
    cd annotated-pdf-summary
    ```

2. **Create a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Drive App / **:
    ```bash
    streamlit run drive_app.py # for drive link of pdf
    streamlit run pdf_app.py # for pdf upload
    ```

## Usage

1. **Upload PDF**: Use the file upload feature to select and upload your PDF document.
2. **Process PDF**: Click on the "Process PDF" button to download, process, and analyze the PDF file.
3. **View Summary**: Navigate to the "Summary" tab to preview and download the Markdown summary.

## Dependencies

- `streamlit`: For the web app interface.
- `google-auth`: For Google Drive API authentication.
- `google-api-python-client`: To interact with the Google Drive API.
- `PyMuPDF`: For PDF processing and text extraction.
- `pandas`: For data manipulation and processing.
- `langchain-community`: For interacting with language models.
- `fpdf`: For PDF creation (if needed).
- `markdown2`: For converting Markdown to HTML (if needed).

## Notes

- Ensure you have a Google Cloud Service Account JSON file for Drive API access.
- Modify the `credentials_file` path in `app.py` as needed.
- For PDF processing, ensure the necessary libraries are installed and configured correctly.

## Contributing

Contributions are welcome! Please submit issues or pull requests to improve the functionality or fix bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact [Srijit Mukherjee](https://www.linkedin.com/in/srijit-mukherjee/).
