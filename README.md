
Setup:

Go install [llm](https://llm.datasette.io)!

Set up the template:
```
cp sonic-pi-script.yaml $(llm templates path)
```

Get set up for Brock (Ubuntu):
* Get sonic-pi cloned from git, `stable` branch
* Follow the BUILD-LINUX.md instructions
  * `sudo apt-get install -y build-essential git libssl-dev ruby-dev elixir erlang-dev erlang-xmerl qt6-tools-dev qt6-tools-dev-tools libqt6svg6-dev libqt6opengl6-dev supercollider-server sc3-plugins-server alsa-utils  libasound2-dev cmake ninja-build pipewire-jack libspa-0.2-jack qt6-wayland libwayland-dev libxkbcommon-dev libegl1-mesa-dev libx11-dev libxft-dev libxext-dev qpwgraph compton`
  * `cd app`
  * VCPKG is wonky, gotta use the master branch, so...
  * build with `VCPKG_BRANCH=master ./linux-build-all.sh`

Use this fork of sonic-pi-tool if you are using the latest sonic-pi, so you get the cool new OSC ports!!!!
cargo install --git https://github.com/sethwalker/sonic-pi-tool/ --force

