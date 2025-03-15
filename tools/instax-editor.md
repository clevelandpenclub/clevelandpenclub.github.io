<iframe src="instaxeditor/index.html" class="instaxframe"></iframe>

<style>
.instaxframe {
    width: 100%;
    height: 500px;
    display: block;
}
</style>

<script>
document.addEventListener("DOMContentLoaded", function () {
    function isMobile() {
        return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    }

    if (isMobile()) {
        const iframe = document.querySelector(".instaxframe");
        if (iframe) {
            iframe.remove(); // Remove the iframe
        }

        const message = document.createElement("div");
        message.textContent = "Sorry sweetie, this page doesn't support mobile browsers. Try using your desktop or laptop computer, or ask your local Amelorate for help! If you ask nicely enough she'll probably make it support your phone.";
        message.style.textAlign = "center";
        message.style.padding = "20px";
        message.style.fontSize = "18px";
        message.style.fontWeight = "bold";

        document.body.appendChild(message);
    }
});
</script>
