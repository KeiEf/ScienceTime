<input type="checkbox" id="pop-up">
       <div class="overlay">
         <div class="window">
           <label class="close" for="pop-up">×</label>
    
           <div class="frame_left">
             <h4>画像挿入</h4>   
             <iframe src="{% url 'image_upload' %}"></iframe>
           </div>
             
         </div>
       </div> 
       <br/>
