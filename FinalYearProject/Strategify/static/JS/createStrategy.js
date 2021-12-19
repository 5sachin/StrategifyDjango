let suggestions = ["ITC.NS","RELIANCE.NS","SBIN.NS","TCS","LTI.NS","TATAMOTORS.NS","ABCAPITAL.NS","AJANTPHARM.NS","AMBUJACEM.NS","ATGL.NS","ADANIGREEN.NS","ADANITRANS.NS","MRF.NS","HDFC.NS","YESBANK.NS","ADANIENT.NS","TITAN.NS","BHARTIARTL.NS","TATASTEEL.NS","INFY.NS"];

const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");

inputBox.onkeyup = (e)=>{
    let userData = e.target.value;
    let emptyArray = [];
    if(userData){
        emptyArray = suggestions.filter((data)=>{
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data)=>{
            return data = `<li>${data}</li>`;
        });
        searchWrapper.classList.add("active");

        showSuggestions(emptyArray);
        let allList = suggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            allList[i].setAttribute("name", "this.innerText");
            allList[i].setAttribute("onclick", "addScripName(this.innerText)");
        }
    }else{
        searchWrapper.classList.remove("active");
    }
}

let scripList = [];
var scripAddedContainer = document.querySelector(".addedscripList");
function addScripName(element){

    var scripAddedName = document.createElement("a");
    scripAddedName.setAttribute("class","btn");
    scripAddedName.setAttribute("name",element);
    scripAddedName.setAttribute("value",element);
    scripAddedName.setAttribute("id",element);
    scripAddedName.innerHTML = element;

    inputBox.value ="";
    var span = document.createElement('span');
    span.setAttribute("class","removeAddedScripName");
    span.setAttribute("onclick","cancel('" + element + "')");
    span.innerHTML = '&times';
    scripAddedName.append(span);
    scripAddedContainer.append(scripAddedName);
    searchWrapper.classList.remove("active");
    scripList.push(element);

    let v = ""

    for(let i = 0;i<scripList.length;i++){
        v += scripList[i]+",";
    }

    let x = document.getElementById('allscriplist');
    x.value = v;
    x.innerHTML = v;
}

function showSuggestions(list){
    let listData;
    if(!list.length){
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    suggBox.innerHTML = listData;
}


function cancel(val){
    var parent = document.getElementById('autocom-box');
    var child = document.getElementById(val);
    child.remove(parent);
    var index = scripList.indexOf(val);
    if (index !== -1) {
      scripList.splice(index, 1);
    }
    let v = "";
    for(let i = 0;i<scripList.length;i++){
        v += scripList[i]+",";
    }

    let x = document.getElementById('allscriplist');
    x.value = "";
    x.innerHTML = "";
    x.innerHTML = v;
}





let indicatorsuggestions = [["MA","Moving Average"],["EMA","Exponential Moving Average"],["WMA","Weighted Moving Average"],["RSI","Relative Strength Index"]];

const indicatorWrapper = document.querySelector(".indicator-search");
const indicatorInputBox = indicatorWrapper.querySelector("input");
const indicatorSuggBox = indicatorWrapper.querySelector(".indicatorsuggest-box");



indicatorInputBox.onkeyup = (e)=>{
    let userData = e.target.value;
    let emptyArray = [];
    let dataArray = [];
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorWrapper.classList.add("active");
        showIndicatorSuggestions(emptyArray);
        let allList = indicatorSuggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            let head = document.createElement("p");
            let desc = document.createElement("p");
            head.innerHTML = dataArray[i][0];
            desc.innerHTML = dataArray[i][1]
            head.classList.add("indicatorsuggestionHead");
            desc.classList.add("indicatorsuggestionDesc");
            allList[i].appendChild(head);
            allList[i].appendChild(desc);
            allList[i].setAttribute("name", 'this.innerText');
            allList[i].setAttribute("onclick", "openIndicatorDetails('"+dataArray[i][0]+"')");
        }
    }else{
        indicatorWrapper.classList.remove("active");
        dataArray = [];
    }
}


function showIndicatorSuggestions(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox.innerHTML = listData;
}

function openIndicatorDetails(element){
    $('#indicatorModal').modal('show')
    let x = document.getElementById('indicatorheadingModal');
    x.innerHTML = element;
}


function saveIndicatordetails(){

    var x = document.getElementsByName("period1")[0].value;
    var y = document.getElementsByName("period2")[0].value;
    var z = document.getElementById('indicatorheadingModal').innerHTML

    document.getElementsByName("indicator1")[0].value = z+","+x;
    document.getElementsByName("indicator2")[0].value = z+","+y;
    if(z == "RSI"){
        document.getElementsByName("indicator2")[0].value = "Value"+","+y;
    }
    indicatorWrapper.classList.remove("active");
    $('#indicatorModal').modal('hide');
}











const indicatorWrapper2 = document.querySelector(".indicator-search2");
const indicatorInputBox2 = indicatorWrapper2.querySelector("input");
const indicatorSuggBox2 = indicatorWrapper2.querySelector(".indicatorsuggest-box2");



indicatorInputBox2.onkeyup = (e)=>{
    console.log("Here");
    let userData = e.target.value;
    let emptyArray = [];
    let dataArray = [];
    console.log(indicatorsuggestions);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorWrapper2.classList.add("active");
        showIndicatorSuggestions2(emptyArray);
        let allList = indicatorSuggBox2.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            let head = document.createElement("p");
            let desc = document.createElement("p");
            head.innerHTML = dataArray[i][0];
            desc.innerHTML = dataArray[i][1]
            head.classList.add("indicator2suggestionHead");
            desc.classList.add("indicator2suggestionDesc");
            allList[i].appendChild(head);
            allList[i].appendChild(desc);
            allList[i].setAttribute("name", 'this.innerText');
            allList[i].setAttribute("onclick", "openIndicator2Details('"+dataArray[i][0]+"')");
        }
    }else{
        indicatorWrapper2.classList.remove("active");
        dataArray = [];
    }
}


function showIndicatorSuggestions2(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox2.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox2.innerHTML = listData;
}

function openIndicator2Details(element){
    $('#indicator2Modal').modal('show')
    let x = document.getElementById('indicator2headingModal');
    x.innerHTML = element;
}


function saveIndicatordetails2(){
    console.log("here");

    var y = document.getElementsByName("indicatorperiod22")[0].value;
    var z = document.getElementById('indicator2headingModal').innerHTML

    document.getElementsByName("indicator2")[0].value = z+","+y;
    indicatorWrapper2.classList.remove("active");
    $('#indicator2Modal').modal('hide');
}




var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

var prevDate = document.getElementById("startDate");
var todayDate = document.getElementById('stopDate');
console.log(prevDate);
prevDate.defaultValue  = parseInt(yyyy)-5+"-"+mm+"-"+dd;
todayDate.defaultValue  = yyyy+"-"+mm+"-"+dd;
