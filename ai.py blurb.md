Both scripts now:

Output to terminal in real-time
Save to ~/ai_output_YYYYMMDD_HHMMSS.txt automatically
Include the prompt, files used, and response in the saved file
Print where it saved at the end
ai-zip.py also filters for .java, .xml, .gradle, .kt, .py, .js, .ts files from zips.

Ai-prompt == feed it your prompt to see how large it is - requires 'tiktoken'

Just feed it like others 

python3 script.py "Your question here"
python3 script.py "Your question" file1.java file2.java
python3 script.py "Your question" myproject.zip
