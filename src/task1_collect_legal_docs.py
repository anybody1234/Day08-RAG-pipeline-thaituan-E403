"""
Task 1 — Thu thập dữ liệu tiêu chí chấm điểm IELTS (Band Descriptors).

Chủ đề: Trợ Lý Tra Cứu Tiêu Chí Chấm Điểm IELTS & Essay Mẫu.

Nguồn dữ liệu:
    - IELTS Writing Band Descriptors (Official British Council/IDP)
    - Task 1 Writing Band Descriptors (Academic)
    - Task 2 Writing Band Descriptors
    - IELTS Speaking Band Descriptors

Hướng dẫn:
    1. Tạo tối thiểu 3 file PDF chứa tiêu chí chấm điểm IELTS.
    2. Dùng fpdf2 để generate PDF từ nội dung text (nguồn chính thống).
    3. Lưu vào data/landing/legal/
"""

import json
from pathlib import Path

from fpdf import FPDF

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Thư mục đã sẵn sàng: {DATA_DIR}")


# =============================================================================
# IELTS BAND DESCRIPTORS DATA
# Nguồn: British Council / IDP IELTS official public band descriptors
# =============================================================================

IELTS_WRITING_TASK2_BAND_DESCRIPTORS = """
IELTS Writing Task 2 - Band Descriptors (Public Version)
Source: British Council / IDP Australia (Official IELTS Partners)

========================================
CRITERION 1: TASK ACHIEVEMENT (Task Response)
========================================

Band 9:
- The prompt is appropriately addressed and explored in depth.
- A clear and fully developed position is presented which directly answers the question/s.
- Ideas are relevant, fully extended and well supported.
- Any lapses in content or support are extremely rare.

Band 8:
- The prompt is appropriately and sufficiently addressed.
- A clear and well-developed position is presented in response to the question/s.
- Ideas are relevant, well extended and supported.
- There may be occasional omissions or lapses in content.

Band 7:
- The main parts of the prompt are appropriately addressed.
- A clear and developed position is presented.
- Main ideas are extended and supported but there may be a tendency to over-generalise or there may be a lack of focus and precision in supporting ideas/material.

Band 6:
- The main parts of the prompt are addressed (though some may be more fully covered than others).
- A position is presented that is directly relevant to the prompt, although the conclusions drawn may be unclear, unjustified or repetitive.
- Main ideas are relevant but some may be insufficiently developed or may lack clarity, with some supporting arguments and evidence.

Band 5:
- The main parts of the prompt are incompletely addressed. The format may be inappropriate in places.
- A position is presented but the development is not always clear.
- Some main ideas are put forward, but they are limited and are not sufficiently developed. There may be irrelevant detail.

Band 4:
- The prompt is tackled in a minimal way, or the answer is tangential, possibly due to some misunderstanding of the prompt. The format may be inappropriate.
- A position is discernible, but the reader has to read carefully to find it.
- Main ideas are difficult to identify and such ideas that are identifiable may lack relevance, clarity and/or support.
- Large parts of the response may be repetitive.

========================================
CRITERION 2: COHERENCE AND COHESION
========================================

Band 9:
- The message can be followed effortlessly.
- Cohesion is used in such a way that it very rarely attracts attention.
- Any lapses in coherence or cohesion are minimal.
- Paragraphing is skilfully managed.

Band 8:
- The message can be followed with ease.
- Information and ideas are logically sequenced, and cohesion is well managed.
- Occasional lapses in coherence and cohesion may occur.
- Paragraphing is used sufficiently and appropriately.

Band 7:
- Information and ideas are logically organised, and there is a clear progression throughout the response. (A few lapses may occur, but these do not detract from the overall clarity.)
- A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some over/under use.
- Paragraphing is generally used effectively to support overall coherence.

Band 6:
- Information and ideas are generally arranged coherently and there is a clear overall progression.
- Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission.
- The use of reference and substitution may lack flexibility or clarity and result in some repetition or error.
- Paragraphing may not always be logical and/or the central topic within each paragraph may not always be clear.

Band 5:
- Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response.
- The relationship of ideas can be followed but the sentences are not fluently linked to each other.
- There may be limited/overuse of cohesive devices with some inaccuracy.
- The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution.
- Paragraphing may be inadequate or missing.

========================================
CRITERION 3: LEXICAL RESOURCE
========================================

Band 9:
- Full flexibility and precise use are widely evident.
- A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features.
- Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.

Band 8:
- A wide resource is fluently and flexibly used to convey precise meanings.
- There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation.
- Occasional errors in spelling and/or word formation may occur but have minimal impact on communication.

Band 7:
- The resource is sufficient to allow some flexibility and precision.
- There is some ability to use less common and/or idiomatic items.
- An awareness of style and collocation is evident, though inappropriacies occur.
- There are only a few errors in spelling and/or word formation and they do not detract from overall clarity.

Band 6:
- The resource is generally adequate and appropriate for the task.
- The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice.
- If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy.
- There are some errors in spelling and/or word formation, but these do not impede communication.

Band 5:
- The resource is limited but minimally adequate for the task.
- Simple vocabulary may be used accurately but the range does not permit much variation in expression.
- There may be frequent lapses in the appropriacy of word choice and a lack of flexibility is apparent in frequent simplifications and/or repetitions.
- Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.

========================================
CRITERION 4: GRAMMATICAL RANGE AND ACCURACY
========================================

Band 9:
- A wide range of structures is used with full flexibility and control.
- Punctuation and grammar are used appropriately throughout.
- Minor errors are extremely rare and have minimal impact on communication.

Band 8:
- A wide range of structures is flexibly and accurately used.
- The majority of sentences are error-free, and punctuation is well managed.
- Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication.

Band 7:
- A variety of complex structures is used with some flexibility and accuracy.
- Grammar and punctuation are generally well controlled, and error-free sentences are frequent.
- A few errors in grammar may persist, but these do not impede communication.

Band 6:
- A mix of simple and complex sentence forms is used but flexibility is limited.
- Examples of more complex structures are not rare, but these tend to be less accurate than simple structures.
- Errors in grammar and punctuation occur, but rarely impede communication.

Band 5:
- The range of structures is limited and rather repetitive.
- Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences.
- Grammatical errors may be frequent and cause some difficulty for the reader.
- Punctuation may be faulty.
"""

IELTS_WRITING_TASK1_BAND_DESCRIPTORS = """
IELTS Writing Task 1 (Academic) - Band Descriptors (Public Version)
Source: British Council / IDP Australia (Official IELTS Partners)

========================================
CRITERION 1: TASK ACHIEVEMENT
========================================

Band 9:
- All the requirements of the task are fully and appropriately satisfied.
- There is a clear overview of main trends, differences or stages.
- Key features are clearly selected, and clearly and appropriately described, highlighted and illustrated.
- There may be occasional omission of detail to the detriment of the overall message.

Band 8:
- The response covers all the requirements of the task appropriately, relevantly and sufficiently.
- There is a clear overview of main trends, differences or stages.
- Key features are skilfully selected, and clearly presented, highlighted and illustrated.

Band 7:
- The response covers the requirements of the task.
- There is a clear overview of main trends, differences or stages.
- Key features are clearly presented, highlighted and illustrated but could be more fully extended.

Band 6:
- The response focuses on the requirements of the task and an appropriate format is used.
- Key features which are selected are not adequately covered. The recounting of detail is mainly mechanical.
- There may be no data to support the description.
- An overview is presented, but the information is not appropriately selected to adequately overview the main trends, differences or stages.

Band 5:
- The response generally addresses the requirements of the task. The format may be inappropriate in places.
- Key features which are selected are not adequately covered. The recounting of detail is mainly mechanical. There may be no data to support the description.
- There may be a tendency to focus on details (e.g., facts and figures used for support) without referring to the main message of the data/diagram.
- The inclusion of irrelevant, inappropriate or inaccurate detail may detract from the main message.

========================================
CRITERION 2: COHERENCE AND COHESION
========================================

Band 9:
- The message can be followed effortlessly.
- Cohesion is used in such a way that it very rarely attracts attention.
- Any lapses in coherence or cohesion are minimal.
- Paragraphing is skilfully managed.

Band 8:
- The message can be followed with ease.
- Information and ideas are logically sequenced, and cohesion is well managed.
- Occasional lapses in coherence or cohesion may occur.
- Paragraphing is used sufficiently and appropriately.

Band 7:
- Information and ideas are logically organised, and there is a clear progression throughout the response.
- A range of cohesive devices is used flexibly but with some inaccuracies or some over/under use.

Band 6:
- Information and ideas are generally arranged coherently, and there is a clear overall progression.
- Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical.
- The use of reference and substitution may lack flexibility or clarity and result in some repetition or error.

Band 5:
- Organisation is evident but is not wholly logical and there may be a lack of overall progression.
- The relationship of ideas can be followed but the sentences are not fluently linked to each other.
- There may be limited/overuse of cohesive devices.

========================================
CRITERION 3: LEXICAL RESOURCE
========================================

Band 9:
- Full flexibility and precise use are widely evident.
- A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features.

Band 8:
- A wide resource is fluently and flexibly used to convey precise meanings.
- There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation.

Band 7:
- The resource is sufficient to allow some flexibility and precision.
- There is some ability to use less common and/or idiomatic items.
- An awareness of style and collocation is evident, though inappropriacies occur.

Band 6:
- The resource is generally adequate and appropriate for the task.
- The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice.

Band 5:
- The resource is limited but minimally adequate for the task.
- Simple vocabulary may be used accurately but the range does not permit much variation in expression.

========================================
CRITERION 4: GRAMMATICAL RANGE AND ACCURACY
========================================

Band 9:
- A wide range of structures is used with full flexibility and control.
- Punctuation and grammar are used appropriately throughout.

Band 8:
- A wide range of structures is flexibly and accurately used.
- The majority of sentences are error-free, and punctuation is well managed.

Band 7:
- A variety of complex structures is used with some flexibility and accuracy.
- Grammar and punctuation are generally well controlled, and error-free sentences are frequent.

Band 6:
- A mix of simple and complex sentence forms is used but flexibility is limited.
- Examples of more complex structures are not rare, but these tend to be less accurate than simple structures.

Band 5:
- The range of structures is limited and rather repetitive.
- Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences.
"""

IELTS_SPEAKING_BAND_DESCRIPTORS = """
IELTS Speaking - Band Descriptors (Public Version)
Source: British Council / IDP Australia (Official IELTS Partners)

========================================
CRITERION 1: FLUENCY AND COHERENCE
========================================

Band 9:
- Speaks fluently with only rare repetition or self-correction.
- Any hesitation is content-related rather than to find words or grammar.
- Speaks coherently with fully appropriate cohesive features.
- Develops topics fully and appropriately.

Band 8:
- Speaks fluently with only occasional repetition or self-correction; hesitation is usually content-related and only rarely to search for language.
- Develops topics coherently and appropriately.

Band 7:
- Speaks at length without noticeable effort or loss of coherence.
- May demonstrate language-related hesitation at times, or some repetition and/or self-correction.
- Uses a range of connectives and discourse markers with some flexibility.

Band 6:
- Is willing to speak at length, though may lose coherence at times due to occasional repetition, self-correction or hesitation.
- Uses a range of connectives and discourse markers but not always appropriately.

========================================
CRITERION 2: LEXICAL RESOURCE
========================================

Band 9:
- Uses vocabulary with full flexibility and precision in all topics.
- Uses idiomatic language naturally and accurately.

Band 8:
- Uses a wide vocabulary resource readily and flexibly to convey precise meaning.
- Uses less common and idiomatic vocabulary skilfully, with occasional inaccuracies.
- Uses paraphrase effectively as required.

Band 7:
- Uses vocabulary resource flexibly to discuss a variety of topics.
- Uses some less common and idiomatic vocabulary and shows some awareness of style and collocation, with some inappropriate choices.
- Uses paraphrase effectively.

Band 6:
- Has a wide enough vocabulary to discuss topics at length and make meaning clear in spite of inappropriacies.
- Generally paraphrases successfully.

========================================
CRITERION 3: GRAMMATICAL RANGE AND ACCURACY
========================================

Band 9:
- Uses a full range of structures naturally and appropriately.
- Produces consistently accurate structures apart from 'slips' characteristic of native speaker speech.

Band 8:
- Uses a wide range of structures flexibly.
- Produces a majority of error-free sentences with only very occasional inappropriacies or basic/non-systematic errors.

Band 7:
- Uses a range of complex structures with some flexibility.
- Frequently produces error-free sentences, though some grammatical mistakes persist.

Band 6:
- Uses a mix of simple and complex structures, but with limited flexibility.
- May make frequent mistakes with complex structures, though these rarely cause comprehension problems.

========================================
CRITERION 4: PRONUNCIATION
========================================

Band 9:
- Uses a full range of pronunciation features with precision and subtlety.
- Sustains flexible use of features throughout.
- Is effortless to understand.

Band 8:
- Uses a wide range of pronunciation features.
- Sustains flexible use of features, with only occasional lapses.
- Is easy to understand throughout; L1 accent has minimal effect on intelligibility.

Band 7:
- Shows all the positive features of Band 6 and some, but not all, of the positive features of Band 8.

Band 6:
- Uses a range of pronunciation features with mixed control.
- Shows some effective use of features but this is not sustained.
- Can generally be understood throughout, though mispronunciation of individual words or sounds reduces clarity at times.
"""


def create_pdf(content: str, filepath: Path, title: str):
    """Tạo PDF từ nội dung text sử dụng fpdf2."""
    from fpdf.enums import XPos, YPos

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.add_page()

    def sanitize(text: str) -> str:
        """Replace special chars that Helvetica can't render."""
        return (text
                .replace("\u2014", "--")   # em dash
                .replace("\u2013", "-")    # en dash
                .replace("\u2018", "'")    # left single quote
                .replace("\u2019", "'")    # right single quote
                .replace("\u201c", '"')    # left double quote
                .replace("\u201d", '"')    # right double quote
                .replace("\u2026", "...")  # ellipsis
                .replace("\u2022", "-")    # bullet
                .replace("\u2713", "[v]")  # checkmark
                .encode("latin-1", errors="replace").decode("latin-1"))

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, sanitize(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(3)

    # Body content
    pdf.set_font("Helvetica", "", 9)
    effective_w = pdf.w - pdf.l_margin - pdf.r_margin  # explicit width

    for line in content.split("\n"):
        line = sanitize(line.strip())
        if not line:
            pdf.ln(2)
            continue
        if line.startswith("========"):
            pdf.ln(2)
            continue

        try:
            if line.startswith("CRITERION") or line.startswith("Band "):
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(w=effective_w, h=5, text=line)
                pdf.set_font("Helvetica", "", 9)
            elif line.startswith("- "):
                pdf.set_x(pdf.l_margin + 5)
                pdf.multi_cell(w=effective_w - 5, h=4, text=line)
            else:
                pdf.multi_cell(w=effective_w, h=4, text=line)
        except Exception:
            # Skip problematic lines
            pdf.ln(2)

    pdf.output(str(filepath))
    print(f"  [OK] Created PDF: {filepath.name} ({filepath.stat().st_size} bytes)")


def collect_legal_docs():
    """Tạo 3+ file PDF chứa IELTS Band Descriptors."""
    setup_directory()

    print("=" * 50)
    print("Task 1: Thu thập Band Descriptors (IELTS)")
    print("=" * 50)

    docs = [
        {
            "content": IELTS_WRITING_TASK2_BAND_DESCRIPTORS,
            "filename": "ielts-writing-task2-band-descriptors.pdf",
            "title": "IELTS Writing Task 2 Band Descriptors",
        },
        {
            "content": IELTS_WRITING_TASK1_BAND_DESCRIPTORS,
            "filename": "ielts-writing-task1-band-descriptors.pdf",
            "title": "IELTS Writing Task 1 Band Descriptors",
        },
        {
            "content": IELTS_SPEAKING_BAND_DESCRIPTORS,
            "filename": "ielts-speaking-band-descriptors.pdf",
            "title": "IELTS Speaking Band Descriptors",
        },
    ]

    for doc in docs:
        filepath = DATA_DIR / doc["filename"]
        create_pdf(doc["content"], filepath, doc["title"])

    print(f"\n✓ Tổng cộng {len(docs)} file PDF đã tạo trong {DATA_DIR}")


if __name__ == "__main__":
    collect_legal_docs()
