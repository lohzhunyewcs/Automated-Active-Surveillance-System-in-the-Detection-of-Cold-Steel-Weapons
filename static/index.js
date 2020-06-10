document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        console.log('JS loaded');
    });

    // When a new vote is announced, add to the unordered list
    socket.on('knife detected', data => {
        document.querySelector('#data').innerHTML = "KNIFE DETECTED";
        // document.querySelector('#data2').innerHTML = "KNIFE DETECTED";
        // document.querySelector('#data3').innerHTML = "KNIFE DETECTED";
        // document.querySelector('#data4').innerHTML = "KNIFE DETECTED";
//        alert("Knife detected");
    });
});
