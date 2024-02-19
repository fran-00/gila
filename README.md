# AI Chatbot

## How to set up development environment

To run from source, you'll need Python 3.12 and Git installed in your system. You'll also need some API Keys, but we'll cover it up later. Clone this project:

        https://github.com/fran-00/metis.git

On Windows create a new virtual environment with venv and activate it:

        py -m venv venv
        venv/Scripts/Activate.ps1

Install project's required packages via pip:

        pip install -r requirements.txt

Now you need an OpenAI API Key and a Google API Key. Once you got them, store them on a *.env* file like this:

        OPENAI_API_KEY="XXXXXXX"
        GOOGLE_API_KEY="XXXXXXX"

Put this file inside ai folder and you're ready! Run the program:

        py main.py

## Notes

APIs do have rate limits. To know more:

- [OpenAI](https://platform.openai.com/docs/guides/rate-limits/rate-limits)
- [Gemini Models](https://ai.google.dev/models/gemini)

## TODO List

- [ ] Add a Pop Up Menu on the left side of screen to adjust settings (model and temperature) and start a new chat
- [ ] Chat log must use markdown instead of html to parse styled responses.
- [ ] Conversations must be saved on every chat iteration on an archive folder.
- [ ] If user wants to export the current conversation, they must be able to choose file format between .txt, .docx and .pdf.
- [ ] User must be able to choose response max length (very short, short, medium, long).
- [ ] Current settings must be saved to an external file for future use, like the current llm.
- [ ] User must not be able to send another prompt if the program is waiting for API response.
- [x] Add a way to load API keys and create a .env file to store them
- [x] Check Internet connection before every request to API, show a modal if client is not connected. Or/and change the color of chatlog to grey.
- [ ] Ensure that model is disconnected from client on window closing.
- [x] Add a loading view on startup.
- [ ] Prompt line must be a QTextEdit widget instead of a QLineEdit widget.
