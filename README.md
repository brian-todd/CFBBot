# CFBBot
Chatbot for CFB implemented with RASA/SpaCy with data from [collegefootballdata.com](collegefootballdata.com)

# Setup

The first step is to install the package requirements:

```pip install -r requirements.txt```

With all the packages installed, we can begin to train our models on our existing NLU data:

```rasa train```

There! Now we have an environment setup with trained models.

# Usage

In order to go about using the software, we have to start an `actions` server:

`rasa run actions`

And we can then either start a shell with `rasa shell` or a chat environment with `rasa x`.
