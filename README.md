# module_bob
## Installation
``` bash
cd modules
git clone https://github.com/turboteun2/module_bob.git
cd module_bob
npm install socket.io-client
npm install -g sass
pip3 install flask flask-socketio ollama
```

## *Optional:* Autostart Python3 file.
File: `package.json`
```json
"scripts": 
{ 
	"start": "concurrently \"npm run start:mirror\" \"npm run start:python\"",
	"start:mirror": "DISPLAY=:0 ./node_modules/.bin/electron js/electron.js", "start:python",
	"start:python": "python modules/MyModule/server.py"
},
```
