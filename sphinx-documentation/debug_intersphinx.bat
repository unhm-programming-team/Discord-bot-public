echo Checking Relative

python -msphinx.ext.intersphinx "https://pillow.readthedocs.io/en/stable/objects.inv" > debug_pillow.txt
python -msphinx.ext.intersphinx "https://discordpy.readthedocs.io/en/stable/objects.inv" > debug_discord.txt