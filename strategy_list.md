---
layout: default
---

{% for strategy in site.strategies %}
  {{strategy}}
  <h3>{{strategy.market}}: {{ strategy.name }} - {{ strategy.strategy_long_name }} - {{strategy.utl}}</h3>
{% endfor %}
