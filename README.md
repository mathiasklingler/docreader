# docreader
Reads all files from root folder filtered by filenames and words within the files and output the results.

# Install requirements. Edit path as specified
python_crypto_trading_bot/bin/pip3 install -r python_crypto_trading_bot/Script/requirements.txt


# Instruction to build image and run container
# build Image named docreader
docker build -t docreader .
# run docreader image in container, accessible on http://localhost:5050/
docker run -p 5050:5000 docreader