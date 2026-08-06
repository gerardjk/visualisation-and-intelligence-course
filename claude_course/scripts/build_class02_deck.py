"""Build the Class 2 deck: Choosing Visual Forms — Encoding, Tidy Data, and the Visual Vocabulary."""

from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches

from deck_common import (
    Deck, FIGURES, ROOT, add_bullets, add_picture_contain, add_rect, add_text,
    BLUE, CORAL, CYAN, INK, MUTED, NAVY, PALE, WHITE,
)

OUTPUT = ROOT / "claude_course" / "classes" / "02-visual-forms" / "Choosing-Visual-Forms.pptx"


def build():
    deck = Deck("CLASS 2 · CHOOSING VISUAL FORMS", "Choosing Visual Forms")

    # 1 — title
    deck.title_slide(
        "36104 · CLASS 2",
        "Choosing Visual Forms",
        "Encoding, tidy data,\nand the Visual Vocabulary",
        "What visual task are we performing?",
        "Data Visualisation and Narratives",
    )

    # 2 — premise
    deck.statement(
        "The premise",
        "Good chart choice begins with the analytical task, not with the visual effect.",
        "Opening question: before you pick a chart—what comparison must the reader actually make?",
    )

    # 3 — outcomes
    slide = deck.content("By the end of today")
    add_bullets(slide, [
        "Rank visual channels by the precision with which people read them.",
        "Classify an analytical question into an FT Visual Vocabulary category.",
        "Map a visual task to candidate chart forms—and name what each could mislead.",
        "Reshape wide data to tidy long form, by hand and with an AI assistant.",
        "Verify AI-wrangled data: identifiers, row counts, types, missing values.",
    ], Inches(0.85), Inches(1.75), Inches(11.4), Inches(4.7), size=25)

    # 4 — channels ranked (Bertin recap → precision)
    slide = deck.content("Channels are read at different precision",
                         "After Cleveland & McGill (1984)")
    ranks = [
        ("1", "Position on a common scale", "the workhorse — dot plots, scatterplots"),
        ("2", "Position on unaligned scales", "small multiples pay a small tax"),
        ("3", "Length", "bars — but only from a zero baseline"),
        ("4", "Angle · slope", "pie charts and line slopes blur"),
        ("5", "Area", "bubbles compress differences"),
        ("6", "Colour value · saturation", "ordered, but coarse"),
        ("7", "Colour hue", "categories only — never magnitude"),
    ]
    for i, (num, label, detail) in enumerate(ranks):
        y = Inches(1.58 + i * 0.72)
        add_rect(slide, Inches(0.85), y, Inches(0.5), Inches(0.5), CORAL, radius=True)
        add_text(slide, num, Inches(0.85), y + Inches(0.01), Inches(0.5), Inches(0.42),
                 size=15, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
                 valign=MSO_ANCHOR.MIDDLE)
        add_text(slide, label, Inches(1.62), y - Inches(0.02), Inches(4.9), Inches(0.5),
                 size=19, color=NAVY, bold=True)
        add_text(slide, detail, Inches(6.7), y - Inches(0.02), Inches(6.0), Inches(0.5),
                 size=17, color=MUTED)

    # 5 — area channel bias (Mohs)
    deck.figure_slide(
        "When the channel fights the data",
        "fig-mohs-output-1.png",
        "Rank ≠ magnitude",
        ["Mohs hardness is an ordinal ladder. Encoded as evenly spaced bars it looks "
         "linear—but real hardness explodes near the top.",
         "The channel you choose asserts a scale. Choose one the data can honour."],
        source="Mohs (1825) · reproduction generated from code",
    )

    # 6 — FT Visual Vocabulary premise
    deck.statement(
        "The shared language",
        "Nine families of visual task. Every chart in this course belongs to one.",
        "Deviation · Correlation · Ranking · Distribution · Change over time · Magnitude · Part-to-whole · Spatial · Flow",
    )

    # 7 — vocabulary grid
    deck.cards_slide("The FT Visual Vocabulary", [
        ("DEVIATION", "Values differ from a baseline or target"),
        ("CORRELATION", "Variables move together or apart"),
        ("RANKING", "Ordering items by value"),
        ("DISTRIBUTION", "Spread, range, clusters, outliers"),
        ("CHANGE OVER TIME", "Temporal pattern and trend"),
        ("MAGNITUDE", "Comparing sizes"),
        ("PART-TO-WHOLE", "Composition of a total"),
        ("SPATIAL", "Location and geography"),
        ("FLOW", "Movement, transfer, connection"),
    ], columns=2)

    # 8 — task-to-chart gallery: distribution
    deck.figure_slide(
        "Distribution: show the spread, not the summary",
        "fig-boxplot-output-1.png",
        "The box plot",
        ["Median, quartiles, whiskers, outliers — five numbers standing in for the "
         "whole spread.",
         "Alternatives: histogram, dot plot, violin, density. Each reveals what the "
         "box compresses."],
        source="Tukey (1977) · reproduction generated from code",
    )

    # 9 — change over time
    deck.figure_slide(
        "Change over time: the line over time is an argument",
        "fig-keeling-output-1.png",
        "The Keeling curve",
        ["A rising saw-tooth: seasonal breathing on a relentless trend.",
         "The aspect ratio, the baseline and the window all change what the reader "
         "concludes."],
        source="Keeling (1960– ) · reproduction generated from code",
    )

    # 10 — correlation
    deck.figure_slide(
        "Correlation: two variables, one claim",
        "fig-hr-output-1.png",
        "Hertzsprung–Russell",
        ["A scatterplot of star brightness against temperature revealed the "
         "structure of stellar evolution.",
         "Position on both axes — the highest-precision channels doing the work."],
        source="Hertzsprung & Russell (1910s) · reproduction generated from code",
    )

    # 11 — spatial + flow
    deck.figure_slide(
        "Spatial and flow: geography and movement carry the claim",
        "fig-minard-output-2.png" if (FIGURES / "fig-minard-output-2.png").exists()
        else "fig-minard-output-1.png",
        "Minard’s march",
        ["Position, band width, colour and temperature in one plane — a flow map "
         "carrying an argument about catastrophe.",
         "Spatial and flow forms are powerful and expensive: use them when location "
         "or movement is the task."],
        source="Minard (1869) · reproduction generated from code",
    )

    # 12 — colour
    deck.figure_slide(
        "Colour is an encoding, not a decoration",
        "fig-climatestripes-output-1.png",
        "Climate stripes",
        ["One channel — colour — encoding one variable, ordered and diverging "
         "around a baseline.",
         "Colour rules: sequential for ordered data, diverging around a meaningful "
         "midpoint, categorical hues only for categories. Check colour-blind safety."],
        source="Hawkins (2018) · reproduction generated from code",
    )

    # 12b — colour rules
    deck.cards_slide("Colour rules, in six cards", [
        ("SEQUENTIAL", "Ordered data: light → dark, one hue"),
        ("DIVERGING", "Two directions around a meaningful midpoint"),
        ("CATEGORICAL", "Distinct hues for categories — never magnitude"),
        ("COLOUR-BLIND", "≈8% of men can't split red/green — check every palette"),
        ("RAINBOW", "Jet invents boundaries that aren't in the data"),
        ("GREY IS A COLOUR", "Mute the context, spend hue on the point"),
    ])

    # 12c — ranking + scale (Zipf)
    deck.figure_slide(
        "Ranking meets the scale question",
        "fig-zipf-output-1.png",
        "Zipf’s law of cities",
        ["Rank cities by size and plot on log–log: a straight line appears — "
         "structure the linear view hides completely.",
         "The task (ranking) chose the form; the data chose the scale."],
        source="Zipf (1949) · reproduction generated from code",
    )

    # 12d — distribution split by category
    deck.figure_slide(
        "Distribution split by category",
        "fig-population-pyramid-output-1.png",
        "The population pyramid",
        ["Back-to-back bars: one distribution per group, mirrored so the shape "
         "of a whole population reads at a glance.",
         "Youthful and broad, or ageing and top-heavy — the silhouette is the "
         "finding."],
        source="Walker (1874) · reproduction generated from code",
    )

    # 12e — flow
    deck.figure_slide(
        "Flow: where the quantity goes",
        "fig-sankey-output-2.png",
        "The Sankey diagram",
        ["Band width is the quantity; the branching shows where it goes. "
         "Energy in, useful work and losses out.",
         "Use flow forms when the reader's task is tracing movement — not "
         "just comparing totals."],
        source="Sankey (1898) · reproduction generated from code",
    )

    # 12f — spatial caveat
    deck.figure_slide(
        "Spatial: the map is the task — and the trap",
        "fig-choropleth-output-1.png",
        "Choropleth vs cartogram",
        ["Colour by area and big empty regions dominate; size by population "
         "and geography distorts. Every map trades truth for truth.",
         "Ask: is location genuinely the task, or is a sorted bar chart the "
         "honest answer?"],
        source="Reproduction generated from code",
    )

    # 12g — baselines, aspect, order
    deck.cards_slide("Baselines, aspect, and order", [
        ("ZERO BASELINE", "Bars encode length — they must start at zero"),
        ("LINES MAY ZOOM", "Position encodings can crop — say so on the axis"),
        ("ASPECT RATIO", "Bank slopes toward 45° to keep change readable"),
        ("SORT ORDER", "Alphabetical is a decision too — usually the wrong one"),
        ("DUAL AXES", "Two scales invite any story — small multiples instead"),
        ("ANNOTATE", "Title the finding; label the point that carries it"),
    ])

    # 12h — think-pair-share
    deck.statement(
        "Think · pair · share",
        "Sketch: monthly ridership for six regions, 2019–2025. Which form — and which channel does the work?",
        "3 minutes solo sketch · 4 minutes compare in pairs · as a room: what did everyone choose, and what did nobody choose?",
    )

    # 13 — tidy data
    slide = deck.content("Tidy data: the shape charts want", "Wickham, “Tidy Data” (2014)")
    rules = [
        ("COLUMN", "each variable is a column"),
        ("ROW", "each observation is a row"),
        ("CELL", "each value is a cell"),
    ]
    for i, (label, detail) in enumerate(rules):
        x = Inches(0.75 + i * 4.15)
        add_rect(slide, x, Inches(1.7), Inches(3.75), Inches(1.35), WHITE, line=PALE,
                 radius=True)
        add_text(slide, label, x + Inches(0.25), Inches(1.95), Inches(3.2), Inches(0.3),
                 size=13, color=CORAL, bold=True)
        add_text(slide, detail, x + Inches(0.25), Inches(2.32), Inches(3.25), Inches(0.6),
                 size=20, color=NAVY, bold=True)
    add_text(slide, "Wide → long is the reshape you will perform most often:",
             Inches(0.85), Inches(3.45), Inches(11), Inches(0.4), size=20, color=INK)
    add_rect(slide, Inches(0.85), Inches(4.0), Inches(11.6), Inches(2.25), WHITE,
             line=PALE, radius=True)
    add_text(slide,
             "region      2023    2024    2025            region   year   riders\n"
             "Inner       1.30M   1.41M   1.52M    →      Inner    2023   1.30M\n"
             "Western     1.05M   1.13M   1.24M           Inner    2024   1.41M\n"
             "                                            Western  2023   1.05M",
             Inches(1.15), Inches(4.25), Inches(11.0), Inches(1.8),
             size=16, color=INK, font="Consolas")
    add_text(slide, "Tidy structure feeds Tableau, pandas, Altair — and AI-generated code.",
             Inches(0.85), Inches(6.45), Inches(11.4), Inches(0.4), size=18, color=MUTED)

    # 14 — AI wrangling verification
    slide = deck.content("AI-assisted wrangling: generate, then verify")
    steps = [
        ("1", "IDENTIFIERS", "Are the key columns intact — no invented or dropped categories?"),
        ("2", "ROW COUNT", "Does the reshaped row count equal what arithmetic predicts?"),
        ("3", "TYPES", "Numbers still numeric, dates still dates — no silent strings?"),
        ("4", "MISSING", "Where did NaNs appear, and are they real or created?"),
        ("5", "SPOT TOTALS", "Does one hand-computed total match the transformed table?"),
    ]
    for i, (num, label, detail) in enumerate(steps):
        y = Inches(1.62 + i * 0.98)
        add_rect(slide, Inches(0.85), y, Inches(0.55), Inches(0.55), CORAL, radius=True)
        add_text(slide, num, Inches(0.85), y + Inches(0.02), Inches(0.55), Inches(0.45),
                 size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
                 valign=MSO_ANCHOR.MIDDLE)
        add_text(slide, label, Inches(1.7), y, Inches(2.0), Inches(0.35),
                 size=15, color=BLUE, bold=True)
        add_text(slide, detail, Inches(3.6), y - Inches(0.03), Inches(8.5), Inches(0.52),
                 size=20, color=INK)

    # 15 — notebook segment
    slide = deck.content("Notebook: classify, reshape, redesign")
    add_bullets(slide, [
        "Open visual_forms_activities.ipynb in VS Code with your AI assistant on.",
        "Exercise 1 — channel precision: judge the same values in five encodings.",
        "Exercise 2 — reshape the wide transport table to tidy long form; run the five checks.",
        "Exercise 3 — classify six analytical questions into Vocabulary categories and draft one chart.",
        "Exercise 4 — aspect ratio and baseline: same data, three impressions.",
        "Exercise 5 — colour: pick the palette family for three datasets, then prove it.",
        "Exercise 6 — redesign the weak chart three ways, one category per redesign.",
    ], Inches(0.85), Inches(1.75), Inches(11.4), Inches(4.9), size=22)

    # 15b — break
    deck.statement("Break", "Back in 10 minutes.",
                   "When we return: the redesign studio — bring your weak-chart diagnosis.")

    # 16 — common mistake
    deck.statement(
        "The common mistake",
        "Choosing the most impressive form instead of the form the task needs.",
        "Does the visual form fit the task—or does it encourage an easier but wrong interpretation?",
    )

    # 17 — studio
    deck.studio_slide(
        "STUDIO · 45 MINUTES", "Redesign ×3",
        "Take the weak chart. Redesign it three ways — each serving a different Visual Vocabulary category.",
        [("10 min", "Diagnose", "Name the task the original fails."),
         ("15 min", "Redesign", "Three sketches, three categories."),
         ("10 min", "Classify", "Justify each category and form choice."),
         ("10 min", "Share", "Trade one redesign; name one risk.")],
    )

    # 18 — session map
    deck.hours_slide("Today’s three-hour rhythm", [
        ("HOUR 1", "Channels and the Vocabulary", "Precision · nine families · colour · baselines"),
        ("HOUR 2", "Tidy data and AI wrangling", "Notebook: reshape, verify, classify, colour"),
        ("HOUR 3", "Redesign studio", "Weak chart ×3 redesigns · critique · quiz"),
    ])

    # 19 — quiz
    deck.statement(
        "Quiz",
        "15 minutes. Open book, closed assistant.",
        "Today's vocabulary: channels and their precision, the nine task families, tidy data, the five wrangling checks.",
    )

    # 20 — close
    deck.statement(
        "Exit question",
        "Does the selected visual form fit the task, or does it encourage an easier but wrong interpretation?",
        "Bring one chart you suspect uses the wrong form to the next class — it becomes Critique 2 material.",
    )

    print(deck.save(OUTPUT))


if __name__ == "__main__":
    build()
