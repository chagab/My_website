fetchColorTransition();

function fetchColorTransition() {
    console.log('in');
    fetch('./static/blog/json/colorTransition.json')
        .then(response => response.json())
        .then(json => gatherParams(json))
        .then(params => {
            // pass an object to be modified by reference
            let timer = { _: null };
            modifyColors(params, timer);
        });
}

function gatherParams(json) {
    const p1 = json.p1;
    const p2 = json.p2;

    const backgroundsElements = [
        document.body,
        document.getElementsByTagName('html')[0],
        document.getElementById('navbar')
    ];

    const fontElements = [
        document.getElementsByTagName('h1'),
        document.getElementsByTagName('h2'),
        document.getElementsByTagName('p'),
        document.getElementsByTagName('small'),
        document.getElementsByClassName('post'),
    ];

    const svgElements = document.querySelectorAll('#outside-links object');

    return [p1, p2, backgroundsElements, fontElements, svgElements];
}

function modifyColors(params, timer) {
    const color_button = document.getElementById('toggle-color');
    color_button.onclick = function () {
        const transitionRate = 0.1;
        timer._ = setInterval(transitionColor, transitionRate, params, timer);
    };
}

function transitionColor(params, timer) {
    const [p1, p2, backgroundsElements, fontElements, svgElements] = params;
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
        clearInterval(timer._);
        updateImshowCmap(transitionColor.up)
    }


    const [p1Color, p2Color] = makeRGBString(transitionColor.counter, p1, p2);
    changeBackgroundColor(backgroundsElements, p1Color);
    changeFontColor(fontElements, p2Color);
    // changeSvgGradient(svgElements, gradientLength, transitionColor.up);
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

function changeSvgGradient(svgElements, gradientLength, up) {
    // TDOD - debug this function 
    for (const element of svgElements) {
        const svg = element.getSVGDocument();
        const gradientCollection = svg.getElementsByTagName('linearGradient');
        const n = gradientCollection.length
        const gradient = gradientCollection[n - 1];
        const x1 = gradient.x1;
        const y1 = gradient.y1;
        const x2 = gradient.x2;
        const y2 = gradient.y2;

        if (typeof transitionColor.step_x == 'undefined') {
            transitionColor.step_x = Math.abs(x2 - x1) / gradientLength;
        }

        if (typeof transitionColor.step_y == 'undefined') {
            transitionColor.step_y = Math.abs(y2 - y1) / gradientLength;
        }

        if (up) {
            gradient.setAttribute('x1', gradient.x1 + transitionColor.step_x);
            gradient.setAttribute('y1', gradient.y1 + transitionColor.step_y);
            gradient.setAttribute('x2', gradient.x2 - transitionColor.step_x);
            gradient.setAttribute('y2', gradient.y2 - transitionColor.step_y);
        } else {
            gradient.setAttribute('x1', gradient.x1 - transitionColor.step_x);
            gradient.setAttribute('y1', gradient.y1 - transitionColor.step_y);
            gradient.setAttribute('x2', gradient.x2 + transitionColor.step_x);
            gradient.setAttribute('y2', gradient.y2 + transitionColor.step_y);
        }
    }
}

function updateImshowCmap(up) {
    const graphDiv = document.getElementsByClassName('plotly-graph-div js-plotly-plot')[0];
    if (up) {
        const cmap = [[0, 'rgb(40, 40, 40)'], [1, 'rgb(200, 200, 200)']];
        graphDiv.layout.coloraxis.colorscale = cmap;
    } else {
        const cmap = [[0, 'rgb(200, 200, 200)'], [1, 'rgb(40, 40, 40)']];
        graphDiv.layout.coloraxis.colorscale = cmap;
    }
    Plotly.redraw(graphDiv)
}