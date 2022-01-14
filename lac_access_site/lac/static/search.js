function getSearchParams() {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  var params = new Map();
  for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split("=");
      params.set(pair[0],decodeURIComponent(pair[1].replace(/\+/g, "%20")));
  }
  return params;
}

function getSearchResults(params) {
  var reqUrl = "/search?q=" + params.get('q') + "&i=" + params.get('i'); 
  console.log(reqUrl);
  var response = fetch(new Request(reqUrl,{mode: 'cors'}))
                 .then(response => {
                  return response.text()
                  .then(text => {
                        //console.log(text);
                        /*var parser = new DOMParser();
                        var htmlDom = parser.parseFromString(text, 'text/html');
                        var items = htmlDom.getElementsByClassName("search-results");
                        console.log(items);
                        populateResults(items);*/

                        var searchContainer = document.getElementById('results');
                        searchContainer.innerHTML = text;
                  });      
                });

}

var params = getSearchParams();

//console.log(params);

var results = getSearchResults(params);

