const socket = new WebSocket("ws://localhost:8080", protocols)

//array buffer binarytype is potentionally more efficent
// socket.binaryType = 'arraybuffer';
socket.binaryType = 'blob'

//connection opened
socket.addEventListener("open", function event() {socket.send("Hello Server!");});

//listen for messages
socket.addEventListener("message", (event) => {console.log("Message from server", event.data)})
