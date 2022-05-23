---
layout: default
---

{% for strategy in site.strategies %}
  {{ strategy.strategy_long_name }} - <img src='{{strategy.equity_curve_url}}' alt='' border=3 height=100>
{% endfor %}
