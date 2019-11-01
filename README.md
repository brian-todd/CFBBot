# CFBBot
Simple chatbot that keeps you up to date on the recent results of a particular college football team. 

# Setup

The first step is to install the package requirements:

```pip install -r requirements.txt```

With all the packages installed, we can begin to train our models on our existing NLU data:

```rasa train```

There! Now we have an environment setup with trained models.

# Usage

In order to go about using the software, we have to start an `actions` server:

`rasa run actions`

And we can then either start a shell with `rasa shell --cors '*'` or a chat environment with `rasa x`.
