function addMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.className = sender + "-message";

    if (sender === "user") {
        // Mensaje del usuario
        messageDiv.textContent = "Tú: " + message;
    } else if (sender === "bot") {
        // Mensaje del bot (Nodie)
        const botResponse = document.createElement("div");

        // Prefijo con el nombre del bot
        const botName = document.createElement("strong");
        botName.textContent = "Nodie: ";
        botResponse.appendChild(botName);

        // Verifica si el mensaje incluye un enlace
        if (message.startsWith("Puedes visitar nuestro sitio web aquí:")) {
            const linkUrl = message.split(":")[1].trim();
            const linkElement = document.createElement("a");
            linkElement.href = linkUrl;
            linkElement.textContent = "Enlace";
            linkElement.target = "_blank";
            botResponse.appendChild(linkElement);
        } 
        // Verifica si incluye una imagen
        else if (message.startsWith("Aquí tienes una imagen interesante:")) {
            const imageUrl = message.split(":")[1].trim();
            const imageElement = document.createElement("img");
            imageElement.src = imageUrl;
            botResponse.appendChild(imageElement);
        } 
        // Mensaje de texto normal
        else {
            const textNode = document.createTextNode(message);
            botResponse.appendChild(textNode);
        }

        messageDiv.appendChild(botResponse);
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
