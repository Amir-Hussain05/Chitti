import logging
import re
from pathlib import Path
from skills.base import BaseSkill

logger = logging.getLogger(__name__)

class PDFSummarizerSkill(BaseSkill):

    @property
    def name(self) -> str:
        return "pdf_summarizer"

    @property
    def triggers(self) -> list[str]:
        return ["summarize", "pdf", "read pdf", "pdf summary",
                "document", "file summarize", "pdf parho"]

    def execute(self, text: str) -> str:
        try:
            from pypdf import PdfReader
        except ImportError:
            return "pypdf library nahi mili. 'pip install pypdf' run karo."

        pdf_path = self._extract_path(text)

        if not pdf_path:
            return (
                "Amir, PDF ka path batao. Example:\n"
                "summarize C:\\Users\\Amir\\Desktop\\notes.pdf"
            )

        path = Path(pdf_path)
        if not path.exists():
            return f"Yeh file nahi mili: {pdf_path}"

        if path.suffix.lower() != ".pdf":
            return "Sirf PDF files support hain abhi."

        try:
            reader = PdfReader(str(path))
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() or ""

            if not text_content.strip():
                return "PDF mein koi readable text nahi mila."

            preview = text_content[:3000]
            logger.info("PDF read: %s (%d pages)", path.name, len(reader.pages))
            return self._summarize(preview, path.name)

        except Exception as e:
            logger.error("PDF error: %s", e)
            return f"PDF padhne mein masla aaya: {e}"

    def _extract_path(self, text: str) -> str | None:
        quoted = re.findall(r'"([^"]+\.pdf)"', text, re.IGNORECASE)
        if quoted:
            return quoted[0]

        match = re.search(r'([A-Za-z]:\\[^\s]+\.pdf)', text, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    def _summarize(self, content: str, filename: str) -> str:
        from llm.groq_client import GroqClient

        llm = GroqClient()
        messages = [
            {
                "role": "system",
                "content": "You are ABIS. Summarize the given document content clearly and concisely in the same language the document is in. Use bullet points."
            },
            {
                "role": "user",
                "content": f"Summarize this document '{filename}':\n\n{content}"
            }
        ]
        response = llm.chat(messages)
        return f"📄 Summary of '{filename}':\n\n{response}"