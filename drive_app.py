import streamlit as st
from helper import download_pdf_from_drive, process_pdf, extract_markdown, prompt
from langchain_community.llms import Ollama

# Streamlit app
st.title("Annotated PDF Summary by Llama")
st.write("Developed by [Srijit Mukherjee](https://www.linkedin.com/in/srijit-mukherjee/). Code available at [Github](https://github.com/mukherjeesrijit/annotated-pdf-summary).")

tabs = st.tabs(["PDF Process", "Annotated Summary"])

with tabs[0]:
    st.header("PDF Process")

    file_id = st.text_input("Google Drive File ID")

    if st.button("Process PDF"):
        if file_id:
            with st.spinner('Downloading PDF from Google Drive...'):
                pdf_file = download_pdf_from_drive(file_id)
                st.success('PDF downloaded successfully.')

            with st.spinner('Processing PDF...'):
                df_sorted = process_pdf(pdf_file)
                st.success('PDF processed successfully.')

            st.write(df_sorted)

            example = """ 
            {
            - **Brief Subtitle 1:** Description 1.
            - **Brief Subtitle 2:** Description 2.
            }
            """
            llm = Ollama(model="llama3.1")

            combined_markdown = []
            for _, row in df_sorted.iterrows():
                text = row['Text']
                comment = row['Comment']
                output = prompt(example, text, comment, llm)
                markdown_output = extract_markdown(output)
                combined_markdown.append(markdown_output)

            combined_markdown_content = "\n".join(combined_markdown)

            # Store the Markdown content in session state for later use
            st.session_state.markdown_content = combined_markdown_content

        else:
            st.error("Please provide the Google Drive file ID.")

with tabs[1]:
    st.header("Annotated Summary")

    # Check if Markdown content is available
    if 'markdown_content' in st.session_state:
        st.markdown("### Preview")
        st.markdown(st.session_state.markdown_content)
        st.download_button("Download Markdown", data=st.session_state.markdown_content, file_name='combined_output.md')
    else:
        st.info("Process a PDF first to see the summary.")
