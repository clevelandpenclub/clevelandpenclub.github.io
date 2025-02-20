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

{% include cle-comments.md %}
