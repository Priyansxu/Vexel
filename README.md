# AI-Text-Or-Image-Chat-Bot-Python
<h2>Chat Bot for Discord</h2> 


<h3>Branches</h3>
<h4>--------</h4>
<h4>openai_generation (easiest/default)</h4>
<p>Uses <a href="https://platform.openai.com/">OpenAI API</a> (requires OpenAI API key) and discord.py (requires <a href="https://discord.com/developers/applications">Discord bot token</a>) to generate text or image response based on prompts received by user. Parses user input and generates appropriate response, e.g. "!ask What is Computer Science?" or "!draw cat chasing dog".</p>
<p>Draw button included after every !ask response to draw image based on the response, which can be an ai-generated prompt. system_message includes basic prompt parameters, so "!ask prompt for an epic spaceship battle with fun details" should format it decently well. system_mesage can be changed as desired under text_by_api.py.</p>
<p>Includes error handling, pagination for responses over 2000 characters (Discord's limit), and prepends escape character \ to > (quote block) and / (command).</p>
<h4>--------</h4>
<h4>local_generation</h4>
<p>Uses <a href="https://github.com/dome272/Wuerstchen">warp-ai/wuerstchen</a> model, <a href="https://platform.openai.com/">OpenAI API</a> (requires OpenAI API key) and discord.py (requires <a href="https://discord.com/developers/applications">Discord bot token</a>) to generate text or image response based on prompts received by user. Parses user input and generates appropriate response, e.g. "!ask What is Computer Science?" or "!draw cat chasing dog".</p>
<p>As with openai_generation branch, Draw button included after every !ask response to draw image based on the response, which can be an ai-generated prompt. system_message includes basic prompt parameters, so "!ask prompt for an epic spaceship battle with fun details" should format it decently well. system_mesage can be changed as desired under text_by_api.py.</p>
<p>As with openai_generation branch, ncludes error handling, pagination for responses over 2000 characters (Discord's limit), and prepends escape character \ to > (quote block) and / (command).</p>
<p>Requires beefy GPU for generation, though Wuerstchen is extremely fast. Resolution can be lowered to speed up generation, located in bot_controller.py under draw_image(). Max (default) res is 2048x2048.</p>
<h4>--------</h4>
<h4>video_generation</h4>
<p>Currently in development! Please feel free to contribute :) thank you.</p>
<p>-Peter</p>

<h2>Installation</h2>
<ul>
<li>Rename .env.template to .env and enter credentials between quotes. Be sure not to delete .gitignore or .env from .gitignore if pushing to repo.</li>
<li>To install the required dependencies, run the following command in project directory after cloning the repository: pip install -r requirements.txt</li>
<li>local_generation requires CUDA and CUDA-enabled <a href="https://pytorch.org/">pytorch</a>.</la>
</ul>
