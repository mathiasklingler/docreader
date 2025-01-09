# docreader
Reads all files from root folder filtered by filenames and words within the files and output the results.

# Install requirements. Edit path as specified
python_crypto_trading_bot/bin/pip3 install -r python_crypto_trading_bot/Script/requirements.txt


# Instruction to build image and run container
# build Image named docreader
docker build -t docreader .
# run docreader image in container, accessible on http://localhost:5050/
docker run -p 5050:5000 docreader

# User requirements
Ich möchte Dokumente von einem Bauprojekt, mit aut. einfacher Prüfung wo prüft
- wie gross ist die Datei
- wieviel Worte, Anzahl zeichen
- Plan oder Dokument
- Welche Möglichkeiten gibt es
- Einfache inhaltliche Suche
- 
Pain:
- Input: Hilfstabelle mit fest definierten Namen von Dokumenten.
- Input: Root-Ordner
- Anhand einer Excel-Liste von einer Struktur
- Wir wollen das Dokumente Beutzervereinbarung, Bericht, Plan, ....
- 
Python Code geschrieben. V0.1. Desktop Application V0.2 WebApp, V0.3 WebApp public

Weitere Anforderungen (noch nicht implementiert)
- 