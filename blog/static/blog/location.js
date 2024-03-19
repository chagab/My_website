const dotArray = document.getElementsByClassName('dot');


setInterval(transitionColor, transitionRate, params);


function transitionColor(params) {
    const [p1, p2, backgroundsElements, fontElements] = params;
    const gradientLength = p1['r'].length;

    if (typeof transitionColor.counter == 'undefined') {
        // static counter
        transitionColor.counter = 0;
    }

    if (typeof transitionColor.up == 'undefined') {
        // static bool to know if we go up or down
        transitionColor.up = true;
    }

    if (transitionColor.up) {
        transitionColor.counter++;
    }
    else {
        transitionColor.counter--;
    }

    if (transitionColor.counter <= 0 ||
        transitionColor.counter >= gradientLength) {
        transitionColor.up = !transitionColor.up;
        // clearInterval(timer._);
    }


    const [p1Color, p2Color] = makeRGBString(transitionColor.counter, p1, p2);
    changeBackgroundColor(backgroundsElements, p1Color);
    changeFontColor(fontElements, p2Color);

}

function makeRGBString(i, p1, p2) {
    const p1i = [p1['r'][i], p1['g'][i], p1['b'][i]];
    const p2i = [p2['r'][i], p2['g'][i], p2['b'][i]];

    const p1Color = `rgb(${p1i[0]}, ${p1i[1]}, ${p1i[2]})`;
    const p2Color = `rgb(${p2i[0]}, ${p2i[1]}, ${p2i[2]})`;

    return [p1Color, p2Color];
}

function changeBackgroundColor(backgroundsElements, color) {
    for (const element of backgroundsElements) {
        element.style.backgroundColor = color;
    }
}

function changeFontColor(fontElements, color) {
    for (const elements of fontElements) {
        for (const element of elements) {
            element.style.color = color;
        }
    }
}