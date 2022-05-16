---
layout: default
---

{% for pg in site.test_collections %}
  <h2>
    <a href="{{ pg.baseurl }}{{ pg.url }}">
      {{ pg.name }} - {{ pg.title }} ({{pg.baseurl}}) ({{pg.url}})
    </a>
  </h2>
  <p>{{ pg.content | markdownify }}</p>
{% endfor %}

#permalink: /test_coll/
#title: 'Test Coll'