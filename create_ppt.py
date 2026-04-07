from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Color Palette (Charcoal + Gold + Teal — Professional) ─────────────────────
BG_DARK    = RGBColor(0x14, 0x14, 0x14)   # near-black charcoal
BG_CARD    = RGBColor(0x22, 0x22, 0x22)   # dark card
BG_STRIPE  = RGBColor(0x1A, 0x1A, 0x1A)   # alt row
GOLD       = RGBColor(0xD4, 0xA0, 0x17)   # rich gold
TEAL       = RGBColor(0x1A, 0xBC, 0x9C)   # professional teal
RED        = RGBColor(0xE7, 0x4C, 0x3C)   # problem red
GREEN      = RGBColor(0x27, 0xAE, 0x60)   # solution green
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
MID_GRAY   = RGBColor(0x88, 0x88, 0x88)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def bg(slide, color=BG_DARK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def box(slide, l, t, w, h, color):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def txt(slide, text, l, t, w, h,
        size=18, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False):
    tf = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf.word_wrap = True
    p = tf.text_frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tf


def divider(slide, t):
    box(slide, 0.5, t, 12.33, 0.04, TEAL)


def section_tag(slide, label, l=0.5, t=0.22):
    box(slide, l, t, len(label) * 0.115 + 0.3, 0.33, TEAL)
    txt(slide, label, l + 0.08, t + 0.04, len(label) * 0.115 + 0.15, 0.28,
        size=11, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)


def bullet(slide, text, l, t, w=11, size=17, color=LIGHT_GRAY):
    txt(slide, "▸   " + text, l, t, w, 0.42, size=size, color=color)


def header_bar(slide):
    box(slide, 0, 0, 13.33, 0.1, GOLD)


def footer_bar(slide):
    box(slide, 0, 7.4, 13.33, 0.1, TEAL)
    txt(slide, "Fortune Teller  ·  AI Tarot Card Recognition  ·  2026",
        0, 7.4, 13.33, 0.1, size=9, color=MID_GRAY, align=PP_ALIGN.CENTER)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 1 — Title
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s1 = add_slide()
bg(s1)
header_bar(s1)
footer_bar(s1)

# Left gold accent strip
box(s1, 0, 0.1, 0.5, 7.3, GOLD)

# Center content area
box(s1, 2.8, 1.8, 8.0, 3.8, BG_CARD)
box(s1, 2.8, 1.8, 0.06, 3.8, TEAL)

txt(s1, "Fortune Teller", 3.0, 2.1, 7.6, 1.4,
    size=54, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

txt(s1, "AI-Powered Tarot Card Recognition", 3.0, 3.3, 7.6, 0.7,
    size=24, color=WHITE, align=PP_ALIGN.CENTER, italic=True)

box(s1, 3.5, 4.1, 6.5, 0.05, MID_GRAY)

txt(s1, "EfficientNet-B0   ·   PyTorch   ·   Transfer Learning", 3.0, 4.25, 7.6, 0.5,
    size=16, color=TEAL, align=PP_ALIGN.CENTER)

txt(s1, "Wannakorn Sangthongngam   ·   2026", 3.0, 4.85, 7.6, 0.45,
    size=14, color=MID_GRAY, align=PP_ALIGN.CENTER)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 2 — Introduction
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s2 = add_slide()
bg(s2)
header_bar(s2)
footer_bar(s2)

section_tag(s2, "INTRODUCTION")
txt(s2, "What is Fortune Teller?", 0.5, 0.65, 12.0, 0.75,
    size=34, bold=True, color=WHITE)
divider(s2, 1.52)

# Left box — Overview
box(s2, 0.5, 1.7, 5.8, 3.0, BG_CARD)
box(s2, 0.5, 1.7, 0.06, 3.0, GOLD)
txt(s2, "Overview", 0.72, 1.78, 5.3, 0.5, size=18, bold=True, color=GOLD)
bullet(s2, "Take a photo of a tarot card", 0.65, 2.32)
bullet(s2, "AI identifies which card it is", 0.65, 2.75)
bullet(s2, "Receive your fortune reading", 0.65, 3.18)
bullet(s2, "78 unique tarot cards supported", 0.65, 3.61)

# Right box — Tech Stack
box(s2, 6.9, 1.7, 5.9, 3.0, BG_CARD)
box(s2, 6.9, 1.7, 0.06, 3.0, TEAL)
txt(s2, "Tech Stack", 7.12, 1.78, 5.4, 0.5, size=18, bold=True, color=TEAL)
bullet(s2, "Framework: PyTorch", 7.05, 2.32)
bullet(s2, "Model: EfficientNet-B0", 7.05, 2.75)
bullet(s2, "Training: Google Colab (T4 GPU)", 7.05, 3.18)
bullet(s2, "Data: Custom tarot card photos", 7.05, 3.61)

# Flow diagram
steps = [("📷  Photo", TEAL), ("🤖  AI Model", TEAL), ("🃏  Card ID", TEAL), ("🔮  Fortune", GOLD)]
xs = [0.8, 3.9, 7.0, 10.1]
for i, ((label, color), x) in enumerate(zip(steps, xs)):
    box(s2, x, 5.1, 2.4, 0.72, color)
    txt(s2, label, x, 5.22, 2.4, 0.5, size=17, bold=True,
        color=BG_DARK if color == GOLD else WHITE, align=PP_ALIGN.CENTER)
    if i < 3:
        txt(s2, "→", x + 2.4, 5.26, 0.5, 0.45, size=22, bold=True, color=GOLD, align=PP_ALIGN.CENTER)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 3 — Problem & Solution
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s3 = add_slide()
bg(s3)
header_bar(s3)
footer_bar(s3)

section_tag(s3, "PROBLEM & SOLUTION")
txt(s3, "Challenge & Approach", 0.5, 0.65, 12.0, 0.75,
    size=34, bold=True, color=WHITE)
divider(s3, 1.52)

# Problem
box(s3, 0.5, 1.7, 5.8, 4.1, BG_CARD)
box(s3, 0.5, 1.7, 0.06, 4.1, RED)
txt(s3, "Problem", 0.72, 1.78, 5.3, 0.52, size=20, bold=True, color=RED)
for i, t in enumerate([
    "78 visually distinct tarot cards",
    "Complex symbols, figures, and colors",
    "Small dataset  (~30 photos per card)",
    "Varied lighting and shooting angles",
    "Training from scratch needs huge data",
]):
    bullet(s3, t, 0.65, 2.38 + i * 0.52, size=16)

# Solution
box(s3, 6.9, 1.7, 5.9, 4.1, BG_CARD)
box(s3, 6.9, 1.7, 0.06, 4.1, GREEN)
txt(s3, "Solution", 7.12, 1.78, 5.4, 0.52, size=20, bold=True, color=GREEN)
for i, t in enumerate([
    "Transfer learning from ImageNet",
    "EfficientNet-B0 as feature extractor",
    "Data augmentation (flip, rotate, jitter)",
    "2-phase training  (freeze → unfreeze)",
    "Good accuracy with small dataset",
]):
    bullet(s3, t, 7.05, 2.38 + i * 0.52, size=16)

box(s3, 0.5, 6.05, 12.33, 0.55, RGBColor(0x1E, 0x1E, 0x1E))
txt(s3, "Key Insight:  Borrow knowledge from 1.2M ImageNet images  →  apply to 78 tarot cards",
    0.6, 6.1, 12.1, 0.45, size=16, italic=True, color=GOLD, align=PP_ALIGN.CENTER)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 4 — Model Architecture
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s4 = add_slide()
bg(s4)
header_bar(s4)
footer_bar(s4)

section_tag(s4, "MODEL ARCHITECTURE")
txt(s4, "Model Architecture", 0.5, 0.65, 12.0, 0.75,
    size=34, bold=True, color=WHITE)
divider(s4, 1.52)

# Architecture blocks
arch_blocks = [
    ("Input\n224×224×3",              TEAL),
    ("EfficientNet-B0\nBackbone",     RGBColor(0x2C, 0x50, 0x6E)),
    ("Global Avg\nPooling  1280",     RGBColor(0x2C, 0x50, 0x6E)),
    ("Dropout\nLinear → 512\nReLU",   RGBColor(0x1E, 0x5C, 0x4A)),
    ("Dropout\nLinear → 78\nSoftmax", GOLD),
]

bw = 2.2
bh = 1.7
bx = 0.35
by = 1.9
for i, (label, color) in enumerate(arch_blocks):
    box(s4, bx, by, bw, bh, color)
    txt(s4, label, bx + 0.05, by + 0.35, bw - 0.1, bh - 0.4,
        size=14, bold=True,
        color=BG_DARK if color == GOLD else WHITE,
        align=PP_ALIGN.CENTER)
    if i < len(arch_blocks) - 1:
        txt(s4, "→", bx + bw, by + 0.55, 0.45, 0.6,
            size=22, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    bx += bw + 0.45

# Label below blocks
labels_below = ["Image Input", "Feature Extraction\n(ImageNet weights)", "Feature Vector", "Custom Head\n(Phase 1 frozen)", "78-Class Output"]
bx = 0.35
for label in labels_below:
    txt(s4, label, bx, by + bh + 0.1, bw, 0.55,
        size=11, color=MID_GRAY, align=PP_ALIGN.CENTER, italic=True)
    bx += bw + 0.45

# Properties table
headers = ["Property", "Value"]
rows = [
    ["Parameters",    "~5.3M"],
    ["Input Size",    "224 × 224 px"],
    ["Pretrained On", "ImageNet  (1.2M images)"],
    ["Output",        "78 classes  (tarot cards)"],
    ["Dropout Rate",  "0.3  (applied twice)"],
]

col_x = [0.5, 5.0]
col_w = [4.2, 7.5]
row_h = 0.4
ty = 4.35

box(s4, col_x[0], ty, col_w[0], row_h, TEAL)
box(s4, col_x[1], ty, col_w[1], row_h, TEAL)
txt(s4, "Property", col_x[0] + 0.1, ty + 0.07, col_w[0], row_h, size=14, bold=True, color=BG_DARK)
txt(s4, "Value",    col_x[1] + 0.1, ty + 0.07, col_w[1], row_h, size=14, bold=True, color=BG_DARK)

for ri, row in enumerate(rows):
    rc = BG_CARD if ri % 2 == 0 else BG_STRIPE
    for ci, cell in enumerate(row):
        box(s4, col_x[ci], ty + row_h * (ri + 1), col_w[ci], row_h, rc)
        txt(s4, cell, col_x[ci] + 0.12, ty + row_h * (ri + 1) + 0.07, col_w[ci], row_h,
            size=14, color=LIGHT_GRAY if ci == 0 else WHITE)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 5 — Training Pipeline
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s5 = add_slide()
bg(s5)
header_bar(s5)
footer_bar(s5)

section_tag(s5, "TRAINING PIPELINE")
txt(s5, "Training Pipeline", 0.5, 0.65, 12.0, 0.75,
    size=34, bold=True, color=WHITE)
divider(s5, 1.52)

cols = [
    ("Data Preparation", GOLD, [
        "78 card classes (tarot deck)",
        "~30 photos per card",
        "HEIC / JPG / PNG formats",
        "Split:  75% / 15% / 10%",
        "Stored in Google Drive",
    ]),
    ("Phase 1  —  10 Epochs", TEAL, [
        "Backbone layers frozen",
        "Train classifier head only",
        "Learning rate:  1e-3",
        "Optimizer:  Adam",
        "Scheduler:  CosineAnnealing",
    ]),
    ("Phase 2  —  20 Epochs", GREEN, [
        "All layers unfrozen",
        "Fine-tune full network",
        "Learning rate:  1e-4",
        "Weight decay:  1e-4",
        "Best model auto-saved",
    ]),
]

cx = 0.5
for title, color, items in cols:
    box(s5, cx, 1.7, 4.0, 4.6, BG_CARD)
    box(s5, cx, 1.7, 0.06, 4.6, color)
    txt(s5, title, cx + 0.2, 1.78, 3.7, 0.52, size=17, bold=True, color=color)
    box(s5, cx + 0.2, 2.35, 3.6, 0.04, RGBColor(0x33, 0x33, 0x33))
    for i, item in enumerate(items):
        bullet(s5, item, cx + 0.1, 2.48 + i * 0.52, w=3.7, size=15)
    cx += 4.44

# Augmentation note
box(s5, 0.5, 6.55, 12.33, 0.6, BG_CARD)
txt(s5, "Augmentation:   Resize  →  RandomCrop  →  Horizontal Flip  →  Rotate ±15°  →  ColorJitter  →  Normalize",
    0.7, 6.6, 11.9, 0.5, size=15, color=TEAL, align=PP_ALIGN.CENTER)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 6 — Roadmap
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s6 = add_slide()
bg(s6)
header_bar(s6)
footer_bar(s6)

section_tag(s6, "ROADMAP")
txt(s6, "Project Roadmap", 0.5, 0.65, 12.0, 0.75,
    size=34, bold=True, color=WHITE)
divider(s6, 1.52)

phases = [
    ("Phase 1", "Data Collection",
     "Photograph all 78 tarot cards  ·  ~30 photos each  ·  HEIC / JPG",
     GOLD, "In Progress"),
    ("Phase 2", "Model Training",
     "Fine-tune EfficientNet-B0 on Google Colab T4 GPU",
     TEAL, "Upcoming"),
    ("Phase 3", "Card Prediction",
     "Identify card from photo  ·  Return top-3 confidence scores",
     RGBColor(0x3B, 0x97, 0xD3), "Upcoming"),
    ("Phase 4", "Fortune Telling",
     "Map predicted card → meaning  ·  Generate fortune reading",
     GREEN, "Upcoming"),
    ("Phase 5", "Application",
     "Build full UI  ·  Camera capture  +  fortune display",
     RGBColor(0xE6, 0x7E, 0x22), "Upcoming"),
]

for i, (phase, title, desc, color, status) in enumerate(phases):
    y = 1.72 + i * 0.98

    # Phase badge
    box(s6, 0.5, y, 1.6, 0.75, color)
    txt(s6, phase, 0.5, y + 0.18, 1.6, 0.42, size=14, bold=True,
        color=BG_DARK if color == GOLD else WHITE, align=PP_ALIGN.CENTER)

    # Content row
    box(s6, 2.3, y, 10.5, 0.75, BG_CARD)
    txt(s6, title, 2.5, y + 0.04, 6.5, 0.38, size=17, bold=True, color=color)
    txt(s6, desc,  2.5, y + 0.42, 8.0, 0.35, size=13, color=LIGHT_GRAY)

    # Status badge
    status_color = GOLD if status == "In Progress" else MID_GRAY
    status_bg    = RGBColor(0x2A, 0x24, 0x10) if status == "In Progress" else BG_STRIPE
    box(s6, 10.5, y + 0.18, 2.1, 0.38, status_bg)
    txt(s6, ("🔄 " if status == "In Progress" else "⏳ ") + status,
        10.5, y + 0.2, 2.1, 0.35, size=13, bold=True,
        color=status_color, align=PP_ALIGN.CENTER)


out = "c:/Users/WannakornSangthongng/Desktop/Fortune Teller/Fortune_Teller_Presentation.pptx"
prs.save(out)
print(f"Saved: {out}")
