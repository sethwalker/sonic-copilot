live_loop :listen do
  use_real_time
  name, script = sync "/osc:127.0.0.1:*/run-code"
  
  puts "we got: ", name, script
  
  eval script
end
