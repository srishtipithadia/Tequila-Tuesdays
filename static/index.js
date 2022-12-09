/*
Current Issues:
1. Want to make it so that when you go back to loading page, you cant go forward again (ie page reloads)
2. Phone number input validation via twilio
*/

var mailTaps = 0;
var modalNum = -1;

window.onload = function() {
    //clearCache();
}

function clearCache() {
    mailTaps = 0;
    modalNum = -1;
}

function noSession() {
    window.location.href="/newPage?page=loading-page.html";
}

function onSubmit(amReturning) {
    if (amReturning) {
        var number = document.getElementById("loading-input").value.replace(/\D/g, '');

        if (!number) {
            alert("Please enter a phone number first.");
        } else {
            validateNumber(number); 
        } 
    }

    if (!amReturning) {
        var number = document.getElementById("number-input").value.replace(/\D/g, '');

        var firstName = document.getElementById("first-name-input").value.toLowerCase();
        firstName = firstName.charAt(0).toUpperCase() + firstName.substring(1);

        var lastName = document.getElementById("last-name-input").value.toLowerCase();
        lastName = lastName.charAt(0).toUpperCase() + lastName.substring(1);

        if (!firstName || !lastName) {
            alert("Please enter a valid name first.");
        } else if (!number) {
            alert("Please enter a phone number first.")
        } else {
            addNewUser(firstName, lastName, number);
        }
    }

    if (!number) {
        alert("Please enter a phone number first.");
    } else {
        if (amReturning) {
            validateNumber(number); 
        } else {
            addNewUser(firstName, lastName, number);
        }
    } 
}

function addNewUser(firstName, lastName, number) {
    fetch('/addNewUser?first='+firstName+'&last='+lastName+'&number='+number)
    .then((response) => {
        return response.json();
    })
    .then((myJson) => {
        validateNumber(number)
    });
}

function register(amRegistering) {
    if (amRegistering) {
        var number = document.getElementById("loading-input").value.replace(/\D/g, '');

        document.getElementById("loading-page").style.display = "none"
        document.getElementById("registration-page").style.display = "block"

        if (number != null) {
            document.getElementById("number-input").value = number
        }
    } else {
        var number = document.getElementById("number-input").value.replace(/\D/g, '');

        document.getElementById("loading-page").style.display = "block"
        document.getElementById("registration-page").style.display = "none"

        if (number != null) {
            document.getElementById("loading-input").value = number
        }
    }
}

function validateNumber(number) {
    fetch('/checkPhone?number='+number)
    .then((response) => {
        return response.json();
    })
    .then((myJson) => {
        document.getElementById("loading-input").value = null;

        if (myJson.result) {
            sessionStorage.setItem("phoneNumberInput", number);
            sessionStorage.setItem("userName", myJson.result);

            window.location.href="/newPage?page=mailbox-page.html";
        } else {
            alert("This number is invalid.");
        }
    });
}

function openMail() {
    if (mailTaps == 0) {
        mailTaps++;
        document.getElementById("mailbox").src = "../static/images/opened-mailbox.jpeg";
    } else {
        mailTaps = 0;
        window.location.href="/newPage?page=home-page.html";
    }
}

function openPartyPage(clickedId) {
    var pageType = document.getElementById(clickedId).classList[1];
    if (pageType == "na") {
        alert("This invite isn't available yet.");
    } else if (pageType == "alert") {
        sessionStorage.setItem("selectedParty", clickedId);
        window.location.href="/newPage?page=indv-party-page.html";
    }
}

function rsvpButtonRedirect() {
    var name = sessionStorage.getItem("userName");
    var phone = sessionStorage.getItem("phoneNumberInput");

    fetch('/rsvpData?name='+name+'&number='+phone)
    .then((response) => {
        return response.json();
    })
    .then((myJson) => {
        var yesList = myJson.result;
        if (yesList) {
            userName = myJson.result
            console.log(userName);
        } else {
            alert("No RSVPs made yet.");
        }
    });

    window.location.href="/newPage?page=my-rsvps-list-page.html";
}

function signupButtonRedirect() {
    window.location.href="/newPage?page=contribution-signups-page.html";
}

function mySignupsRedirect() {
    window.location.href="/newPage?page=my-signups-page.html";
}

function incrementLabel(toIncrease) {
    var curVal = parseInt(document.getElementById("quantity-label").textContent);
    if (toIncrease) {
        document.getElementById("quantity-label").textContent = (curVal+1).toString();
    } else if (curVal-1 > 0) {
        document.getElementById("quantity-label").textContent = (curVal-1).toString();
    }
}

function openSignupModal(obj, id) {
    if (obj.classList[1] == "no") {
        document.getElementById("modal-name-input").value = null
        document.getElementById("quantity-label").textContent = (1).toString();
        modalNum = id;

        document.getElementById("modal").style.display = "block";
        window.onclick = function(event) {
            if (event.target == document.getElementById("modal")) {
                modalNum = -1;
                document.getElementById("modal").style.display = "none";
            }
          }
    }
}

function submitModal() {
    var name = document.getElementById("modal-name-input").value;
    var quantityOfCont = parseInt(document.getElementById("quantity-label").textContent);

    if (!name || quantityOfCont < 1) {
        alert("Invalid fields. Please retry.");
    } else {
        alert("Submitted " + quantityOfCont + " items for " + name + ".");
        modalNum = -1;
        document.getElementById("modal").style.display = "none";
    }
}

function showModal() {
    document.getElementById("modal").style.display = "block";
    window.onclick = function(event) {
        if (event.target == document.getElementById("modal")) {
            modalNum = -1;
            document.getElementById("modal").style.display = "none";
        }
    }
}

function updateRsvp(status) {
    var phone = sessionStorage.getItem("phoneNumberInput");
    var party = sessionStorage.getItem("selectedParty");

    fetch('/updateRsvp?number='+phone+'&status='+status)
    .then((response) => {
        return response.json();
    })
    .then((myJson) => {
        status = (status == 1) ? "Yes" : "No";
        document.getElementById("rsvp-label").value = 'said ' + status;

        document.getElementsByClassName("rsvp-answer")[0].style.display = "none";
        document.getElementsByClassName("rsvp-answer")[1].style.display = "none";

        setTimeout(() => {
            window.location.href="/newPage?page=indv-party-page.html";
        }, '500');
    });
}

function partyTab1() {
    document.getElementById("tab2cover").style.visibility = "hidden";
    document.getElementById("tab3cover").style.visibility = "hidden";
    document.getElementById("tab1cover").style.visibility = "visible";
}

function partyTab2() {
    document.getElementById("tab1cover").style.visibility = "hidden";
    document.getElementById("tab3cover").style.visibility = "hidden";
    document.getElementById("tab2cover").style.visibility = "visible";
}
function partyTab3() {
    document.getElementById("tab1cover").style.visibility = "hidden";
    document.getElementById("tab2cover").style.visibility = "hidden";
    document.getElementById("tab3cover").style.visibility = "visible";
}