---
title: Sophants
---

To state the obvious, I'm not using anyone's real names or faces. 

{% include gallery.css.html %}

<div class="gallery">
  {% for item in site.data.sophants %}
  <div class="item">
    <img src="{{ item.src }}" alt="{{ item.alt }}" width="250" />
    <p>{{ item.description | markdownify }}</p>
  </div>
  {% endfor %}
</div>


* Sophant: An entity with a human-level level intelligence

{% include cle-comments.md %}
