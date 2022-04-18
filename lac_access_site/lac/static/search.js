
function getSearchParams() {
  return window.location.search; 
}

function setSearchParams(params) {
  const parsedParams = new URLSearchParams(params);
  let inputs = document.getElementsByClassName('form-control');

  parsedParams.forEach((paramValue, paramKey) => {
    const input = inputs[paramKey]; 
    if(input && paramValue.length!=0){
      input.value = paramValue;
    }
  });
}

function getSearchResults(params) {
  var path = (document.documentElement.lang  == "fr") ? "/fr/search" : "/search"
  var reqUrl = path + params;
  var response = fetch(new Request(reqUrl,{mode: 'cors', headers: new Headers({"X-Requesting-Page": window.location}) }))
                 .then(response => {
                  return response.text()
                  .then(text => {
                        var searchContainer = document.getElementById('results');
                        searchContainer.innerHTML = text;
                  });      
                });

}

function validateAdvSearch() {
  let startDate = document.getElementById("startField").value;
  let endDate = document.getElementById("endField").value; 
 
  if(!!startDate && !!endDate){
    let startValue = new Date(startDate).valueOf();
    let endValue = new Date(endDate).valueOf();

    if(startValue >= endValue){
      let errorMsg=document.getElementById("s-date-error");
      errorMsg.textContent="Invalid start date | Date de début non valide";
      return false;
    }
  }
  return true;
}

var params = getSearchParams();

//console.log(params);
if (!!params.length){
  var results = getSearchResults(params);
  setSearchParams(params);
}
