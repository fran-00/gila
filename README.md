# GILA - AI Chatbot

## How to set up development environment

To run from source, you'll need Python 3.12 and Git installed in your system. You'll also need some API Keys, but we'll cover it up later. Clone this project:

        git clone https://github.com/fran-00/gila.git

On Windows create a new virtual environment with venv and activate it:

        py -m venv venv
        venv/Scripts/Activate.ps1

Install project's required packages via pip:

        pip install -r requirements.txt

Now you need an OpenAI, Google, Mistral and Cohere API Keys. Once you got them, store them on a *api_keys.json* file like this:

        {
            "COHERE_API_KEY": "XXXXXXX",
            "MISTRAL_API_KEY": "XXXXXXX",
            "GOOGLE_API_KEY": "XXXXXXX",
            "OPENAI_API_KEY": "XXXXXXX"
        }

Put this file inside the *storage* dir and you're ready! Now you can run the program as a Python package:

        py -m gila

## How to build the .exe file

On the root directory (with the virtual environment activated and PyInstaller installed):

        pyinstaller build.spec

The command used to create the spec file was this:

        pyinstaller cli.py --onefile --name gila --add-data="storage/saved_settings.json:." --add-data="storage/assets:."

You will find **gila.exe** executable file inside *dist* directory: remember to copy *storage* folder there before distributing it!

## Notes

APIs do have rate limits. To know more:

- [OpenAI](https://platform.openai.com/docs/guides/rate-limits/rate-limits)
- [Gemini Models](https://ai.google.dev/models/gemini)

## TODO List

- [x] Add a Menu on the left side of screen to adjust settings (model and temperature) and start a new chat
- [x] Sidebar must be hideable.
- [x] Add a way to load API keys and create a .json file to store them
- [x] Check Internet connection before every request to API, show a modal if client is not connected. Or/and change the color of chatlog to grey.
- [x] Ensure that model is disconnected from client on window closing.
- [x] Add a loading view on startup.
- [x] Add the ability to continue a conversation and a list of past chat to ui.
- [x] Add custom exceptions to handle as many kind of server's request errors as possible.
- [x] Prompt line must be a QTextEdit widget instead of a QLineEdit widget.
- [x] If user wants to export the current conversation, they must be able to choose file format between .txt, .docx and .pdf.
- [x] User must not be able to send another prompt if the program is waiting for API response and there must be a "waiting" symbol, like a spinning wheel.
- [x] User must be able to choose response length.
- [x] Last used settings must be saved to an external file for future use, like the current llm, temperature and maximum number of tokens.
- [x] Add the ability to change the lenght of the response.
- [x] Add a token counter, at least for OpenAI. Use [tiktoken](https://github.com/openai/tiktoken).
- [x] User must be able to rename stored chats.
- [x] Chatlog must show the number of token used.
- [x] Find a way to exit the main thread if the chat is taking too long to respond.
- [ ] Fix the gila monster image visible when opening the program not remaining aligned to the center when the window is resized.
- [ ] Add specific settings for images generation models like Dall-E 2 and 3.

## Useful Docs

- [Gemini Pro API count tokens](https://ai.google.dev/tutorials/python_quickstart#count_tokens)
- [OpenAI API max tokens](https://platform.openai.com/docs/api-reference/chat/create#chat-create-max_tokens)
- [Cohere API Generate](https://docs.cohere.com/reference/generate)
- [PyInstaller](https://pyinstaller.org/en/stable/)
- [PyUpdater](https://www.pyupdater.org/)
- [GitPython](https://gitpython.readthedocs.io/en/stable/)

## Gila Updater (Not yet implemented)

The Model runs a method to compare the sha of the running project (saved in a configuration file in the *storage* folder) with that of the latest commit on the remote repo.
If the two shas don't match, the Model sends a Boolean signal to the controller, which will tell the view to show a modal asking the user if he wants to update the program.

If the user agrees, the Gila process closes and the remote repo will be cloned locally via the subprocess module. At this point Pyinstaller creates a new executable starting from the updated codebase and puts it in place of the old one.

## Future changes

- Add chat formatting.
- Add Gemini Pro, Anthropic, Meta and Mistral to AI clients.
- Fix .pdf files created when chat is exported.
- Add a way for the app to search for updates from the main branch of the repo using [gitpython](https://gitpython.readthedocs.io/en/stable/)?
- Add image generation to AI Clients that supports it and internal image rendering with Pillow.
- Improve errors and exceptions management.
- Main thread must stop if API is taking too long to respond to prevent GUI freezing.
