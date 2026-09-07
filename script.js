const message = document.getElementById("message");
const count = document.getElementById("count");
const btn = document.getElementById("detectBtn");

message.addEventListener("input", () => count.textContent = message.value.length);

function fillExample(text){
    message.value = text;
    count.textContent = text.length;
    message.focus();
}

btn.addEventListener("click", async () => {
    const text = message.value.trim();
    if(!text){
        alert("Please enter a message first.");
        return;
    }

    btn.disabled = true;
    btn.textContent = "⏳ Analyzing...";

    try{
        const response = await fetch("/predict", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({text})
        });
        const data = await response.json();

        document.getElementById("resultLabel").textContent = data.label;
        document.getElementById("resultReason").textContent = data.reason;
        document.getElementById("confidenceText").textContent = data.confidence + "%";
        document.getElementById("progressBar").style.width = data.confidence + "%";

        const icon = document.getElementById("resultIcon");
        icon.textContent = data.label === "Normal" ? "✅" :
                           data.label === "Spam" ? "🚨" : "⚠️";

        document.getElementById("tip").textContent =
            data.label === "Normal"
            ? "✅ This message looks normal based on the demo rules."
            : data.label === "Spam"
            ? "🚨 Avoid unknown links, prize claims, and suspicious offers."
            : "⚠️ If someone is being targeted online, save evidence and tell a trusted adult or responsible authority.";
    }catch(error){
        alert("Server error. Make sure Flask is running.");
    }finally{
        btn.disabled = false;
        btn.textContent = "🔍 Detect Message";
    }
});
