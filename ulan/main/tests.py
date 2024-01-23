< form name = "myForm" action = "{% url 'createdata' %}" method = "POST" > { % csrf_token %}
<div class="row">
    <div class="col">
            <select name="article" class="form-control" required >
                <option selected>Выбирайте...</option>
                {% for article in articles %}
                <option value="{{ article.id }}" >{{ article.name }}</option>
                {% endfor %}
            </select>
        <div class="invalid-feedback">Пример обратной связи неверного выбора </div>

    </div>
        {{ work_stations.work_station|title }}
    <input type="hidden" name="work_stations" value="{{ work_stations.id }}">
    <div class="col">
        <label  class="form-label" ></label>
        <input type="hidden" class="form-control" name="category" value="{{ work_stations.category_id }}">


    </div>
    <div class="col">
        <label  class="form-label" >{{ work_stations.category }}</label>
        <input type="text" class="form-control" placeholder="Количество" aria-label="" name="quantity">

    </div>
    <div class="col">
        <input type="text" class="form-control" placeholder="Примечение" aria-label="" name="description">
    </div>
    <div class="col">
        <input type="text" class="form-control" placeholder="Брак" aria-label="last name" name="brak">
    </div>
        <div class="col">

    </div>
</div>
<input type="submit">
            </form>