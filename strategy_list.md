---
layout: default
---

{% for strategy in site.strategies %}
  {{ strategy.strategy_long_name }} - <img src='{{strategy.equity_curve_url}}' alt='' border=3 height=100>
{% endfor %}

table attempt ...


|EquityCurve|Metrics|
|-----------|-------|
{% for doc in site.strategies %}
  |<img src='{{doc.equity_curve_url}}' alt='' border=3 height=100>|RL: {{doc.robust_level}}<br>WFE: {{doc.wfe_ring1}}<br>NP: {{doc.backtest.metrics_all_trades.net_profit}}|
{% endfor %}