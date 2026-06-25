<div align="center">

<h1>🤖 <span style="color:#000000">ARFF</span><span style="color:#1a73e8">ify</span></h1>

<p style="color:#666; font-size:0.95rem;">Generate PubChem fingerprints via PaDEL-Descriptor and export Weka-ready ARFF files</p>

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![PaDEL](https://img.shields.io/badge/PaDEL--Descriptor-PubChem%20FP-1a73e8?style=flat-square)
![Weka](https://img.shields.io/badge/Weka-ARFF%20Ready-2e7d32?style=flat-square)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-0d1b2a?style=flat-square)

</div>

---

## 📖 Overview

**ARFFify** is a Streamlit web app that takes a bioactivity CSV file (containing molecule IDs, SMILES strings, and class labels), computes **PubChem fingerprints** using PaDEL-Descriptor, and packages everything into a `.arff` file ready for machine-learning workflows in **Weka**.

> 💡 No command-line knowledge needed — the entire pipeline runs through a clean, step-by-step browser interface.

---

## ⚙️ How It Works

<table>
<tr>
<td align="center"><b>📂</b><br/><sub>STEP 1</sub><br/><b>Upload CSV</b><br/><sub>Drop your bioactivity file<br/>with ID, SMILES & Class</sub></td>
<td align="center"><b>🏷️</b><br/><sub>STEP 2</sub><br/><b>Name Relation</b><br/><sub>Set the <code>@relation</code><br/>tag for your ARFF</sub></td>
<td align="center"><b>🔬</b><br/><sub>STEP 3</sub><br/><b>PaDEL Settings</b><br/><sub>Toggle salt removal,<br/>aromaticity & tautomers</sub></td>
<td align="center"><b>🗂️</b><br/><sub>STEP 4</sub><br/><b>Class Labels</b><br/><sub>Map 1/0 → active/inactive<br/>or keep originals</sub></td>
<td align="center"><b>⬇️</b><br/><sub>OUTPUT</sub><br/><b>Download ARFF</b><br/><sub>One-click download of<br/>your Weka-ready file</sub></td>
</tr>
</table>

---

## 📋 Input CSV Format

Your CSV must contain exactly these three columns (case-sensitive):

| Column | Type | Description |
|--------|------|-------------|
| `ID` | string / int | Unique molecule identifier (e.g. ChEMBL ID, compound name) |
| `SMILES` | string | Valid SMILES string representing the molecular structure |
| `Class` | int / string | Bioactivity label — e.g. `1`/`0` or `active`/`inactive` |

**Example:**

```csv
ID,SMILES,Class
CHEMBL1,CC(=O)Oc1ccccc1C(=O)O,1
CHEMBL2,c1ccc2ccccc2c1,0
CHEMBL3,CC(C)Cc1ccc(cc1)C(C)C(=O)O,1
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Java 8+ (required by PaDEL-Descriptor)

### Install dependencies

```bash
pip install streamlit pandas padelpy
```

### Run the app

```bash
streamlit run ARFFify.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🔧 PaDEL-Descriptor Options

| Option | Default | Description |
|--------|---------|-------------|
| Remove salt | ✅ On | Strips salt fragments from multi-component structures |
| Detect aromaticity | ✅ On | Assigns aromaticity before descriptor calculation |
| Standardize tautomers | ✅ On | Converts structures to a canonical tautomeric form |
| Standardize nitro groups | ✅ On | Normalises nitro group representation |
| Standardize molecules | ✅ On | General molecular standardization pass |
| SMIRKS tautomers file | None | Optional custom tautomer rules (`.txt` / `.tsv` / `.smirks`) |

---

## 📄 Output ARFF Structure

The generated file follows the standard Weka ARFF format:

```
@relation CDK5_pubchem

@attribute PubchemFP0 numeric
@attribute PubchemFP1 numeric
...
@attribute PubchemFP880 numeric
@attribute class {active, inactive}

@data
0,1,0,1,...,active
1,0,1,0,...,inactive
```

> ✅ **881 PubChem fingerprint bits** are extracted per molecule and written as numeric attributes.

---

## ⚠️ Notes & Limitations

> ⚠️ If PaDEL fails to process a molecule (e.g. invalid SMILES), it is silently skipped. The app will warn you if the output row count differs from the input and will match by order.

- Processing time scales with the number of compounds — large datasets (1 000+) may take several minutes.
- Java must be installed and accessible on your system `PATH` for PaDEL to run.
- The `@relation` name must not contain spaces (use underscores instead).
- Class label mapping (`1→active`, `0→inactive`) only works for binary integer labels.

---

## 🛠️ Tech Stack

- **Streamlit** — web interface
- **pandas** — CSV loading & data manipulation
- **padelpy** — Python wrapper for PaDEL-Descriptor
- **PaDEL-Descriptor** — molecular fingerprint computation (Java)
- **PubChem Fingerprints** — 881-bit binary fingerprint schema

---

## 📜 License

© 2026 Nabiul Orko. All Rights Reserved.

---

<div align="center">
<table width="100%" style="background:linear-gradient(90deg,#0d1b2a,#1a3a5c);border-radius:10px;border:none;">
<tr>
<td style="padding:14px 20px;">
<span style="font-size:1.1rem;font-weight:800;color:#ffffff;">🤖 ARFF<span style="color:#4da6ff;">ify</span></span>
</td>
<td align="right" style="padding:14px 20px;">
<span style="color:#a0b8cc;font-size:0.78rem;">
Designed & developed by <a href="https://www.linkedin.com/in/nabiulorko" style="color:#4da6ff;font-weight:600;">Nabiul Orko</a><br/>
<span style="color:#6a8a9e;font-size:0.72rem;">PaDEL-Descriptor · PubChem FP · Python · Streamlit</span><br/>
<span style="color:#4a6a7e;font-size:0.70rem;">© 2026 All Rights Reserved</span>
</span>
</td>
</tr>
</table>
</div>
