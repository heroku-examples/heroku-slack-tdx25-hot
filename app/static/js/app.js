document.getElementById("feedButton").addEventListener("click", function() {
    fetch("/feed", { method: "POST" })
        .then(response => response.json())
        .then(data => updatePage(data));
});

document.getElementById("waterButton").addEventListener("click", function() {
    fetch("/water", { method: "POST" })
        .then(response => response.json())
        .then(data => updatePage(data));
});

document.getElementById("moveButton").addEventListener("click", function() {
    fetch("/move", { method: "POST" })
        .then(response => response.json())
        .then(data => updatePage(data));
});

document.getElementById("vetButton").addEventListener("click", function() {
    fetch("/vet", { method: "POST" })
        .then(response => response.json())
        .then(data => updatePage(data));
});

function updatePage(data) {
    document.querySelector("p:nth-child(2)").textContent = `Location: ${data.location}`;
    document.querySelector("p:nth-child(3)").textContent = `Health Status: ${data.health_status}`;
    document.querySelector("p:nth-child(4)").textContent = `Feed Percentage: ${data.feed_percentage}%`;
    document.querySelector("p:nth-child(5)").textContent = `Water Percentage: ${data.water_percentage}%`;
}

