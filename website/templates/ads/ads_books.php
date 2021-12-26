{% if related_books %}
<div id="book-slider">
	<div class="book-slider-wrapper">
    {% for book in related_books|slice:":3" %}
	  <div class="book-slider-item">
        <table>
          <thead>
            <tr>
              <th colspan="1">
                <a href="{{ book.main_url }}">              
                {% if book.main_image%}
                <img src="{{ book.main_image.url }}" alt="" class="book-slider-img">
                {% else %}
                <img src="{{ book.image_url}}" alt=""  class="book-slider-img">
                {% endif %}
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {% if book.amazon_url %}
                <a href="{{ book.amazon_url }}"  target="_blank"type="button" class="btn_amazon">amazon</a>
                {% endif %}
                {% if book.rakuten_url %}
                <a href="{{ book.rakuten_url }}"  target="_blank"type="button" class="btn_rakuten">楽天</a>
                {% endif %} 
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      {% endfor %}
	</div>
</div>

{% else %}
   {% include 'ads/ads_vert.php' %}
{% endif %}