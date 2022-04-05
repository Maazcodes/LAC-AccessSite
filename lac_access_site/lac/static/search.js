
function getSearchParams() {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  var params = new Map();
  if (vars[0]!="") {
    for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split("=");
      params.set(pair[0],decodeURIComponent(pair[1].replace(/\+/g, "%20")));
    }
  }

  // for case with no params
  if (!params.size) {
      var searchContainer = document.getElementById('results');
      searchContainer.innerHTML = "";
  }
  return params;
}

function getSearchResults(params) {
  var path = (document.documentElement.lang  == "fr") ? "/fr/search" : "/search"
  // TODO maybe just pass these along more directly?
  var reqUrl = path + "?q=" + params.get('q') + "&i=" + params.get('i')
                + (params.has("nq") ? "&nq=" + params.get("nq"):"") 
                + (params.has("exact") ? "&exact=" + params.get("exact"):"") 
                + (params.has("site") ? "&site=" + params.get("site"):"") 
                + (params.has("filetype") ? "&filetype=" + params.get("filetype"):"") 
                + (params.has("start") ? "&start=" + params.get("start"):"") 
                + (params.has("end") ? "&end=" + params.get("end"):"");
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
if (!!params.size){
  var results = getSearchResults(params);
}

