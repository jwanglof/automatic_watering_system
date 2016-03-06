"use strict";

var http = require('http');
var mraa = require("mraa");

var Resistance = require('./utils/Resistance');

// Gpio
const digital2 = 2;
const digital3 = 3;
const digital4 = 4;
const digital5 = 5;
const digital6 = 6;
const digital7 = 7;
const digital8 = 8;

// Aio
const analog0 = 0;
const analog1 = 1;
const analog2 = 2;
const analog3 = 3;

var analogPin0 = new mraa.Aio(analog0);

var app = http.createServer((req, res) => {
  //var pinRead = analogPin0.read();
  //var resistance = getResistance.getAnalogResistance(pinRead);

  let Resistance = new Resistance(analogPin0.read());

  console.log(111, "Resistance:", Resistance.analogResistance, Resistance.analogResistance10Bit);

  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('<h1>Hello world from Intel IoT platform!</h1>');
}).listen(1337);