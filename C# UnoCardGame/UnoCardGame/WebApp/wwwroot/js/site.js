
// Timer for 5 seconds
// window.startTimer = function(initialTimerValue) {
//     let timerValue = initialTimerValue;
//     let timerLabel = document.querySelector("#counter");
//     let switchToNextPlayer = document.querySelector("#switchToNextPlayer");
//
//     setInterval(() => {
//         timerValue--;
//         timerLabel.innerHTML = timerValue.toString();
//         if (timerValue <= 0) {
//             switchToNextPlayer.submit();
//         }
//     }, 1000);
// }

// // Call the function with initial timer value 5
// startTimer(5);
//
// // Call the function with initial timer value 0
// startTimer(0);

// let timerValue3 = 5;
// let timerLabel3 = document.querySelector("#shoutUno");
// let switchTo = document.querySelector("#switchToNextPlayer");
//
// setInterval(() => {
//     timerValue3--;
//     timerLabel3.innerHTML = timerValue3.toString();
//     if (timerValue3 <= 0) {
//         switchTo.submit();
//     }
// }, 1000);

let timerValue1 = 5;
let timerLabel1 = document.querySelector("#counter");
let switchToNextPlayer = document.querySelector("#switchToNextPlayer");

setInterval(() => {
    timerValue1--;
    timerLabel1.innerHTML = timerValue1.toString();
    if (timerValue1 <= 0) {
        switchToNextPlayer.submit();
    }
}, 1000);


// Reload page after 5 seconds
let timerValue2 = 1;
let timerLabel2 = document.querySelector("#reload-label");

setInterval(() => {
    timerValue2--;
    timerLabel2.innerHTML = timerValue2.toString();
    if (timerValue2 <= 0) {
        window.location.reload();
    }
}, 1000);