from pathlib import Path
from crewai.tools import tool
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader

class ReadDataSchema(BaseModel):
    path: str = Field(description="The absolute LOCAL file path to the PDF.")

@tool("read_data_tool")
def read_data_tool(path: str) -> str:
    """Extracts text from a LOCAL PDF. The path must be a local string, not a URL."""
    # Clean the input
    clean_path = path.strip().replace('"', '').replace("'", "")
    
    if clean_path.startswith("http"):
        return "Error: This tool only reads local PDFs. Do not use URLs."

    normalized_path = Path(clean_path)
    
    if not normalized_path.exists():
        return f"Error: File not found at {normalized_path}"
    
    try:
        loader = PyPDFLoader(file_path=str(normalized_path))
        docs = loader.load()
        full_text = "\n".join(page.page_content for page in docs)
        return full_text[:8000] if full_text.strip() else "The document is empty."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

read_data_tool.args_schema = ReadDataSchema