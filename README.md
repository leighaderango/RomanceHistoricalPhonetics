# Digitally Mapping Romance Phonetic Outcomes

A visual presentation of the modern pronunciation of Latin consonants across the Romance languages, inspired by the L'Atlas Linguistique Roman (ALiR) 1987

View the app here: https://digital-qdfh.streamlit.app/

Data compiled digitally by Tim Bertucci, code by Leigha DeRango


## Environment Setup

Requires **Python 3.13**. Install it from [python.org](https://www.python.org/downloads/) if needed.

1. Clone the repository:
   ```bash
   git clone https://github.com/leighaderango/RomanceHistoricalPhonetics.git
   cd RomanceHistoricalPhonetics
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   streamlit run streamlit_map.py
   ```

## Deployment

The app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud). The `runtime.txt` file in the repo root pins the Python version used at build time.


