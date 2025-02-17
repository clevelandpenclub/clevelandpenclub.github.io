<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post Creator</title>
    <script>
        function updateInfoBox() {
            const titleInput = document.getElementById("title").value;
            const infoBox = document.getElementById("info-box");
            const preambleText = document.getElementById("preamble-text");
            
            const cleanTitle = titleInput.replace(/[^a-zA-Z0-9\s-]/g, "").replace(/\s+/g, "-");
            const hasIllegalChars = titleInput !== cleanTitle.replace(/-/g, " ");
            
            preambleText.value = `---\ntitle: ${titleInput || "Title Goes Here!"}\n---`;
            infoBox.style.display = hasIllegalChars ? "block" : "none";
        }

        function copyToClipboard() {
            const preambleText = document.getElementById("preamble-text");
            preambleText.select();
            preambleText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Preamble copied to clipboard!");
        }

        function generatePostLink() {
            const titleInput = document.getElementById("title").value;
            const dateInput = document.getElementById("date").value;

            if (!titleInput || !dateInput) {
                alert("Please enter both a title and a date.");
                return;
            }

            const date = new Date(dateInput);
            const today = new Date();
            
            if (date > today) {
                alert("The date cannot be in the future.");
                return;
            }
            
            const formattedDate = `${date.getFullYear()}-${(`0${date.getMonth() + 1}`).slice(-2)}-${(`0${date.getDate()}`).slice(-2)}`;
            
            const cleanTitle = titleInput.replace(/[^a-zA-Z0-9\s-]/g, "").replace(/\s+/g, "-");
            
            const fileName = `${formattedDate}-${cleanTitle}.md`;
            const githubUrl = `https://github.com/clevelandpenclub/clevelandpenclub.github.io/new/main/_posts?filename=${fileName}`;
            
            window.open(githubUrl, "_blank");
        }
    </script>
</head>
<body>
    <h1>Jekyll Post Creator</h1>
    <label for="title">Post Title:</label>
    <input type="text" id="title" placeholder="Enter post title" required oninput="updateInfoBox()">
    <br>
    <label for="date">Post Date:</label>
    <input type="date" id="date" required><script>document.getElementById('date').valueAsDate = new Date();</script>
    <br>
    <button onclick="generatePostLink()">Next</button>
    
    <div id="info-box" style="display: none; margin-top: 20px; padding: 10px; border: 1px solid #ccc; background: #f9f9f9;">
        <p>You'll need to paste the following at the beginning of your article:</p>
        <textarea id="preamble-text" readonly style="width: 100%; height: 60px;">---
title: Title Goes Here!
---</textarea>
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
    </div>
</body>
</html>
