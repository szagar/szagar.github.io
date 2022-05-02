note: finds static files anywhere, doesn't have to be in assetss
{% for file in site.static_files %}
  {% if file.image %}
    <img src="{{file.path}}" alt="{file.name}">
  {% else %}
    { file.path }}
  {% endif %}
{% endfor %}
