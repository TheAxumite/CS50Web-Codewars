

//array buffer binarytype is potentionally more efficent
// socket.binaryType = 'arraybuffer';
//  socket.binaryType = 'blob'

// //connection opened
// socket.addEventListener("open", function event() {socket.send("Hello Server!");});

// //listen for messages
// socket.addEventListener("message", (event) => {console.log("Message from server", event.data)})

// Send text to all users through the server
//socket.addEventListener("open", function event() {socket.send("Hello Server!");});
// Create WebSocket connection.
const socket = new WebSocket('ws://127.0.0.1:8000/ws/')

// Connection opened
socket.addEventListener("open", (event) => {
  socket.send("Hello Server!");
});

socket.addEventListener("error", (event) => {
    console.log("WebSocket error: ", event);
  });
function sendText() {
    // Construct a msg object containing the data the server needs to process the message from the chat client.
    const clientID =  document.getElementById("username").innerHTML
    const msg = {
        type: "message",
        text: document.getElementById("message-collector").value,
        id: clientID,
        date: Date.now(),
    };

    // Send the msg object as a JSON-formatted string.
    socket.send(JSON.stringify(msg));

    // Blank the text input element, ready to receive the next line of text from the user.
    document.getElementById("message-collector").value = "";
}

socket.onmessage = (event) => {
    console.log(event.data);
  };
  