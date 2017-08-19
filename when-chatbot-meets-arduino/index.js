var five = require("johnny-five");
var TelegramBot = require('node-telegram-bot-api');

var token = '47947300:AAH4Ab7KZy7-gq2E2R16Ks7oDiPu476Islw';
// fill this variable with the chatId of the use you want
// to send the message to
var chatIds = [];
var lightSensorValue = 0;

var board = new five.Board();
var bot = new TelegramBot(token, {
  polling: true
});

// send message to who so every ask for the value
bot.onText(/\/light/, (msg, match) => {
  var chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Light is at ' + (lightSensorValue * 100) + '%');
});

// subscribe to the list of users who wish to recieve light notifications
bot.onText(/\/subscribe/, (msg, match) => {
  var chatId = msg.chat.id;
  chatIds.push(chatId);
  bot.sendMessage(chatId, 'Your will recieve light notifications ;)');
});

// unsubscribe the notifications
bot.onText(/\/unsubscribe/, (msg, match) => {
  var chatId = msg.chat.id;
  var index = chatIds.indexOf(chatId);
  chatIds.splice(index, 1);
  bot.sendMessage(chatId, 'Your have successfully unsubcribed.');
});

/**
 * if the value of sensor is within range then
 * too many message might get pushed in short span
 * of time to avoid this below logic has been included
 * to make sure that there is atleast 10 min interval between
 * two notifications
 */
var spamControlOn = true;
setInterval(function () {
  spamControlOn = true;
}, 1000 * 60 * 10)

light.within([ 0.10, 0.20 ], function() {

})
board.on("ready", function () {
  console.log('Board is ready')
  var light = new five.Light("A0");

  light.on("change", function () {
    lightSensorValue = this.level;
    if (five.Fn.inRange(this.level, 0.10, 0.30)) {
      if (spamControlOn && chatIds.length > 0) {
        chatIds.forEach(function (chatId) {
          bot.sendMessage(chatId, 'Light is : ' + (lightSensorValue * 100) + '%');
        });
        spamControlOn = false;
      }
    }
  });
});
