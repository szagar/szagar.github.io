---
layout: default
title: 'Test Coll'
permalink: /test_coll/
---

{% for pg in site.test_collections %}
  <h2>
    <a href="{{ pg.baseurl }}{{ pg.url }}">
      {{ pg.name }} - {{ pg.title }} ({{pg.baseurl}}) ({{pg.url}})
    </a>
  </h2>
  <p>{{ pg.content | markdownify }}</p>
{% endfor %}
