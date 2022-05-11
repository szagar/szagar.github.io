---
layout: default
---

{% for pg in site.test_collections %}
  <h2>
    <a href="{{ pg.baseurl }}{{ pg.url }}">
      {{ pg.name }} - {{ pg.title }}
    </a>
  </h2>
  <p>{{ pg.content | markdownify }}</p>
{% endfor %}
