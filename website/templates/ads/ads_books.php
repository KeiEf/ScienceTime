{% if related_books %}
<div id="book-slider">
	<div class="book-slider-wrapper">
    {% for book in related_books|slice:":6" %}
	  <div class="book-slider-item">
        <table>
          <thead>
            <tr>
              <th colspan="1">
                <button onclick="api_click(value,id)" id="{{ book.main_url }}" value = "{% url 'api_click' book.pk %}">
                {% if book.main_image%}
                <img src="{{ book.main_image.url }}" alt="" class="book-slider-img">
                {% else %}
                <img src="{{ book.image_url}}" alt=""  class="book-slider-img">
                {% endif %}
                </button>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {% if book.amazon_url %}
                <button onclick="api_click(value,id)" id="{{ book.main_url }}" value = "{% url 'api_click' book.pk %}" type="button" class="btn_amazon">amazon</button>
                {% endif %}
                {% if book.rakuten_url %}
                <button onclick="api_click(value,id)" id="{{ book.main_url }}" value = "{% url 'api_click' book.pk %}" type="button" class="btn_rakuten">楽天</button>
                {% endif %} 
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      {% endfor %}
	</div>
</div>

<script>
  function api_click(value,id) {
    var api_url = value
    var request = new XMLHttpRequest();
    request.open("GET",api_url);
    request.send();
    open(id, "_blank" );
    }
</script>

{% else %}
   {% include 'ads/ads_vert.php' %}
{% endif %}