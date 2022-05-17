def writer_bot():
    HTML = f"""
    {% extends "shared/base.html" %}

    {% block title %}
        <title>restrictapp</title>
    {% endblock %}

    {% block content %}
    <!--<div class="w3-bar w3-display-container w3-white w3-border-bottom w3-xlarge">
        <a href="#" class="w3-bar-item w3-button w3-text-red w3-hover-red"><b><i class="fa fa-map-marker w3-margin-right"></i>restrictapp</b></a>
        <a href="" class="w3-bar-item w3-button w3-right w3-hover-red w3-text-orange w3-xlarge"> login</a>
        <a href="" class="w3-bar-item w3-button w3-right w3-hover-red w3-text-orange w3-xlarge">enquiries</a>
        
    </div>-->

    <div class="container-fluid">
        <h1 class="display-4">OUTPUT</h1>
        <button class="w3-btn" onclick="document.getElementById('id01').style.display='block'">Overview</button>

        <div id="id01" class="w3-panel w3-green w3-display-container" style="display:none">
        <span onclick="this.parentElement.style.display='none'"
        class="w3-button w3-display-topright">X</span>
        <p>Click on the X to close this panel.</p>
        <p>Click on the X to close this panel.</p>
        </div>
    </div>

    {% endblock %}
    """
    with open("templates/general_pages/juggle.html", "w") as f:
        f.write(HTML)
