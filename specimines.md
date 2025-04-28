---
title: Specimines
---

These aren't actually for sale or anything, these are just pens I wanted to show off.

Some pictures have a HD version. Click or tap on the image to load it in HD!

{% include gallery.css.html %}

<div class="gallery">
  {% for item in site.data.specimines %}
  <div class="item">
    <img 
      src="{{ item.src }}" 
      alt="{{ item.alt }}" 
      width="250" 
      data-hd="{{ item.hd | default: '' }}" 
      onclick="upgradeToHD(this)" 
    />
    <p>{{ item.description | markdownify }}</p>
  </div>
  {% endfor %}
</div>

<script>
function upgradeToHD(img) {
  const hdSrc = img.dataset.hd;
  if (hdSrc) {
    img.src = hdSrc;
    img.removeAttribute('onclick'); // Optional: prevent re-clicking
  }
}
</script>

{% include cle-comments.md %}
