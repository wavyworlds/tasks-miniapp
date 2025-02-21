const videos = [
    "https://www.youtube.com/embed/QHUqTNNDduI?enablejsapi=1",
    "https://www.youtube.com/embed/ocoAJvXIfe8?enablejsapi=1",
    "https://www.youtube.com/embed/v0vNYgGxg0?enablejsapi=1",
    "https://www.youtube.com/embed/ew6Zxy1Amsw?enablejsapi=1",
    "https://www.youtube.com/embed/d6Cut_VS5wc?enablejsapi=1"
];

let currentTask = 0;
let player;
let videoWatched = false; // Track if user has watched the video

// Load YouTube IFrame API
function onYouTubeIframeAPIReady() {
    player = new YT.Player("youtube-video", {
        events: {
            "onStateChange": onPlayerStateChange
        }
    });
}

// When video ends, enable the complete button
function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.ENDED) {
        videoWatched = true;
        document.getElementById("complete-task").disabled = false;
    }
}

// Load a new task
function loadTask() {
    if (currentTask < videos.length) {
        document.getElementById("youtube-video").src = videos[currentTask];
        document.getElementById("complete-task").disabled = true;
        document.getElementById("next-task").style.display = "none";
        videoWatched = false;
    } else {
        document.body.innerHTML = "<h2>🎉 All tasks completed! 🎉</h2>";
    }
}

// Send completion to Telegram bot
async function notifyBot() {
    const botToken = "7532214010:AAGuuMOa2G708Ah4O3uhkgS0KaTwgR5TaEs";
    const chatId = "USER_TELEGRAM_CHAT_ID"; // Replace with actual user chat ID
    const message = `User has completed task ${currentTask + 1}`;

    await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text: message })
    });
}

// Handle task completion
document.getElementById("complete-task").addEventListener("click", async () => {
    if (!videoWatched) {
        alert("⚠ You must watch the full video before completing the task!");
        return;
    }

    await notifyBot();
    document.getElementById("complete-task").style.display = "none";
    document.getElementById("next-task").style.display = "inline-block";
});

// Load next task
document.getElementById("next-task").addEventListener("click", () => {
    currentTask++;
    document.getElementById("complete-task").style.display = "inline-block";
    loadTask();
});

loadTask();
