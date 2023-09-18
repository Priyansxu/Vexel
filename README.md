# AI-Text-Or-Image-Chat-Bot-Python
<h2> Chat Bot for Discord </h2> 

Uses Discord.py and OpenAI API to generate text or image responses based on prompts received by user. Parses user input and generates appropriate response, e.g. "!ask What is Computer Science?" or "!draw cat chasing dog, 1024x1024". 

Includes error handling, pagination for responses over 2000 characters (Discord's limit), and prepends escape character \ to > (quote block) and / (command). 

** Rename .env.template to .env and enter credentials between quotes. Be sure not to delete .gitignore or .env from .gitignore if pushing to repo. 

** To install the required dependencies, run the following command after cloning the repository: pip install -r requirements.txt
