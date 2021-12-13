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

function populateResults(results){
  //title, url, date captured, description, collection
  var searchContainer = document.getElementById('results');

  console.log(searchContainer);

  searchContainer.innerHTML = results[0].innerHTML;
   
}

function getSearchResults(params) {
  //'https://archive-it.org/organizations/719?q=hello&show=Sites&queryType=facets-entities'
  //https://archive-it.org/home/bac-lac?q=hello&page=1&show=Sites&queryType=facets-entities
  //https://archive-it.org/home/bac-lac?q=canada&show=Sites&collectionIds=10794&collectionIds=6602

  //TODO find the better search API, parsing html is groddy
  var reqUrl = "https://archive-it.org/home/bac-lac?show=Sites&q=" + params.get('q'); //collectionIds=
  console.log(reqUrl);
  var response = fetch(new Request(reqUrl,{mode: 'cors'}))
                 .then(response => {
                  return response.text()
                  .then(text => {
                        var parser = new DOMParser();
                        var htmlDom = parser.parseFromString(text, 'text/html');
                        var items = htmlDom.getElementsByClassName("search-results");
                        console.log(items);

                        //var results = [];

                        //items.forEach( item => {
                        //        var title = 
                        //        results.append({title: title, url: url, description: description, collection: collection});
                        //});

                        //console.log(results);

                        populateResults(items);
                  });      
                });

}


console.log("searching!");

let params = getSearchParams();

console.log(params);

let results = getSearchResults(params);

