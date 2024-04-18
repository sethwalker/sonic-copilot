# system.txt is stored as a template for llm
# also note, had to patch sonic-pi-tool to send to the right port
# which updated recently in sonic pi and is not configurable in sonic pi GUI.

cat prompt.txt | llm -t sonic-pi-script | tee script.rb | sonic-pi-tool eval-stdin
