
function getSearchParams() {
  return window.location.search; 
}

function getSearchResults(params) {
  var path = (document.documentElement.lang  == "fr") ? "/fr/search" : "/search"
  var reqUrl = path + params;
  console.log(reqUrl);
  var response = fetch(new Request(reqUrl,{mode: 'cors', headers: new Headers({"X-Requesting-Page": window.location}) }))
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
if (!!params.length){
  var results = getSearchResults(params);
}

