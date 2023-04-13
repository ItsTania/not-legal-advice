# not-legal-advice
Making law summaries accessible with AI and Natural Language Processing Tools

## Quick Start

After cloning the repo, do the following to get started!

1. Create a conda environment from the yml file

2. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

3. Add your [API key](https://beta.openai.com/account/api-keys) and [Pinecone Key and Environment](https://app.pinecone.io/) to the newly created `.env` file

4. Run the app

   ```bash
   $ flask run
   ```

--------

The project extends the OpenAI API [quickstart tutorial](https://beta.openai.com/docs/quickstart). It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. 