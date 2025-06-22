async function askQuestion() {
    const question = document.getElementById("question").value;
    const responseDiv = document.getElementById("response");
    responseDiv.innerText = "Loading...";

    const res = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await res.json();
    responseDiv.innerText = data.answer || data.error;
}
