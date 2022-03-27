'use strict';

const h1 = document.querySelector(".body");

const map = document.querySelector("#map_france");
const areas = document.querySelector(".france_areas");

fetch('/city/Lyon').then(function (response) {
    response.json().then(function (data) {
        h1.innerHTML = data.main;
    });
});

