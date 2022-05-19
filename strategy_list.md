---
layout: default
---

{% for strategy in site.strategies %}
  <h2>{{strategy.market}}: {{ strategy.name }} - {{ strategy.strategy_name }} - {{ strategy.strategy_long_name }}</h2>
{% endfor %}
