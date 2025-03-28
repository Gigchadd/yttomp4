document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("download-btn").addEventListener("click", downloadVideo);
});

function downloadVideo() {
    const url = document.getElementById("video-url").value;

    if (!url) {
        alert("Please enter a YouTube URL");
        return;
    }

    document.getElementById("status").textContent = "Processing...";

    fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.download_link) {
            document.getElementById("status").textContent = "Download Ready:";
            document.getElementById("download-link").innerHTML =
                `<a href="${data.download_link}" download>Click here to download</a>`;
            document.getElementById("download-link").style.display = "block";
        } else {
            document.getElementById("status").textContent = "Error: " + (data.error || "Unknown error");
        }
    })
    .catch(error => {
        document.getElementById("status").textContent = "Error: " + error.message;
    });
}
