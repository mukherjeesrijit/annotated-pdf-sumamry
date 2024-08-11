import streamlit as st
from helper import extract_markdown, prompt, process_pdf
from langchain_community.llms import Ollama

# Streamlit app
st.title("Annotated PDF Summary by Llama")
st.write("Developed by [Srijit Mukherjee](https://www.linkedin.com/in/srijit-mukherjee/). Code available at [Github](https://github.com/mukherjeesrijit/annotated-pdf-summary).")

tabs = st.tabs(["PDF Process", "Annotated Summary"])

with tabs[0]:
    st.header("PDF Process")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if st.button("Process PDF") and uploaded_file:
        with st.spinner('Processing PDF...'):
            df_sorted = process_pdf(uploaded_file)
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
        st.error("Please upload a PDF file.")

with tabs[1]:
    st.header("Annotated Summary")

    # Check if Markdown content is available
    if 'markdown_content' in st.session_state:
        st.markdown("### Preview")
        st.markdown(st.session_state.markdown_content)
        st.download_button("Download Markdown", data=st.session_state.markdown_content, file_name='combined_output.md')
    else:
        st.info("Process a PDF first to see the summary.")
