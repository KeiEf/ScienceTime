{% load static %}

<!-- popular posts-->
<div class="col-lg-4 col-md-4 col-sm-4">
          <aside class="right_content">
            <div class="single_sidebar">
              <h2><span>Popular Posts</span></h2>
              <ul class="spost_nav">
                {% for post in popular_list|slice:":4" %}
                <li>
                  <div class="media wow fadeInDown">             
                    <a href="{% url 'post_detail' post.pk %}" class="media-left">              
                      {% if post.main_image%}
                        <img src="{{ post.main_image }}" alt="">
                      {% else %}
                        <img src="{{ post.image_url}}" alt="">
                      {% endif %}
                    </a>
                    <div class="media-body">
                      <a href="{% url 'post_detail' post.pk %}" class="catg_title">{{ post.title }}
                      </a>
                    </div>
                  </div>
                </li>
                {% endfor %}
              </ul>
            </div>

            <!-- popular items-->
            <div class="single_sidebar">
              <h2><span>Popular Items</span></h2>
              <ul class="spost_nav">
                {% for post in popular_items|slice:":4" %}
                <li>
                  <div class="media wow fadeInDown">             
                  <a href="{% url 'product_detail' post.pk %}" class="media-left">              
                    {% if post.main_image%}
                      <img src="{{ post.main_image }}" alt="">
                    {% else %}
                      <img src="{{ post.image_url}}" alt="">
                    {% endif %}
                  </a>
                    <div class="media-body">
                      <a href="{% url 'product_detail' post.pk %}" class="catg_title">{{ post.name }}
                      </a>
                    </div>
                  </div>
                </li>
                {% endfor %}
              </ul>
            </div>            

          <!-- ads -->
          <div class="single_sidebar wow fadeInDown">
            <h2><span>Sponsor</span></h2>
            {% include 'ads/ads1.php' %}
          </div>
          <!-- category -->
          <div class="single_sidebar wow fadeInDown">
            <h2><span>Category Archive</span></h2>
            <select class="catgArchive" onChange="location.href=value;">
              <option>Select Category</option>
              {% for item in cat_menu %}              
              <option value="{% url 'category' item|slugify %}">{{ item }}</option>
              {% endfor %}
            </select>
          </div>
          </aside>
        </div>