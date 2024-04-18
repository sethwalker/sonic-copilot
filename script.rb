# Sonic Pi code to create a four on the floor bass drum with slightly swung double tap high hat on the 2s and 4s
# Minimum Sonic Pi version required: v2.0

# This Sonic Pi script continually plays a simple bass drum beat with slightly swung double tap high hat
# Four on the floor means we'll hear the bass drum on every count - four beats per measure

# Let's define the beat
live_loop :bass_drum do
  # The :bd_haus sample represents a bass drum sound
  sample :bd_haus
  # We'll sleep for 1 beat between drum hits
  # This value can be adjusted for faster/slower tempos
  sleep 1
end

live_loop :high_hat, sync: :bass_drum do
  # The :drum_cymbal_pedal sample represents a high hat sound
  # Code to create a slightly swung double tap high hat effect on beats 2 and 4
  sleep 1
  sample :drum_cymbal_pedal
  sleep 0.5
  sample :drum_cymbal_pedal
  sleep 0.5
  sample :drum_cymbal_pedal
  sleep 2
end
