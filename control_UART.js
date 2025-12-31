/**
 * Control Basico CMS
 */

//flags
var center_flag = "false";
var center = 1816;
var end_flag_Sup = "false"
var end_flag_Inf = "false"
var endSup = 2714;
var endInf = 934;

//ADC
var ads1x15 = require("node-ads1x15");
var chip = 0; //0 for ads1015, 1 for ads1115
var adc = new ads1x15(chip); //Simple usage (default ADS address on pi 2b or 3):
var channel = 0; //channel 0, 1, 2, or 3...
var samplesPerSecond = "250"; // see index.js for allowed values for your chip
var progGainAmp = "4096"; // see index.js for allowed values for your chip
var ADC;


// Serial
const { SerialPort } = require('serialport')
const { ReadlineParser } = require('@serialport/parser-readline')
const port = new SerialPort({ path: '/dev/ttyS0', baudRate: 115200 }) // /dev/ttyUSB1   /dev/ttyS0

const parser = port.pipe(new ReadlineParser())
//parser.on('data', console.log)

parser.on("data", (data) => {
 // var str = data.String(data);
  console.log("esp32: " ,data);
 // console.log("str: ",str);
});

port.on('open',function() {
  console.log('Port open');
  console.log('space ==> Scan');
  console.log('esc ==> Stop');
  console.log('c ==> Center');
  console.log('> ==> Full-CC-motor1');
  console.log('< ==> Full-CW-motor1');
  console.log('up ==> Full-CC-motor2');
  console.log('dw ==> Full-CW-motor2');
  console.log('w ==> mini-Step-CC-motor2');
  console.log('s ==> mini-Step-CW-motor2');
  console.log('q ==> micro-Step-CC-motor2');
  console.log('a ==> micro-Step-CW-motor2');
  console.log('Ctrl + c ==> Exit');
});

port.on("error", function(err) {
  console.log("Error: ", err.message);
});



var keypress = require('keypress');
 
// make `process.stdin` begin emitting "keypress" events
keypress(process.stdin);


// listen for the "keypress" event
process.stdin.on('keypress', function (ch, key) {
  //console.log('got "keypress"', key);
  if (key.ctrl && key.name == "c") {
    process.exit();
  }

  if (key.name == "right") {
    //console.log("right");
    port.write('CC1\n');
  }

  if (key.name == "left") {
    //console.log("left");
    port.write('CW1\n');
  }

  if (key.name == "up") {
    //console.log("up");
    end_flag_Inf = "true";
    port.write('CC2\n');
  }

  if (key.name == "down") {
    //console.log("down");
    end_flag_Sup = "true";
    port.write('CW2\n');
  }

  if (key.name == "escape") {
    //console.log("escape");
    port.write('stp\n');
  }

  if (key.name == "space") {
    //console.log("space");
    //port.write('ste\n');
    console.log(ADC);
  }

  if (key.name == "w" || key.name == "W") {
    if(ADC < endSup){
        port.write('MCW\n');
    }
  }

  if (key.name == "s" || key.name == "S") {
    if(ADC > endInf){
        port.write('MCC\n');
    }
  }

  if (key.name == "q" || key.name == "Q") {
    if(ADC < endSup){
        port.write('SCW\n');
    }
  }

  if (key.name == "a" || key.name == "A") {
    if(ADC > endInf){
        port.write('SCC\n');
    }
  }

  if (key.name == "c" || key.name == "C") {
    //ADC1015();
    center_flag = "true"; // 
    //end_flag_Sup = "true";
    //end_flag_Inf = "true"; // solo proteccion por si no detecta el centro

    if (ADC >= center+1){
        port.write('CC2\n');
    }
    if (ADC <= center-1){
        port.write('CW2\n');
    }
    
  }

});
 
process.stdin.setRawMode(true);
process.stdin.resume();


function ADC1015() { 
    if (!adc.busy) {
        adc.readADCSingleEnded(channel, progGainAmp, samplesPerSecond, function(err,data) {
            if (err) {
                throw err;
            }
            ADC = data;
            //console.log(ADC);
            // detiene el brazo en el centro
            if (center_flag == "true"){
                if((ADC > center-1) && (ADC < center+1)){
                    port.write('stp\n'); 
                    center_flag = "false"; 
                }
                // seguridad limites
                if(ADC > endSup){
                    port.write('stp\n');
                    center_flag = "false"; 
                }
                if(ADC < endInf){
                    port.write('stp\n');
                    center_flag = "false"; 
                }
            }
            // detiene los motores si llega a los limites del movimiento del brazo
            if(end_flag_Sup == "true"){
                if(ADC > endSup){
                    port.write('stp\n');
                    end_flag_Sup = "false";
                }
            }
            if (end_flag_Inf == "true"){
                if(ADC < endInf){
                    port.write('stp\n');
                    end_flag_Inf = "false";
                }
            }
        });
    }
}


setInterval(function() {
    ADC1015();
}, 10)


