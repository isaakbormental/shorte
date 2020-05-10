function handleGenerateLink() {
    let xmlHttp = new XMLHttpRequest();
    let url = document.getElementsByClassName('input-field')[0].value;
    xmlHttp.open("POST", 'http://localhost/full-url', true);
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200)
            // alert("Requst done");
            // console.log(xmlHttp.response)
            document.getElementsByClassName('output-url')[0].innerText = xmlHttp.response;
    }
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    let data = JSON.stringify({'fullUrl': url});
    xmlHttp.send(data);
}