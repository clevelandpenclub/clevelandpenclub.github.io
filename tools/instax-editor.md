<iframe src="instaxeditor/index.html" class="instaxframe"></iframe>

<div class="mobilemessage" hidden>Sorry sweetie, this page doesn't support mobile browsers. Try using your desktop or laptop computer, or ask your local Amelorate for help! If you ask nicely enough she'll probably make it support your phone.</div>

<style>
.instaxframe {
    width: 100%;
    height: 500px;
    display: block;
}

.mobilemessage {
    text-align: center;
    padding = 20px;
    font-size: 18px;
    font-weight: bold;
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

        const message = document.querySelector(".mobilemessage");
        if (message) {
            message.hidden = false;
        }
    }
});
</script>
