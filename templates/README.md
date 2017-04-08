{% for note in notes %}
[{{ note.text }}]({{ note.url }})
{% endfor %}