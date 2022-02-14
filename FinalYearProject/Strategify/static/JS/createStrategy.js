/*
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
    scripAddedName.setAttribute("class","btn fadeIn");
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
    console.log(child);
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
    x.value = v;
    x.innerHTML = v;

}
*/


var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

var prevDate = document.getElementById("startDate");
var todayDate = document.getElementById('stopDate');
prevDate.defaultValue  = parseInt(yyyy)-5+"-"+mm+"-"+dd;
todayDate.defaultValue  = yyyy+"-"+mm+"-"+dd;








let indicatorsuggestions = [["MA","Moving Average"],["EMA","Exponential Moving Average"],["WMA","Weighted Moving Average"],["RSI","Relative Strength Index"],["Value","Value"]];

var indicatorWrapper = document.querySelector(".indicator-search");
var indicatorInputBox = indicatorWrapper.querySelector("input");
var indicatorSuggBox;



function lookup(arg){
    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#firindicatorBox"+no.toString();
    indicatorSuggBox = indicatorWrapper.querySelector(string);
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
            allList[i].setAttribute("onclick", "openIndicatorDetails('"+dataArray[i][0]+"',"+no+")");
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

function openIndicatorDetails(element,id){
    $('#indicatorModal').modal();
    let x = document.getElementById('indicatorheadingModal');
    x.innerHTML = element;
    let y = document.getElementById('modalIndicator');
    y.setAttribute("onclick","saveIndicatordetails("+id+");")
}


function saveIndicatordetails(id){

    var x = document.getElementsByName("period1")[0].value;
    var y = document.getElementsByName("period2")[0].value;
    var z = document.getElementById('indicatorheadingModal').innerHTML;
    document.getElementsByName("entryfirindicator"+id.toString())[0].value = z+","+x;
    document.getElementsByName("entrysecindicator"+id.toString())[0].value = z+","+y;
    indicatorWrapper.classList.remove("active");
    $('#indicatorModal').modal('hide');
}

















var indicatorWrapper2 = document.querySelector(".indicator-search2");
var indicatorInputBox2 = indicatorWrapper2.querySelector("input");
var indicatorSuggBox2;



function lookup2(arg){
    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#secindicatorBox"+no.toString();
    indicatorSuggBox2 = indicatorWrapper2.querySelector(string);
    console.log(indicatorWrapper);
    console.log(indicatorSuggBox2);
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
            allList[i].setAttribute("onclick", "openIndicator2Details('"+dataArray[i][0]+"',"+no+")");
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

function openIndicator2Details(element,id){
    $('#indicator2Modal').modal('show')
    let x = document.getElementById('indicator2headingModal');
    x.innerHTML = element;
    let y = document.getElementById('modalIndicator2');
    y.setAttribute("onclick","saveIndicatordetails2("+id+");");
}


function saveIndicatordetails2(id){
    var y = document.getElementsByName("indicatorperiod22")[0].value;
    var z = document.getElementById('indicator2headingModal').innerHTML

    document.getElementsByName("entrysecindicator"+id.toString())[0].value = z+","+y;
    indicatorWrapper2.classList.remove("active");
    $('#indicator2Modal').modal('hide');
}







var indicatorWrapper3 = document.querySelector(".exitConditionRow");
var indicatorInputBox3 = indicatorWrapper3.querySelector("input");
var indicatorSuggBox3;


function lookup3(arg){
    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#exitfirindicatorBox"+no.toString();
    indicatorSuggBox3 = indicatorWrapper3.querySelector(string);
    console.log(indicatorWrapper3);
    console.log(indicatorSuggBox3);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorWrapper3.classList.add("active");
        showIndicatorSuggestions3(emptyArray);
        let allList = indicatorSuggBox3.querySelectorAll("li");
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
            allList[i].setAttribute("onclick", "openIndicator3Details('"+dataArray[i][0]+"',"+no+")");
        }
    }else{
        indicatorWrapper3.classList.remove("active");
        dataArray = [];
    }
}


function showIndicatorSuggestions3(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox3.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox3.innerHTML = listData;
}


function openIndicator3Details(element,id){
    $('#indicatorModal').modal();
    let x = document.getElementById('indicatorheadingModal');
    x.innerHTML = element;
    let y = document.getElementById('modalIndicator');
    y.setAttribute("onclick","saveIndicatordetails3("+id+");")
}


function saveIndicatordetails3(id){

    var x = document.getElementsByName("period1")[0].value;
    var y = document.getElementsByName("period2")[0].value;
    var z = document.getElementById('indicatorheadingModal').innerHTML;
    document.getElementsByName("exitfirindicator"+id.toString())[0].value = z+","+x;
    document.getElementsByName("exitsecindicator"+id.toString())[0].value = z+","+y;
    indicatorWrapper3.classList.remove("active");
    $('#indicatorModal').modal('hide');
}





var indicatorWrapper4 = document.querySelector(".exitConditionRow");
var indicatorInputBox4 = indicatorWrapper3.querySelector("input");
var indicatorSuggBox4;


function lookup4(arg){
    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#exitsecindicatorBox"+no.toString();
    indicatorSuggBox4 = indicatorWrapper4.querySelector(string);
    console.log(indicatorWrapper4);
    console.log(indicatorSuggBox4);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorWrapper4.classList.add("active");
        showIndicatorSuggestions4(emptyArray);
        let allList = indicatorSuggBox4.querySelectorAll("li");
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
            allList[i].setAttribute("onclick", "openIndicator4Details('"+dataArray[i][0]+"',"+no);
        }
    }else{
        indicatorWrapper4.classList.remove("active");
        dataArray = [];
    }
}


function showIndicatorSuggestions4(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox4.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox4.innerHTML = listData;
}


function openIndicator4Details(element,id){
    $('#indicator2Modal').modal('show')
    let x = document.getElementById('indicator2headingModal');
    x.innerHTML = element;
    let y = document.getElementById('modalIndicator2');
    y.setAttribute("onclick","saveIndicatordetails4("+id+");");
}


function saveIndicatordetails4(id){

    var y = document.getElementsByName("indicatorperiod22")[0].value;
    var z = document.getElementById('indicator2headingModal').innerHTML

    document.getElementsByName("exitsecindicator"+id.toString())[0].value = z+","+y;
    indicatorWrapper4.classList.remove("active");
    $('#indicator2Modal').modal('hide');
}









function searchallscrip(){
    var input,filter;
    input = document.getElementById("searchStrategy");
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    filter = input.value.toUpperCase();
    console.log(filter);
    $.ajax({
            type:"POST",
            url:'${search_url_link}',
            data:{
              'csrfmiddlewaretoken': csrfmiddlewaretoken,
              'scrip':filter,
            },
            success :function(data){
                console.log(data);
                if(data.success){
                console.log(data.success);
                console.log(data.data)
                }else{
                console.log(data.error);
                }
            }
        })
    }
