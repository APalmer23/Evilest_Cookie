//!!!!!!! Elements called in cookie.js that don't have correct name from index.html !!!!!!!
//PLAYBUTTON (button to get new cookie) = 
//PLAYAREA (image background for player to trace) = 
//CANVAS (area where player can trace) = 
//DONEBUTTON (button to save attempt) = 



//ACTUAL GAME
const canvas = document.getElementById("CANVAS");
const ctx = canvas.getContext("2d");
const doneButton = document.getElementById("DONEBUTTON");

let isCutting = false; 
let hasCut = false;
let lastX = 0;
let lastY = 0;

ctx.strokeStyle = "white";
ctx.lineWidth = 2;
ctx.lineCap = "round";


//Display image in play area and prep game, but don't start timer
document.getElementById("PLAYBUTTON").addEventListener("click", async () => {
  const playArea = document.getElementById("PLAYAREA");
  //load image
  //show as bitmap to playArea
})


//Start cutting and start timer (10 min)
canvas.addEventListener("mousedown", async () => {
  if (hasCut) {
    isCutting = true;
    lastX = e.offsetX;
    lastY = e.offsetY;  
    const timeoutID = setTimeout(() => { console.log("Timer Started!"); }, 600000);
  }
})


//As mouse moves, record shift and render a stroke for that movement
canvas.addEventListener("mousemoving", async () => {
  if (!isCutting) return;
  ctx.beginPath();
  ctx.moveTo(lastX, lastY);
  ctx.lineTo(e.offsetX, e.offsetY);
  ctx.stroke();

  lastX = e.offsetX;
  lastY = e.offsetY;
})



canvas.addEventListener("mouseleave", async () => {
  //end game if mouse leaves canvas
})


//When mouse released, end cutting, prevent cutting this cookie again, and end timer
canvas.addEventListener("mouseup", async() => {
  isCutting = false;
  hasCut = true;
})


//save cursor movements to bitmap
