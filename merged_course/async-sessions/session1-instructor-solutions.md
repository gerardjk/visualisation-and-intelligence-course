# Session 1 — Asynchronous exercises: instructor solutions

Instructor reference for the exercises on the student site
(https://dvn36104.github.io). **Visibility policy (17 Aug
2026):** the *mid-part* exercises (A-1 `ex_wing`, B-1 `ex_carnivora`,
C-1 `ex_density`, D-1 `ex_radius`) show students a worked solution behind Hint → Hint →
"Show Solution" buttons. The **final exercise of each part** (A-2
`ex_family`, B-2 `ex_split`, C-2 `ex_hubble`, D-2 `ex_table`) has **no solution on the
site** — students get two non-code hints plus a "how to know you got it"
self-check, and the full solutions below are instructor-only.

Source of truth: `student-site/session1/part-{a,b,c,d}.qmd`.

---

## Part A · Allometry

### A-1 `ex_wing` — A different trait pair (wing vs tarsus)

**Task.** Repeat the full pipeline — cleaning included — for wing length
vs tarsus length, starting from the raw `birds` table (90,371 rows), not
from `clean`. Aggregate to species means and plot at species level,
printing n at each step.

**Solution.**

```python
clean_w = birds.dropna(subset=["species", "wing_length_mm", "tarsus_length_mm"])
print(f"{len(birds):,} rows → {len(clean_w):,} rows")

species_w = (clean_w
             .groupby("species")[["wing_length_mm", "tarsus_length_mm"]]
             .mean())

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(np.log10(species_w["tarsus_length_mm"]),
           np.log10(species_w["wing_length_mm"]),
           s=4, alpha=0.25, color="#e66852")
ax.set_xlabel("log10 tarsus length (mm)")
ax.set_ylabel("log10 wing length (mm)")
ax.set_title(f"Species means (n = {len(species_w):,})")
plt.show()
```

**Expected output / checks.** Wing length is missing in only ~1,100 rows,
so `clean_w` keeps far more data (~89,000 rows) than the beak comparison
did (69,509). The wing–tarsus cloud is visibly tighter than beak–tarsus.
Five points sit stranded at log10(wing) ≈ −1: the five kiwi species,
whose wing length is coded 0.1 mm (a placeholder, not a measurement) —
the solution block now uses this as a sentinel-value teaching point
(dropna cannot catch missingness written down as a fake number).

**Marking notes.** The key error to look for: dropping on the *beak*
column (or reusing `clean`) instead of requiring exactly the columns the
comparison uses. The point of the exercise is that n depends on the
comparison chosen, and that cleaning is per-question, not per-dataset.

### A-2 (replaced 19 Aug): Part II open investigation on the amniote database

The guided Amniote section and `ex_family` were replaced by a five-stage
student-owned investigation (expectations/structure, unit of analysis,
validation, row accounting, final chart + one rank up). Full instructor
guide with verified numbers and the two planted defects (4 rows with
maturity <= 0 days; 35 rows with maturity > longevity after the days/years
unit conversion) lives in `student-site/session1/_instructor-a.qmd`
(instructor build only). Key anchors: classes 9,802/6,567/4,953; 465
families, Scincidae largest (1,351); mass-longevity pair 5,122 (24%),
r 0.519 at species level, 327 families and r 0.649 at family level with
logged means.

---

## Part B · Tree of Life

### B-1 `ex_carnivora` — The carnivore clade

**Task.** Extract the clade containing Canidae and Felidae from the
amniote family tree, draw it labelled, print how many families it holds
and the age of their common ancestor.

**Solution.**

```python
carnivora = clade(amniotes, ["Canidae", "Felidae"])

print(f"{len(carnivora.leaves())} families, common ancestor "
      f"{root_age - carnivora.depth:.1f} Myr ago")

fig, ax = plt.subplots(figsize=(8, 4))
draw_tree(carnivora, ax, labels=True, fontsize=9)
ax.set_xlabel("Myr since the amniote root")
plt.show()
```

**Expected output.** 16 families, common ancestor ~55.4 Myr ago.

**Discussion points (in the student-visible solution).** Cats' closest
relatives in the clade are the civets (Viverridae-2, MRCA 33.3 Mya),
then hyaenas and mongooses — not dogs; dogs sit on
the other side of the first split, nearer bears and seals. "Cats and
dogs" have been separate lineages roughly since the dinosaurs left.

### B-2 `ex_split` — Close the loop (write `divergence`)

**Task.** Write `divergence(root, a, b)` returning Myr since the lineages
of tips a and b split; date the Mammalia–Aves split in the eukaryote
class tree; compare with the amniote file's root age (319.0 Myr).

**Solution.**

```python
def divergence(root, a, b):
    set_depths(root)
    root_age = max(l.depth for l in root.leaves())
    return root_age - clade(root, [a, b]).depth

split = divergence(euk, "Mammalia", "Aves")
print(f"Mammalia-Aves split in the eukaryote class tree: {split:.1f} Mya")
print(f"Amniote root in the family-level file:           319.0 Mya")
```

**Expected output.** Both lines read 319.0 Mya.

**Marking notes.** The conceptual step is realising the split date is the
age of the MRCA, and "age" = root age − depth (depth runs root→tip, age
runs tip→root). The discussion point that matters: the two files agree to
the decimal because both come from TimeTree's single consensus —
agreement between two views of one database is *consistency*, not
independent confirmation.

---

## Part C · The Triangle of Everything

### C-1 `ex_density` — Interrogate the densities

**Task.** Rank all 29 objects by density (densest first), print rank /
name / group / density; compute the red giant vs white dwarf density gap
in decades.

**Solution.**

```python
order = np.argsort(rho_all)[::-1]

for rank, i in enumerate(order, 1):
    print(f"{rank:>2}. {names[i]:<20} {groups[i]:<18} {rho_all[i]:>9.1e} g/cm³")

gap = np.log10(rho_all[names.index("white dwarf")]
               / rho_all[names.index("red giant")])
print(f"\nred giant vs white dwarf: {gap:.0f} decades of density")
```

**Expected output.** Top of table: top quark (5.0e25), Higgs boson
(1.4e25), proton (6.7e14), neutron star (3.9e14). Bottom: supercluster
(2.2e-29), observable Universe (9.1e-30). Gap = **12 decades**.

**Marking notes.** `np.argsort` ascending then `[::-1]` is the intended
one-liner; a manual sorted() over indices is fine too. Discussion: the
"density" of a fundamental particle is a strange quantity (radius is a
quantum limit, not a surface); red giant and white dwarf have nearly the
same mass — the pair (mass, radius) is what distinguishes them.

### C-2 `ex_hubble` — Put the Universe on the wall

**Task.** From H₀ alone: Hubble radius r_H = c/H₀, critical density
ρ_c = 3H₀²/8πG, mass of the Hubble sphere; then the Schwarzschild radius
of that mass, compared to r_H.

**Solution.**

```python
r_H   = c / H0
rho_c = 3 * H0**2 / (8 * np.pi * G)
m_U   = 4/3 * np.pi * r_H**3 * rho_c

r_s = 2 * G * m_U / c**2
print(f"r_H = {r_H:.2e} cm   m_U = {m_U:.2e} g")
print(f"Schwarzschild radius of the Universe's mass: {r_s:.2e} cm")
print(f"ratio r_s / r_H = {r_s / r_H:.3f}")
```

**Expected output.** r_H ≈ 1.32e28 cm, m_U ≈ 8.8e55 g, ratio = **1.000**.

**Marking notes.** The punchline is in the algebra (shown in the
student-visible solution): substituting ρ_c into m_U into r_s cancels
every constant, so r_s = r_H *identically* — a critical-density universe
must sit on the black-hole line for any H₀. The transferable lesson: when
a data point lands exactly on a theory line, check whether both were
computed from the same ingredients. Common student error: forgetting to
cube r_H, which makes the ratio come out ~1e-57 and is immediately
visible.

---

## Part D · The Periodic Spiral

### D-1 `ex_radius` — The size of atoms (mid-part, solution ON the site)

**Task.** Plot covalent radius vs Z for all 118 elements, highlighting
alkali metals and noble gases.

**Solution.** Three scatter layers over a faint line (full code in the
site's solution block). Expected: sawtooth with peaks at alkali metals —
Ar 96 pm jumps to K 196 pm at the shell closure.

**Marking notes.** Watch for off-by-one indexing (`radius[z]` instead of
`radius[z - 1]`).

### D-2 `ex_table` — The whole thing (FINAL, instructor-only solution)

**Task.** Build the full canonical 118-element table: main grid from
`group`/`period`, lanthanides and actinides in two footnote rows of 15,
cells coloured by category.

**Solution.**

```python
def cell_position(i):
    if group[i] is not None:
        return group[i], period[i]
    if 57 <= Z[i] <= 71:
        return 3 + (Z[i] - 57), 9      # lanthanide footnote row
    return 3 + (Z[i] - 89), 10         # actinide footnote row
```

then the Rectangle/text loop from the exercise scaffold. Expected: the
standard 18-column table — H top-left, He above Ne, solid colour blocks,
two footnote rows separated from row 7 by a blank row.

**Marking notes.** The whole exercise is `cell_position`'s three cases.
Accept any footnote column constant keeping x within 1–18. Common
errors: crashing on `group = None` (missed the f-block case); upside-down
table (sign of y); footnote rows touching row 7. Reward extensions:
legend, Z labels, or a 32-column no-footnote variant (that variant is
exactly Section 6's design conversation).
