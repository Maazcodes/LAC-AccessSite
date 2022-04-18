//get the dom nodes we want to manipulate
function parseList() {
    let list = document.getElementById("seed-list");
    return Array.from(list.children);
}

//helper function. divide list based on pagination vars
function paginateList(flatList) {
    let start = perPage * (currentPage-1);
    return flatList.slice(start, start+perPage);
}

//repopulate list element given an Array of li-like nodes
function redrawList(currentElements) {
    let list = document.getElementById("seed-list");
    let drawElements = paginateList(currentElements);
    //console.log(drawElements);
    list.innerHTML = drawElements.map(element => element.innerHTML).reduce((prev, curr)=> prev + '\n' + curr, "");

    updateStats();
    return;
}

//filter list based on form data
function filterList() {
    let inclEng = document.getElementById("english-checkbox").checked;
    let inclFr = document.getElementById("french-checkbox").checked;
    let inclTopic = document.getElementById("topic-select").value;
    let inclKeyword = document.getElementById("keyword-search").value;

    filterElements = listElements;

    //filter topic
    if(inclTopic){
        filterElements = filterElements.filter((div) => div.querySelector("[name=subj-item]").childNodes[1].textContent.includes(inclTopic));
    }

    //filter language
    if(inclEng && !inclFr ){
        filterElements = filterElements.filter((div) => {
                return (div.querySelector("[name=lang-item]").childNodes[1].textContent == "EN") ||
                (div.querySelector("[name=lang-item]").childNodes[1].textContent == "AN");
        });
    }
    if(inclFr&& !inclEng ){
        filterElements = filterElements.filter((div) => {
                return div.querySelector("[name=lang-item]").childNodes[1].textContent == "FR";
        });
    }

    if(inclKeyword){
        filterElements = filterElements.filter((div) => div.textContent.includes(inclKeyword));
    }
    filterLen = filterElements.length;
    redrawList(filterElements);
}

//TODO setup event listeners
function pageList(modifier) {
    let numPages = filterElements.length / perPage;
    if(((currentPage + modifier) <= Math.ceil(numPages)) && ((currentPage + modifier) > 0)) {
        currentPage = currentPage + modifier;
        redrawList(filterElements);
    }
}
//TODO draw pagination buttons based on list length, current vars
function sortList(fieldName) {
    let filterFunc = (e1,e2) => { 
            let v1 = e1.querySelector(`[name=${fieldName}`).childNodes[1].textContent;
            let v2 = e2.querySelector(`[name=${fieldName}`).childNodes[1].textContent;

            if(v1 > v2) { return 1;}
            else if(v1 < v2) { return -1;}
            else {return 0;}

    };

    filterElements.sort(filterFunc);
    listElements.sort(filterFunc);

    //redraw
    redrawList(filterElements);
}

function updateStats(){
     stats[0].textContent = statsCopy.replace("<>", filterElements.length).replace("<>", listElements.length);
     stats[2].textContent = pageCopy.replace("<>", currentPage).replace("<>",perPage);
}

function resetList(){
    filterElements = listElements;
    currentPage = 1;
    redrawList(filterElements);
}

// state for filtering
let listElements = parseList();
let filterElements = listElements;

//state for pagination 
let perPage = 50;
let currentPage = 1;

//state for stats display on top of list
let stats = document.getElementById("list-stats").childNodes;
let statsCopy = stats[0].textContent;
let pageCopy = stats[2].textContent;
updateStats();
