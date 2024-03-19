getUserLocation();

function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(makeAPIcall);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}

function makeAPIcall(position) {
    const API_base_url = 'https://api.sunrise-sunset.org/json?';
    const API_params = {
        "lat": position.coords.latitude,
        "lng": position.coords.longitude,
        "tzid": Intl.DateTimeFormat().resolvedOptions().timeZone
    }

    let API_call = API_base_url;
    for (const [k, v] of Object.entries(API_params)) {
        API_call += `${k}=${v}&`;
    }

    fetch(API_call)
        .then(response => response.json())
        .then(json => formatResponse(json))
        .then(times => fetchColorTransition(times));
}

function formatResponse(json) {
    const sunrise = stringToDate(json.results.sunrise);
    const sunset = stringToDate(json.results.sunset);
    const now = new Date();

    return {
        'sunrise': sunrise,
        'sunset': sunset,
        'now': now
    }
}

function stringToDate(s) {
    const [hours, minutes, s_am_pm] = s.split(":");
    const [seconds, am_pm] = s_am_pm.split(" ");

    const t = new Date();
    t.setHours(Number(hours) + (am_pm === "AM" ? 0 : 12));
    t.setMinutes(Number(minutes));
    t.setSeconds(Number(seconds));

    return t
}

function fetchColorTransition(times) {

    fetch('./static/blog/colorTransition.json')
        .then(response => response.json())
        .then(json => gatherParams(json))
        .then(params => {
            // pass an object to be modified by reference
            let timer = { _: null };
            modifyColors(params, timer, times);
        });
}

function gatherParams(json) {
    const p1 = json.p1;
    const p2 = json.p2;

    const backgroundsElements = [
        document.body,
        document.getElementById('navbar')
    ];

    const fontElements = [
        document.getElementsByTagName('h1'),
        document.getElementsByTagName('h2'),
        document.getElementsByTagName('p'),
        document.getElementsByTagName('small'),
        document.getElementsByClassName('navbar-links'),
        document.getElementsByClassName('post')
    ];

    return [p1, p2, backgroundsElements, fontElements];
}

function modifyColors(params, timer, times) {
    const transitionRate = 0.1;
    document.addEventListener(
        "keydown",
        (event) => {
            const keyName = event.key;
            if (keyName === "a") {
                timer._ = setInterval(transitionColor, transitionRate, params, timer, times);
            }
        }
    )
}

function transitionColor(params, timer, times) {
    // console.log(times);
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
        clearInterval(timer._);
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