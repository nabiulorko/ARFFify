# ARFFify

🚀 **From Molecular Descriptors to Weka-Ready Datasets in One Click**

ARFFify is an open-source cheminformatics application that automates **PUBCHEM descriptor** generation and converts datasets into **Weka-compatible ARFF files**. 

## ✨ Features

- Generate molecular descriptors and fingerprints using PaDEL-Descriptor
- Import molecular datasets containing SMILES strings
- Automatic descriptor preprocessing and cleaning
- Export datasets directly to Weka-compatible ARFF format
- Support for classification and regression datasets
- User-friendly graphical interface
- Streamlined QSAR and machine learning workflow

## 🔄 Workflow

```text
           Input Bioactivity Data (ID, SMILES, Class)
                      │
                      ▼
            Descriptor Generation
    (PaDEL-Descriptor)
           │
           ▼
    Data Processing
           │
           ▼
      ARFF Export
           │
           ▼
      Weka Analysis
```

## 📦 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/ARFFify.git
cd ARFFify
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Verify Java Installation

PaDEL-Descriptor requires Java.

```bash
java -version
```

## 🚀 Usage

Run the application:

```bash
python arffify.py
```

### Basic Steps

1. Load a CSV file containing SMILES strings.
2. Select descriptor or fingerprint generation options.
3. Run PaDEL-Descriptor.
4. Review generated descriptors.
5. Export the dataset as an ARFF file.
6. Open the ARFF file in Weka for machine learning analysis.

## 📄 Input Example

```csv
SMILES,Class
CCO,1
CCN,0
CCCO,1
```

## 📊 Output Example

```arff
@RELATION bioactivity

@ATTRIBUTE MW NUMERIC
@ATTRIBUTE XLogP NUMERIC
@ATTRIBUTE Class {0,1}

@DATA
180.16,2.34,1
250.22,3.45,0
```

## 🎯 Applications

- QSAR Modeling
- QSPR Modeling
- Drug Discovery
- Bioactivity Prediction
- Virtual Screening
- Machine Learning for Cheminformatics

## 🛠 Tech Stack

- Python
- PaDEL-Descriptor
- Pandas
- NumPy
- Weka
- Java

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

## 📜 License

This project is licensed under the MIT License.

## 👨‍🔬 Author

Developed for researchers, students, and professionals working in cheminformatics, QSAR, and machine learning.

---

⭐ If you find ARFFify useful, please consider starring the repository.
