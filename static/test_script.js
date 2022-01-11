// Users should be able to change the color of any element with the
// class, "changes-colors", by clicking on the "Turn Stuff Red" button
// or "Turn Stuff Blue" button.
//
// Clicking on "Turn Stuff Red" should make text red and clicking on "Turn
// Stuff Blue" should make text blue.

const colorChangeButtons = document.querySelectorAll('button'); //this used to be (button.changes-colors)

for (const colorChangeButton of colorChangeButtons) {

  colorChangeButton.addEventListener('click', (evt) => {

    const newText = document.querySelectorAll('.changes-colors');
      
    const button = evt.target;
      // the button ID contains the color we want to change to
      for (const text of newText) //need to loop through the text in order to change the text color
      if (button.id === 'red-changer') {
        text.style.color = "red";
      }
      else {
        text.style.color = "blue";
        }}

  )};