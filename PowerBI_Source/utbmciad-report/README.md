# MCU analysis report (LaTeX)

LaTeX sources of the MCU analysis report:

| Source | PDF | Language |
|---|---|---|
| `main.tex` | `MCU_Analyse_Performances_Commerciales_Critiques_FR.pdf` | French |
| `main_en.tex` | `MCU_Commercial_Critical_Performance_Analysis_EN.pdf` | English |

Figures (Power BI screenshots) are in `figures/`. Both versions contain the same sections and figures.

## Build

The reports compile with XeLaTeX. Run it three times so that the table of contents is up to date, then rename the output:

```bash
xelatex main.tex
xelatex main.tex
xelatex main.tex
```

`main.pdf` is then copied to `MCU_Analyse_Performances_Commerciales_Critiques_FR.pdf`; do the same with `main_en.tex` for the English PDF.

## Template

The layout started from a neutral starter that follows the structure of the `utbmciad-report` class (upstream: https://ctan.org/pkg/utbmciad-report). It uses standard classes only; no upstream class files or institutional logos are included. The upstream LaTeX source is LGPL-3.0, and its logo files have separate institutional terms.
