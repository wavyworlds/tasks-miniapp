document.addEventListener("DOMContentLoaded", () => {
    let currentTask = 0;
    const videoLinks = [
        "https://youtube.com/shorts/v0vNYgGxg0w?feature=share",
        "https://youtube.com/shorts/ew6Zxy1Amsw?feature=share",
        "https://youtube.com/shorts/d6Cut_VS5wc?feature=share",
        "https://youtu.be/QHUqTNNDduI",
        "https://youtu.be/ocoAJvXIfe8"
    ];

    function loadTask() {
        if (currentTask < videoLinks.length) {
            document.getElementById("videoFrame").src = videoLinks[currentTask];
            document.getElementById("taskText").innerText = `Task ${currentTask + 1} of ${videoLinks.length}`;
        } else {
            document.getElementById("taskText").innerText = "All tasks completed!";
            document.getElementById("completeBtn").style.display = "none";
        }
    }

    document.getElementById("completeBtn").addEventListener("click", () => {
        if (document.getElementById("videoFrame").src.includes("youtu")) {
            currentTask++;
            loadTask();
        } else {
            alert("Please watch the video before completing the task!");
        }
    });

    loadTask();
});
