# Mental health awareness chatbot

This conversational agent is build to support police officers to keep an eye on their mental health.
The agent uses the Stress First Aid method to walk users through a mental health checkup.

This project is the master thesis work of Robin Cromjongh. Once published, the resulting thesis report will be linked here.

## Dependencies

This project uses the following libraries and datasets:

- Rasa version 3.0.9 (instructions [here](https://rasa.com/docs/rasa/installation/))
- spacy (instructions [here](https://rasa.com/docs/rasa/installation/#dependencies-for-spacy))
- spacy dataset nl_core_news_lg

## Building the bot

From the agent folder, first validate the yml documents using `rasa data validate --domain domain`.
To train the model, run `rasa train --domain domain`.

You can run the test stories by `rasa test`.

To have conversations locally, open one terminal and execute `rasa run actions`, in another execute `rasa shell`.
