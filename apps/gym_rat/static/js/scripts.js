$(document).ready(function() {
    // brings up form to edit specific set when button is clicked
    $(".edit-set-btn").one("click", function() {
        var setID = $(this).attr("id");
        var weightInput = document.createElement("input");
        $(weightInput).attr("type", "number");
        $(weightInput).attr("inputmode", "numeric");
        $(weightInput).attr("name", "weight");
        $(weightInput).attr("placeholder", "Weight in lbs.");
        $(weightInput).addClass("form-control");
        $(weightInput).appendTo(".weight-" + setID);
        var repsInput = document.createElement("input");
        $(repsInput).attr("type", "number");
        $(repsInput).attr("inputmode", "numeric");
        $(repsInput).attr("name", "reps");
        $(repsInput).attr("placeholder", "Reps");
        $(repsInput).addClass("form-control");
        $(repsInput).appendTo(".reps-" + setID);
        var button = document.createElement("button");
        $(button).addClass("btn btn-primary");
        $(button).html("Edit Set");
        $(button).appendTo(".edit-set-form-" + setID);
    });
});