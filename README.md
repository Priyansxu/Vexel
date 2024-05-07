<h3>Commands:</h3>
<ul>
<li>!ask ___</li>
<li>!ask prompt ___</li>
<li>!draw ___</li>
<li>!edit ___ [attach image file]</li>
<li>[Draw] button attached to each image response to easily generate another image based on the same prompt.</li>
<li>Example: [send message] !ask prompt cat chasing a dog. [bot responds] Vibrant and playful scene of a mischievous cat chasing a startled dog through a sun-kissed park. Capture the cat mid-leap, with its claws outstretched, and the dog with a comical expression of surprise and determination. Bring the charming chaos to life with dynamic shadows and animated foliage. [Draw]</li>
<li>Draw button works until the message's timeout, 10-15 minutes (or bot restart).</li>
</ul>

<h4>Legend:</h4>
<ul>
<li>___ is your prompt</li>
<li>Text between [ and ] is an action, excepting [Draw], which is a GUI button provided by discord.py (and technically an action).</li>
</ul>
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
<h4>local_video</h4>
<p>Currently in development! Please feel free to contribute :) thank you.</p>
<p>-Peter</p>

<h2>Installation</h2>
<ul>
<li>Rename .env.template to .env and enter credentials between quotes. Be sure not to delete .gitignore or .env from .gitignore if pushing to repo.</li>
<li>To install the required dependencies, run the following command in project directory after cloning the repository: pip install -r requirements.txt</li>
<li>local_generation requires CUDA and CUDA-enabled <a href="https://pytorch.org/">pytorch</a>.</la>
</ul>
