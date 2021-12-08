
$(document).ready(function() {
    var wrapper1 = $(".entryConditionRow");
    var add_button1 = $(".addEntryRow");
    var wrapper2 = $(".exitConditionRow");
    var add_button2 = $(".addExitRow");

    var x = 2;
    $(add_button1).click(function(e) {
        e.preventDefault();
        $(wrapper1).append('<div class="row" id="inputEntryFormRow"><div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12"><div class="indicatorsearch1"><input type="text" name="indicator1" placeholder="Indicator" class="form-control" autocomplete="off"><ul class="indicatorsuggest-box" id="indicatorBox"></ul></div></div><div class="col-lg-3 col-xl-3 col-md-12 col-sm-12 col-xs-12"><select class="form-select form-control" name="entrycomparator'+x+'" aria-label="Default select example"><option selected value="0">Crosses Below</option><option value="1">Equal To</option><option selected value="2">Lower than</option><option value="3">Higher Than</option><option value="4">Crosses Above</option></select></div><div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12"><input type="text" name="entryindicatortwo'+x+'" placeholder="Indicator" class="form-control"></div><div class="col-1"><span class="w-50 h-50 deleteEntryRow" style="font-size:3rem">&times;</span></div></div>');
        x += 1;
    });

    $(document).on("click", ".deleteEntryRow", function() {
        $(this).closest('#inputEntryFormRow').remove();
    });

    var y = 2;
    $(add_button2).click(function(e) {
        e.preventDefault();
            $(wrapper2).append('<div class="row" id="inputExitFormRow"><div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12"><input type="text" name="exitindicatorone'+y+'" placeholder="Indicator" class="form-control"></div><div class="col-lg-3 col-xl-3 col-md-12 col-sm-12 col-xs-12"><input type="text" name="exitcomparator'+y+'" placeholder="Comparator" class="form-control"></div><div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12"><input type="text" name="exitindicatortwo'+y+'" placeholder="Indicator" class="form-control"></div><div class="col-1"><span class="w-50 h-50 deleteExitRow" style="font-size:3rem">&times;</span></div></div>');
            y += 1;
    });

    $(document).on("click", ".deleteExitRow", function(e) {
        $(this).closest('#inputExitFormRow').remove();
    })


    $('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });

});



$('#createStrategyForm').submit(function(){
    var $vala = $('#addedscripList').html();
    console.log($val);
});

function openNav() {
  document.getElementById("mySidenav").style.display = "inline-block";
}

function closeNav() {
  document.getElementById("mySidenav").style.display = "none";
}




let suggestions = ["ITC.NS","RELIANCE.NS","SBIN.NS","TCS","LTI.NS","TATAMOTORS.NS","ABCAPITAL.NS","AJANTPHARM.NS","AMBUJACEM.NS","ATGL.NS","ADANIGREEN.NS","ADANITRANS.NS","MRF.NS","HDFC.NS","YESBANK.NS","ADANIENT.NS","TITAN.NS","BHARTIARTL.NS","TATASTEEL.NS","INFY.NS"];

const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
console.log("1. ",searchWrapper," 2. ",inputBox);

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
        console.log(v,scripList[i]);
    }

    let x = document.getElementById('allscriplist');
    x.value = "";
    x.innerHTML = "";
    console.log(v,x);
    x.innerHTML = v;
    console.log(x);
}





let indicatorsuggestions = [["MA","Moving Average"],["EMA","Exponential Moving Average"],["WMA","Weighted Moving Average"]];

const indicatorWrapper = document.querySelector(".indicator-search");
const indicatorInputBox = indicatorWrapper.querySelector("input");
const indicatorSuggBox = indicatorWrapper.querySelector(".indicatorsuggest-box");



indicatorInputBox.onkeyup = (e)=>{
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
    console.log("here");

    var x = document.getElementsByName("period1")[0].value;
    var y = document.getElementsByName("period2")[0].value;
    var z = document.getElementById('indicatorheadingModal').innerHTML

    document.getElementsByName("indicator1")[0].value = z+","+x;
    document.getElementsByName("indicator2")[0].value = z+","+y;
    indicatorWrapper.classList.remove("active");
    $('#indicatorModal').modal('hide');
}























