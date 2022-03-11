
$(document).ready(function() {
    var wrapper1 = $(".entryConditionRow");
    var add_button1 = $(".addEntryRow");
    var wrapper2 = $(".exitConditionRow");
    var add_button2 = $(".addExitRow");

    var x = 2;
    $(add_button1).click(function(e) {
        e.preventDefault();
        $(wrapper1).append('<div class="row fadeIn" id="inputEntryFormRow">'+
                                '<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">'+
                                    '<div class="indicator-search">'+
                                        '<input type="text" name="entryfirindicator'+x+'" placeholder="Indicator" class="form-control" autocomplete="off" id="entryfirindicator'+x+'" onkeyup="lookup(this);" required>'+
                                        '<ul class="indicatorsuggest-box" id="firindicatorBox'+x+'"></ul>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="col-lg-3 col-xl-3 col-md-12 col-sm-12 col-xs-12">'+
                                    '<select class="form-select form-control" id="entrycomparator'+x+'" name="entrycomparator'+x+'" aria-label="Default select example">'+
                                                            '<option value="0">Crosses Below</option><option value="1">Equal To</option><option selected value="2">Lower than</option><option value="3">Higher Than</option><option selected value="4">Crosses Above</option></select>'+
                                '</div>'+
                                '<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">'+
                                    '<input type="text" name="entrysecindicator'+x+'" id="entrysecindicator'+x+'" placeholder="Indicator" class="form-control" onkeyup="lookup2(this)" required >'+
                                    '<ul class="indicatorsuggest-box2" id="secindicatorBox'+x+'"></ul></div><div class="col-1">'+
                                    '<span class="w-50 h-50 deleteEntryRow" style="font-size:3rem">&times;</span>'+
                                '</div>'+
                            '</div>');
        x += 1;
    });

    $(document).on("click", ".deleteEntryRow", function() {
        $(this).closest('#inputEntryFormRow').remove();
    });

    var y = 1;
    $(add_button2).click(function(e) {
        e.preventDefault();
            $(wrapper2).append('<div class="row fadeIn" id="inputExitFormRow">'+
                                '<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">'+
                                    '<div class="indicator-search">'+
                                        '<input type="text" name="exitfirindicator'+y+'" placeholder="Indicator" class="form-control" autocomplete="off" id="exitfirindicator'+y+'" onkeyup="lookup3(this);" required>'+
                                        '<ul class="indicatorsuggest-box3" id="exitfirindicatorBox'+y+'"></ul>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="col-lg-3 col-xl-3 col-md-12 col-sm-12 col-xs-12">'+
                                    '<select class="form-select form-control" name="exitcomparator'+y+'" aria-label="Default select example">'+
                                                            '<option selected value="0">Crosses Below</option><option value="1">Equal To</option><option value="2">Lower than</option><option value="3">Higher Than</option><option selected value="4">Crosses Above</option></select>'+
                                '</div>'+
                                '<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">'+
                                    '<input type="text" name="exitsecindicator'+y+'" id="entrysecindicator'+y+'" placeholder="Indicator" class="form-control" onkeyup="lookup4(this)" required>'+
                                    '<ul class="indicatorsuggest-box4" id="exitsecindicatorBox'+y+'"></ul></div><div class="col-1">'+
                                    '<span class="w-50 h-50 deleteExitRow" style="font-size:3rem">&times;</span>'+
                                '</div>'+
                            '</div>');
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
});

function openNav() {
  document.getElementById("mySidenav").style.display = "inline-block";
}

function closeNav() {
  document.getElementById("mySidenav").style.display = "none";
}

function deploy(){
    var container = document.querySelector("#MAonTCS");
    var checkboxesAll = container.querySelectorAll('input[type="checkbox"]');
    var checkBoxesSelected = container.querySelectorAll('input[type="checkbox"]:checked');
    console.log(checkBoxesSelected[0].name);
}










