Run Actor locally

Install Apify CLI

Via Homebrew

brew install apify-cli

Using NPM

npm -g install apify-cli

Create and run Actor

Create new Actor using this template

apify create my-actor -t project_langchain_js

Run the Actor locally

cd my-actor
apify run

Deploy on Apify

Log in to Apify

You will need to provide your Apify API token to complete this actions.

apify login

Deploy your Actor

This command will deploy and build the Actor on the Apify Platform. You can find your newly created Actor under My Actors

apify push

