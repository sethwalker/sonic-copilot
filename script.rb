# Sonic Pi code to create a house drums with electro funk bass groove
# Minimum Sonic Pi version required: v2.0

use_bpm 120

# This Sonic Pi script plays a house drum pattern over 12 bars 
# along with an electro funk bass groove.

# Let's define the house drums
live_loop :drums do
  # The :bd_tek sample represents a bass drum sound, :sn_dolf for snare
  sample :bd_tek
  sleep 0.5
  sample :bd_tek
  sleep 1
  sample :sn_dolf
  sleep 0.5
end

# Let's define the electro funk bass groove
live_loop :bass_groove do
  use_synth :prophet
  play :e1, release: 0.6
  sleep 0.75
  play :g1, release: 0.5
  sleep 0.25
  play :a1, release: 0.8
  sleep 0.5
  play :b1, release: 0.5
  sleep 1
end

