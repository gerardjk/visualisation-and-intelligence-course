# Full Course Outline

## Course title

**Visualisation and Intelligence: Narrative, Critique, and Analytics**

## Course logic

This course teaches students to build visualisations, but it is not primarily about producing attractive charts. It is about developing visual judgement. Students learn to connect user stories, visual tasks, chart choices, interface design, deployment, disclosure, and responsible interpretation.

The repeated workflow is:

```text
User story → Visual task → Visual form → Interaction → Deployment → Disclosure → Review → Defence
```

The course uses the FT Visual Vocabulary as the shared language for visual task classification and chart selection.

---

## Week 1 — Seeing Data: Visualisation, Intelligence, and Interpretation

### Core question

How do charts create meaning?

### Core message

A visualisation is not merely a picture of data. It is an act of selection, comparison, compression, framing, and interpretation.

### Content outline

1. **Data, chart, insight, narrative**
   - Data as structured evidence.
   - Charts as selective visual encodings.
   - Insights as claims that require justification.
   - Narratives as ordered interpretations.

2. **Visualisation and intelligence**
   - Human visual intelligence: perception, attention, comparison.
   - Machine-generated outputs: charts, captions, summaries, and code.
   - Institutional intelligence: dashboards and visual data products used to support decisions.

3. **Generated charts and hallucinated insight**
   - Compare human-made and generated visualisations.
   - Identify unsupported claims.
   - Distinguish fluent interpretation from valid interpretation.

4. **Data governance from the start**
   - Who is represented?
   - Who collected the data?
   - Who benefits from the visualisation?
   - Who could be harmed?
   - What should not be visualised?

### Studio

Students complete Critique 1 using a structured template.

### Lightweight responsibility prompt

Could this visualisation lead a viewer to believe something that the data does not actually support?

### References

Required:

- Cairo, *How Charts Lie*, selected chapter.
- D’Ignazio and Klein, *Data Feminism*, selected chapter.
- Maiam nayri Wingara and AIGI, *Indigenous Data Sovereignty Communique*.

Recommended:

- Munzner, “A Nested Model for Visualization Design and Validation.”
- Hicks, Humphries and Slater, “ChatGPT is bullshit.”
- Bender et al., “On the Dangers of Stochastic Parrots.”

---

## Week 2 — Choosing Visual Forms: Encoding, Tidy Data, and the Visual Vocabulary

### Core question

What visual task are we performing?

### Core message

Good chart choice begins with the analytical task, not with the visual effect.

### Content outline

1. **Visual channels**
   - Position, length, angle, area, colour, shape, texture, motion.
   - Why some comparisons are easier than others.

2. **FT Visual Vocabulary**

| Category | Core use |
|---|---|
| Deviation | values differ from a baseline or target |
| Correlation | variables move together or apart |
| Ranking | ordering items |
| Distribution | spread, range, clusters, outliers |
| Change over time | temporal pattern |
| Magnitude | comparing sizes |
| Part-to-whole | composition |
| Spatial | location or geography |
| Flow | movement, transfer, connection |

3. **Task-to-chart mapping**
   - Bar and dot plots for magnitude and ranking.
   - Line charts and small multiples for change over time.
   - Scatterplots for correlation.
   - Histograms, box plots, dot plots, and densities for distributions.
   - Choropleths, proportional symbols, and maps for spatial tasks.
   - Sankey, alluvial, and flow maps for flow tasks.

4. **Tidy data**
   - Each variable is a column.
   - Each observation is a row.
   - Each value is a cell.
   - Tidy structure supports Tableau, pandas, Altair, and AI-generated code.

5. **AI-assisted wrangling**
   - Ask an intelligent tool to reshape data.
   - Verify identifiers, row counts, missing values, data types, and transformations.

### Studio

Students redesign a weak chart three ways and classify each redesign using the FT Visual Vocabulary.

### Lightweight responsibility prompt

Does the selected visual form fit the task, or does it encourage an easier but wrong interpretation?

### References

Required:

- Financial Times Visual Vocabulary.
- Franconeri et al., “The Science of Visual Data Communication.”
- Wickham, “Tidy Data.”

Recommended:

- Cleveland and McGill, “Graphical Perception.”
- Heer and Bostock, “Crowdsourcing Graphical Perception.”
- Long and Kay, “To Cut or Not To Cut?”
- Crameri et al., “The Misuse of Colour in Science Communication.”
- Ware, Stone and Szafir, “Rainbow Colormaps Are Not All Bad.”

---

## Week 3 — Dashboards, Personas, and User Stories: Tableau Public

### Core question

Who is this for and what do they need to do?

### Core message

A dashboard is not a collection of charts. It is an interface for a user with a purpose.

### Content outline

1. **Tableau Public fundamentals**
   - Connecting to CSV.
   - Dimensions and measures.
   - Marks card.
   - Filters.
   - Calculated fields.
   - Dashboard layout.
   - Publishing to Tableau Public.
   - Public-data warning.

2. **Personas**
   - Executive or minister.
   - Public/community audience.
   - Investigative journalist.
   - Technical analyst.

3. **User stories**
   - `As a [user], I want to [task], so that [purpose].`
   - User stories connect audience to design choices.

4. **Visual Vocabulary in dashboard planning**
   - Main dashboard question.
   - Primary visual task.
   - Secondary visual task.
   - Chart forms.
   - Interaction choices.

5. **Methodology-change trap**
   - Stable definitions.
   - Category changes.
   - Structural breaks.
   - Missing values.
   - Provider metadata.

### Studio

Students build a one-page Tableau Public dashboard and defend it for a persona.

### Lightweight responsibility prompt

Could this persona make a plausible but wrong decision from the dashboard?

### References

Required:

- Sarikaya et al., “What Do We Talk About When We Talk About Dashboards?”
- Bach et al., “Dashboard Design Patterns.”
- Financial Times Visual Vocabulary.

Recommended:

- Setlur et al., “Heuristics for Supporting Cooperative Dashboard Design.”
- Few, *Information Dashboard Design*, selected pages.
- Wexler, Shaffer and Cotgreave, *The Big Book of Dashboards*.

---

## Week 4 — Interactive Data Apps with Streamlit

### Core question

How does a user interact with the data?

### Core message

A data app is a small interactive system: it loads data, transforms it, responds to input, and communicates an interpretation.

### Content outline

1. **Streamlit app structure**
   - `app.py`.
   - imports.
   - page configuration.
   - data loading.
   - layout.

2. **Data loading patterns**
   - local CSV.
   - public URL.
   - API.
   - uploaded file.
   - database.

3. **Streamlit controls**
   - `st.sidebar.selectbox`.
   - `st.sidebar.multiselect`.
   - `st.slider`.
   - `st.dataframe`.
   - `st.altair_chart`.
   - `st.columns`.
   - `st.expander`.

4. **Interface basics**
   - Page hierarchy.
   - Visual hierarchy.
   - Controls and affordances.
   - Empty states.
   - Error states.
   - Progressive disclosure.

5. **AI-assisted coding**
   - Good prompts specify data structure, output, constraints, and explanation needs.
   - Students must be able to explain code they submit.

### Studio

Groups build a local minimum viable Streamlit app.

### Lightweight responsibility prompt

What does the app make easy to see, and what does it make hard to see?

### References

Required:

- Long and Magerko, “What is AI Literacy?”
- Denny et al., “Computing Education in the Era of Generative AI.”

Recommended:

- White et al., “A Prompt Pattern Catalog.”
- Sentance et al., PRIMM.
- Bastani et al., “Generative AI Can Harm Learning.”
- Lehmann et al., “AI Meets the Classroom.”
- Perry et al., “Do Users Write More Insecure Code with AI Assistants?”

---

## Week 5 — From Prototype to Public Data Product

### Core question

Can someone else open, understand, trust, and use it?

### Core message

A visualisation is not finished when it works locally. It becomes a public data product only when another person can load it, understand it, trust it, and use it.

### Content outline

1. **Publication structure**
   - GitHub repository.
   - `app.py`.
   - `requirements.txt`.
   - `README.md`.
   - `data/`.
   - `docs/`.

2. **Deployment as communication**
   - Streamlit Community Cloud.
   - GitHub connection.
   - app entry point.
   - dependency errors.
   - file path errors.
   - logs.

3. **Trust and reliability**
   - Caching.
   - Source notes.
   - Loading states.
   - Empty states.
   - Error states.
   - Column validation.
   - Dataset updates.

4. **Data and AI Disclosure**
   - Data source.
   - Time period.
   - Unit of analysis.
   - Cleaning and transformations.
   - Visual Vocabulary category.
   - Known limitations.
   - AI assistance.
   - Human verification.
   - Appropriate and inappropriate use.

5. **User story acceptance tests**
   - Does the app actually support the user stories from Week 3?
   - What data and interaction does each user story depend on?
   - What could fail?
   - How does the app guide the user if it fails?

### Studio

Groups deploy the app and complete the Public Data Product Checkpoint.

### Lightweight responsibility prompt

What would make a user trust this app too much?

### References

Required:

- Gebru et al., “Datasheets for Datasets.”
- Mitchell et al., “Model Cards for Model Reporting.”
- Holland et al., “The Dataset Nutrition Label.” Use as background for the disclosure pattern; do not use “nutrition label” as the student-facing term.

Recommended:

- Bender and Friedman, “Data Statements for NLP.”
- Pushkarna et al., “Data Cards.”
- NIST AI Risk Management Framework, selected sections.

---

## Week 6 — Web Visualisation Studio: Maps, Flows, Animation, 3D, and JavaScript Literacy

### Core question

When do we need specialised or web-native visualisation?

### Core message

Specialised visualisation is justified by task, not spectacle.

### Content outline

1. **Specialised visualisation families**
   - Geographic maps.
   - Flow and Sankey diagrams.
   - Networks.
   - Animation.
   - 3D and spatial visualisation.
   - Data art and cinematic effects.

2. **Geographic visualisation**
   - Choropleths.
   - Proportional symbols.
   - Normalisation.
   - Projections.
   - MAUP.
   - Boundary changes.
   - Small-area demographic risk.

3. **Animation and 3D**
   - Animation may increase engagement but often weakens comparison.
   - 3D is usually poor for abstract data on flat screens.
   - 3D can be useful for genuinely spatial or immersive tasks.

4. **JavaScript literacy**
   - HTML = structure.
   - CSS = appearance.
   - JavaScript = behaviour.
   - SVG, Canvas, WebGL.
   - D3, Vega-Lite, Plotly.js, Leaflet, deck.gl, Three.js.
   - Python wrappers: Altair, Plotly, pydeck, folium.

5. **Specialised visualisation decision**
   - Used or rejected.
   - Visual Vocabulary category.
   - Simpler alternative.
   - Risk of misleading.

### Studio

Groups either add a specialised visualisation or justify why they rejected one.

### Lightweight responsibility prompt

Does the specialised form clarify the task, or does it merely impress?

### References

Required:

- Robertson et al., “Effectiveness of Animation in Trend Visualization.”
- Marriott et al., “Immersive Analytics: Time to Reconsider the Value of 3D.”
- Lee et al., “Viral Visualizations.”

Recommended:

- Tversky et al., “Animation: Can it Facilitate?”
- Heer and Robertson, “Animated Transitions in Statistical Data Graphics.”
- Yang et al., “Tilt Map.”
- Monmonier, *How to Lie with Maps*.
- Lisnic et al., “Misleading Beyond Visual Tricks.”

---

## Week 7 — Responsible Interpretation and Visualisation Quality Review

### Core question

Is the interpretation justified, accessible, and responsible?

### Core message

A visualisation can be technically correct and still encourage an unjustified interpretation.

### Content outline

1. **Narrative and framing**
   - Titles.
   - Annotation.
   - Ordering.
   - Emphasis.
   - Omission.
   - Neutral, optimistic, critical, and alarmist framings.

2. **Uncertainty**
   - Estimates vs observations.
   - Confidence intervals.
   - Prediction intervals.
   - Missing data.
   - Error bars.
   - Quantile dotplots.
   - Forecast bands.

3. **Causality**
   - Correlation is not causation.
   - Confounding.
   - Simpson’s paradox.
   - One simple DAG.
   - Caption repair.

4. **Accessibility**
   - Alt text.
   - Colour contrast.
   - Keyboard and screen-reader considerations.
   - Mobile readability.
   - Accessible chart descriptions.

5. **Visualisation Quality Review**
   - Main claim.
   - Audience fit.
   - Visual clarity.
   - Misinterpretation risk.
   - Input/filter robustness.
   - Data and AI Disclosure.
   - AI provenance.
   - Specialised visualisation decision.

### Studio

Groups review another group’s app and complete a structured review report. Each group then revises its own app and writes a revision log.

### Lightweight responsibility prompt

What is the most plausible wrong conclusion a user could draw from this app?

### References

Required:

- Segel and Heer, “Narrative Visualization.”
- Hullman, “Why Authors Don’t Visualize Uncertainty.”
- Lundgard and Satyanarayan, “Accessible Visualization via Natural Language Descriptions.”

Recommended:

- Hullman and Diakopoulos, “Visualization Rhetoric.”
- Kay et al., “When (ish) is My Bus?”
- Correll and Gleicher, “Error Bars Considered Harmful.”
- Padilla, Kay and Hullman, “Uncertainty Visualization.”
- D’Agostino McGowan et al., “Causal Inference Is Not Just a Statistics Problem.”

---

## Week 8 — Present and Defend: Visual Intelligence in Practice

### Core question

Can students defend the whole product?

### Core message

Students should be able to explain and defend the relationship between task, user, data, visual form, interaction, deployment, intelligent-tool use, and interpretation.

### Content outline

1. **Group presentation**
   - Project title.
   - Audience and purpose.
   - User stories.
   - Dataset and source.
   - Main claim or use case.
   - Visual Vocabulary categories.
   - Key visualisations.
   - Interactions.
   - Deployment and reliability choices.
   - Limitations and uncertainty.
   - Intelligent-tool use and verification.
   - Quality review findings and response.

2. **Individual oral defence**
   - Personal contribution.
   - Code/data/design explanation.
   - Limitations and risks.
   - Intelligent-tool use and verification.
   - Communication clarity.

3. **Final reflection**
   - Most important learning.
   - Biggest mistake.
   - Most useful critique.
   - What intelligent tools helped with.
   - What intelligent tools made worse.
   - What to do differently next time.

### References

Required:

- Bearman et al., “Developing Evaluative Judgement for a Time of Generative AI.”
- Sotiriadou et al., “The Role of Authentic Assessment to Preserve Academic Integrity and Promote Skill Development and Employability.”

Recommended:

- Dawson et al., “Validity Matters More Than Cheating.”
- Corbin, Dawson and Liu, “Talk Is Cheap.”
- University of Sydney two-lane assessment model.
- TEQSA, *Assessment Reform for the Age of Artificial Intelligence*.
