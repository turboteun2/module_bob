Module.register("MyModule", {
    defaults: {
        pythonServer: "http://localhost:5001" // URL van de Python-server
    },

    start: function () {
        this.text = ""; // Opslag voor ontvangen tekst

        // Verbind met de WebSocket-server
        this.setupSocketConnection();
    },

    getDom: function () {
        var wrapper = document.createElement("div");

        // Input veld en knop
        var input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Typ een bericht...";
        input.id = "myInput";

        var button = document.createElement("button");
        button.innerHTML = "Verstuur";
        button.onclick = () => {
            var text = input.value;
            this.sendTextToServer(text);
        };

        // H1 veld om de ontvangen tekst te tonen
        var received = document.createElement("h1");
        received.id = "receivedText";
        received.innerHTML = this.text;

        wrapper.appendChild(input);
        wrapper.appendChild(button);
        wrapper.appendChild(received);

        return wrapper;
    },

    sendTextToServer: function (text) {
        fetch(`${this.config.pythonServer}/send`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        }).then(response => {
            console.log("Bericht verzonden:", text);
        });
    },

    setupSocketConnection: function () {
        // Verbind met de Python WebSocket-server
        var socket = io(this.config.pythonServer);

        // Luister naar de "update_text" gebeurtenis
        socket.on("update_text", (data) => {
            this.text = data.text;
            document.getElementById("receivedText").innerHTML = this.text;
            console.log("Nieuw bericht ontvangen:", this.text);
        });
    }
});
