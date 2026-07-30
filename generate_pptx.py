from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
DARK_BLUE = RGBColor(0x1A, 0x3C, 0x6E)
ACCENT = RGBColor(0x00, 0xA8, 0xE8)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
GRAY = RGBColor(0x66, 0x66, 0x66)
GREEN = RGBColor(0x10, 0xB9, 0x81)
ORANGE = RGBColor(0xFF, 0x9F, 0x43)

def add_bg(slide, color=DARK_BLUE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, color, left=0, top=0, width=None, height=None):
    if width is None: width = prs.slide_width
    if height is None: height = prs.slide_height
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=BLACK, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=18, color=BLACK):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(8)
        p.level = 0
    return txBox

def add_accent_bar(slide, left, top, width, height, color=ACCENT):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

# ===== SLIDE 1: Title =====
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_bg(slide, DARK_BLUE)
add_text_box(slide, Inches(1), Inches(1.5), Inches(11), Inches(1.5),
             "Comptable-SLM", font_size=54, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_accent_bar(slide, Inches(5.5), Inches(3.2), Inches(2.3), Inches(0.06), ACCENT)
add_text_box(slide, Inches(1), Inches(3.5), Inches(11), Inches(1),
             "AI Assistant for Algerian Accounting & Audit", font_size=28, color=ACCENT, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(5), Inches(11), Inches(0.8),
             "Google Africa Applied AI Lab — Pitch", font_size=18, color=GRAY, alignment=PP_ALIGN.CENTER)

# ===== SLIDE 2: Problem =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "❌  The Problem", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), ACCENT)

add_bullet_list(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(5.5), [
    "🔴  AI tools are trained on US/European data — they hallucinate on African law",
    "🔴  Each African country has its own tax system, chart of accounts, regulations",
    "🔴  Algeria alone: SCF, 3 VAT rates (19%/9%/0%), CNAS, CASNOS, SARL/EURL/SPA...",
    "🔴  Accountants rely on scattered PDFs, outdated textbooks, expensive consultants",
    "",
    "🌍  Africa has 500,000+ accounting professionals — with zero AI tools built for them"
], font_size=20, color=BLACK)

# ===== SLIDE 3: Solution =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "✅  The Solution", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), GREEN)

add_bullet_list(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(5.5), [
    "🤖  Comptable-SLM: AI assistant trained specifically on African accounting",
    "",
    "📚  RAG Pipeline → instant retrieval from curated knowledge base (SCF law, tax codes, audit standards)",
    "🧠  Fine-tuned SLM → Llama 3.2 3B trained on 150+ real Algerian accounting scenarios",
    "📡  Works offline → deployable via Ollama, no internet required",
    "🎯  Always accurate → responses cite sources, distance threshold filters hallucinations",
    "",
    "⚡  \"AI should serve African professionals, not the other way around\""
], font_size=20, color=BLACK)

# ===== SLIDE 4: How it works =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "⚙️  How It Works", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), ACCENT)

# Flow boxes
box_y = Inches(2.2)
box_h = Inches(1.0)
arrow_x = Inches(4.6)
arrow_w = Inches(0.8)

for i, (label, desc, color) in enumerate([
    ("🔍  Question", "User asks about Algerian accounting", RGBColor(0x3B, 0x82, 0xF6)),
    ("📚  RAG Retrieval", "Search SCF law, tax codes\nin ChromaDB (534 chunks)", RGBColor(0x10, 0xB9, 0x81)),
    ("🧠  LLM + Context", "Llama 3.1 8B / 3.2 3B\nfine-tuned on Algeria", RGBColor(0xFF, 0x9F, 0x43)),
    ("✅  Answer", "Precise, sourced response\nin French / Arabic", RGBColor(0xEF, 0x44, 0x44)),
]):
    x = Inches(0.5 + i * 3.1)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, box_y, Inches(2.8), box_h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(18)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(12)
    p2.font.color.rgb = WHITE
    p2.font.name = "Calibri"
    p2.alignment = PP_ALIGN.CENTER

tech_items = [
    "🔧  Embeddings: NVIDIA Nemotron-3-Embed-1B (NIM API)",
    "🔧  Vector Store: ChromaDB (cosine distance, persistent)",
    "🔧  Fine-tuning: Unsloth + QLoRA (4-bit, 2x faster)",
    "🔧  Deployment: Cloud (NVIDIA NIM) or Local (Ollama GGUF)"
]
add_bullet_list(slide, Inches(0.8), Inches(3.8), Inches(11.5), Inches(3.5), tech_items, font_size=16, color=GRAY)

# ===== SLIDE 5: Technical Innovation =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "🚀  Technical Innovation", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), ORANGE)

# Table-like layout
cols = [("Component", Inches(0.5)), ("Technology", Inches(4.5)), ("Why it matters", Inches(8.5))]
row_h = Inches(0.65)
start_y = Inches(1.6)

items = [
    ("Embeddings", "NVIDIA Nemotron-3-Embed-1B", "State-of-the-art retrieval accuracy"),
    ("Vector Store", "ChromaDB (cosine, persistent)", "Fast, local, privacy-preserving"),
    ("Cloud LLM", "Llama 3.1 8B Instruct", "Handles complex multi-step reasoning"),
    ("Local SLM", "Llama 3.2 3B (4-bit fine-tuned)", "Works offline, no internet needed"),
    ("Fine-tuning", "Unsloth + QLoRA", "2x faster training, low VRAM (2-4 GB)"),
    ("Dataset", "150 Algerian examples (curated)", "Real scenarios, SCF-compliant"),
]

for i, (comp, tech, why) in enumerate(items):
    y = start_y + i * row_h
    bg_color = LIGHT_GRAY if i % 2 == 0 else WHITE
    add_shape_bg(slide, bg_color, left=Inches(0.3), top=y, width=Inches(12.7), height=row_h)
    add_text_box(slide, Inches(0.5), y + Inches(0.1), Inches(3.5), Inches(0.5), comp, font_size=16, color=DARK_BLUE, bold=True)
    add_text_box(slide, Inches(4.5), y + Inches(0.1), Inches(3.5), Inches(0.5), tech, font_size=16, color=BLACK)
    add_text_box(slide, Inches(8.5), y + Inches(0.1), Inches(4.5), Inches(0.5), why, font_size=16, color=GRAY)

# ===== SLIDE 6: Market =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "📊  Market Opportunity", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), GREEN)

add_bullet_list(slide, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.5), [
    "🇩🇿  Algeria",
    "    ~15,000 chartered accountants",
    "    50,000+ accounting professionals",
    "",
    "🌍  OHADA Zone (16 countries)",
    "    Benin, Burkina Faso, Cameroon,",
    "    Central African Republic, Chad,",
    "    Comoros, Congo, DR Congo,",
    "    Equatorial Guinea, Gabon,",
    "    Guinea, Guinea-Bissau,",
    "    Ivory Coast, Mali, Niger,",
    "    Senegal, Togo",
], font_size=18, color=BLACK)

add_bullet_list(slide, Inches(6.5), Inches(1.6), Inches(6), Inches(5.5), [
    "💰  Market Size",
    "",
    "TAM: 500,000+ accounting",
    "professionals across",
    "Francophone Africa",
    "",
    "📈  Growth drivers:",
    "    • Digital transformation",
    "    • Regulatory complexity",
    "    • Cloud adoption in Africa",
    "    • Mobile-first professionals",
    "",
    "🏆  Competition: None",
    "    (no AI tool built for",
    "    African accounting)",
], font_size=18, color=BLACK)

# ===== SLIDE 7: Traction & Roadmap =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "📈  Traction & Roadmap", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), ACCENT)

add_text_box(slide, Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.5),
             "✅  Completed", font_size=24, color=GREEN, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(2.1), Inches(5.5), Inches(2.5), [
    "RAG pipeline functional (534 chunks)",
    "SLM fine-tuned (loss: 1.89 → 0.03)",
    "Local inference via Ollama (GGUF ready)",
    "Knowledge base: SCF, tax, audit, social charges",
], font_size=16, color=BLACK)

add_text_box(slide, Inches(6.8), Inches(1.5), Inches(6), Inches(0.5),
             "🚀  Next 3 Months", font_size=24, color=ORANGE, bold=True)
add_bullet_list(slide, Inches(6.8), Inches(2.1), Inches(6), Inches(2.5), [
    "Expand dataset to 1,000+ examples",
    "Add OHADA support (16 countries)",
    "Web UI (Gradio/Streamlit)",
    "Beta test with 20 Algerian firms",
], font_size=16, color=BLACK)

add_text_box(slide, Inches(0.8), Inches(4.5), Inches(12), Inches(0.5),
             "🎯  Next 6 Months", font_size=24, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(5.1), Inches(12), Inches(2), [
    "Country modules: Morocco, Tunisia, Senegal, Ivory Coast",
    "Mobile app for on-the-go queries",
    "Integration with accounting software",
    "Pan-African rollout",
], font_size=16, color=BLACK)

# ===== SLIDE 8: Why Google =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_text_box(slide, Inches(1), Inches(0.8), Inches(11), Inches(1),
             "🎯  Why Google Africa Applied AI Lab?", font_size=36, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_accent_bar(slide, Inches(5), Inches(1.8), Inches(3.3), Inches(0.06), ACCENT)

add_bullet_list(slide, Inches(1.5), Inches(2.3), Inches(10), Inches(4.5), [
    "🔑  Early access to Gemini / Gemma — experiment with cutting-edge models",
    "🧠  Technical mentorship from Google Research — optimize RAG & fine-tuning",
    "🌍  Go-to-market support — reach 500,000+ African accounting professionals",
    "💰  VC network (4DX, Norrsken22, Novastar) — scale from Algeria to all of Africa",
    "🤝  Community of African founders — build the first generation of AI-native startups",
    "",
    "With Google's support, Comptable-SLM can become",
    "the standard AI tool for accounting across Africa."
], font_size=20, color=WHITE)

# ===== SLIDE 9: Team =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_shape_bg(slide, DARK_BLUE, left=Inches(0), top=Inches(0), width=Inches(13.333), height=Inches(1.2))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "👤  The Team", font_size=36, color=WHITE, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.1), Inches(2), Inches(0.05), ACCENT)

add_text_box(slide, Inches(1), Inches(1.8), Inches(11), Inches(5.5),
             "Expert-Comptable & Auditeur Légal  |  Développeur Amateur IA",
             font_size=28, color=DARK_BLUE, bold=True, alignment=PP_ALIGN.CENTER)

add_bullet_list(slide, Inches(1.5), Inches(2.8), Inches(10), Inches(4), [
    "✅  15+ years experience in Algerian accounting, audit & tax",
    "✅  Deep knowledge: SCF, IBS, IRG, TVA, CNAS, CASNOS",
    "✅  Built Comptable-SLM from scratch — RAG, fine-tuning, dataset",
    "✅  Self-taught AI developer — proof of passion & execution",
    "",
    "💡  \"I know the problem because I live it every day.\"",
    "💡  \"AI should serve African professionals, not the other way around.\""
], font_size=20, color=BLACK)

# ===== SLIDE 10: Demo =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_text_box(slide, Inches(1), Inches(0.8), Inches(11), Inches(1),
             "🎬  Live Demo", font_size=42, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_accent_bar(slide, Inches(5.5), Inches(1.8), Inches(2.3), Inches(0.06), ACCENT)

add_bullet_list(slide, Inches(1.5), Inches(2.5), Inches(10), Inches(4.5), [
    "1️⃣  \"What are the VAT rates in Algeria?\"",
    "      → RAG retrieves SCF law + tax code → precise answer with sources",
    "",
    "2️⃣  \"What's the difference between SARL and EURL?\"",
    "      → Fine-tuned model → accurate legal explanation in French",
    "",
    "3️⃣  \"How to record a purchase with 19% VAT?\"",
    "      → Accounting entry with correct accounts (401, 4456, 4457)",
    "",
    "4️⃣  Offline mode: same model runs on laptop, no internet needed"
], font_size=18, color=WHITE)

# ===== SLIDE 11: Thank You =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_text_box(slide, Inches(1), Inches(1.5), Inches(11), Inches(1.5),
             "Merci — Thank You", font_size=48, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_accent_bar(slide, Inches(5), Inches(3.2), Inches(3.3), Inches(0.06), ACCENT)
add_text_box(slide, Inches(1), Inches(3.8), Inches(11), Inches(1),
             "Let's build AI for Africa, together.", font_size=28, color=ACCENT, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(5.5), Inches(11), Inches(0.6),
             "Contact: [your email / LinkedIn]", font_size=18, color=GRAY, alignment=PP_ALIGN.CENTER)

prs.save("Comptable_SLM_Pitch.pptx")
print("Presentation saved: Comptable_SLM_Pitch.pptx")
