#------------------------------------------
# Step B : Setup read paper(PDF) online tool
#------------------------------------------

from langchain_core.tools import tool
import io
import requests
import PyPDF2


@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL.

    Args:
        url: The URL of the PDF file to read

    Returns:
        The extracted text content from the PDF
    """

    try:
        # Important: add timeout so agent doesn't hang
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return f"Could not access paper at {url}. Status code: {response.status_code}"

        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        num_pages = len(pdf_reader.pages)
        text = ""

        for i, page in enumerate(pdf_reader.pages, 1):
            print(f"Extracting text from page {i}/{num_pages}")

            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if not text.strip():
            return f"Paper at {url} could be opened but no readable text was found."

        print(f"Successfully extracted {len(text)} characters of text from PDF")
        return text.strip()

    except requests.exceptions.RequestException as e:
        # NETWORK FAILURE — DO NOT CRASH AGENT
        print(f"Network error reading PDF: {str(e)}")
        return f"Failed to download paper at {url} due to network error. Continue with other papers."

    except Exception as e:
        # PDF PARSE FAILURE — DO NOT CRASH AGENT
        print(f"PDF parsing error: {str(e)}")
        return f"Could not read the PDF content at {url}. Continue research using other sources."


# #------------------------------------------
# #Step B : Setup read paper(PDF) online tool
# #------------------------------------------


# from langchain_core.tools import tool
# import io
# import requests
# import PyPDF2


# @tool
# def read_pdf(url: str) -> str:
#     """Read and extract text from a PDF file given its URL.

#     Args:
#         url: The URL of the PDF file to read

#     Returns:
#         The extracted text content from the PDF
#     """
#     try:
#         response = requests.get(url)                #Step 1 : Access and read PDF from URL
#         pdf_file = io.BytesIO(response.content)     #Step 2 : convert to bytes
#         pdf_reader = PyPDF2.PdfReader(pdf_file)     # Step 3 : Retrieve text from PDF
#         num_pages = len(pdf_reader.pages)
#         text = ""
#         for i, page in enumerate(pdf_reader.pages, 1):
#             print(f"Extracting text from page {i}/{num_pages}")
#             text += page.extract_text() + "\n"

#         print(f"Successfully extracted {len(text)} characters of text from PDF")
#         return text.strip()
#     except Exception as e:
#         print(f"Error reading PDF: {str(e)}")
#         raise
