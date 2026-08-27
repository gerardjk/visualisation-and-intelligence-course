# Vision, Color and Perception: slide content

## Core question

What survives as colour moves from the world into a visualisation?

## Opening distinction

The word *yellow* might identify a spectral light, a reflecting surface, an
appearance, a CIE coordinate, an encoded screen colour, or a linguistic
category. These descriptions are related but are not synonyms.

## Light

- A wavelength describes one component of light.
- A spectral power distribution records power across wavelength.
- For an ordinary surface, illumination multiplied by spectral reflectance
  determines the spectrum reaching the eye.
- Additive and subtractive mixing are different physical operations.

## Vision

- S, M and L cones have broad, overlapping spectral sensitivities.
- One cone response cannot identify the wavelength that caused it: the
  principle of univariance.
- A spectrum is compressed to three initial responses.
- Metamers are spectrally different stimuli that produce the same colour
  match for a specified observer and conditions.
- Context, adaptation and later opponent comparisons affect appearance.

## History and measurement

- Newton studied controlled transformations of the stimulus.
- Goethe foregrounded appearance, boundaries and context.
- Maxwell connected three-primary matching to reproduction.
- Munsell ordered surface appearances by hue, value and chroma.
- CIE XYZ standardised colour-matching behaviour mathematically.

## Chromaticity

- Calculate X, Y and Z by integrating a spectrum against the CIE matching
  functions.
- Normalise to x and y to remove one overall scale factor.
- Plot monochromatic wavelengths to construct the spectral locus.
- Additive mixtures lie on straight segments between chromaticities.
- The line of purples closes the locus but is not a sequence of wavelengths.
- Three physical display primaries enclose a triangular gamut.

## Visualisation practice

- Hue, lightness and chroma support different comparisons.
- Test a palette in context, at its actual size and on its actual background.
- Use redundant cues whenever a distinction matters.

## Streamlit lab

Students first run a minimal slider app, then build an explorer with linked
views of a spectrum, schematic cone responses and CIE xy chromaticity. Their
extension adds intensity and verifies that response magnitude changes while
chromaticity remains stable.
