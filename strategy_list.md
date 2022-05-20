---
layout: default
---

{% for strategy in site.strategies %}
  <h3>{{strategy.market}}: {{ strategy.strategy_name }} - {{ strategy.strategy_long_name }} - {{strategy.utl}}</h3>
{% endfor %}
