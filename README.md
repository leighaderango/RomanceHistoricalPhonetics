# Digitally Mapping Romance Phonetic Outcomes

A visual presentation of the modern pronunciation of Latin consonants across the Romance languages, inspired by the L'Atlas Linguistique Roman (ALiR) 1987

View the app here: https://digital-qdfh.streamlit.app/

Data compiled digitally by Tim Bertucci, code by Leigha DeRango


## Environment Setup

There are two ways to set up the development environment:

### Option 1: Using Conda (Recommended)

1. Install [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. Clone the repository:
   ```bash
   git clone https://github.com/leighaderango/RomanceHistoricalPhonetics.git
   cd RomanceHistoricalPhonetics
   ```

3. Create and activate the Conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate romance_phonetics
   ```

### Option 2: Using pip and venv

1. Ensure you have Python 3.10 or later installed

2. Clone the repository:
   ```bash
   git clone https://github.com/leighaderango/RomanceHistoricalPhonetics.git
   cd RomanceHistoricalPhonetics
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix or MacOS:
   source .venv/bin/activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```


