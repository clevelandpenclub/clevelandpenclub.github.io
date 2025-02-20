---
title: Specimines
---

These aren't actually for sale or anything, these are just pens I wanted to show off.

{% include gallery.css.html %}

<div class="gallery">
  {% for item in site.data.specimines %}
  <div class="item">
    <img src="{{ item.src }}" alt="{{ item.alt }}" width="250" />
    <p>{{ item.description | markdownify }}</p>
  </div>
  {% endfor %}
</div>

<script src="https://giscus.app/client.js"
        data-repo="clevelandpenclub/clevelandpenclub.github.io"
        data-repo-id="R_kgDONeh5oQ"
        data-category="Announcements"
        data-category-id="DIC_kwDONeh5oc4Cl6ba"
        data-mapping="pathname"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
