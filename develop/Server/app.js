
var express = require('express');
var app = express();
var fs = require('fs');
var multer  = require('multer');
var upload = multer({ dest: 'uploads/' });
var exec = require('child_process').exec;
var cfenv = require('cfenv');
var appEnv = cfenv.getAppEnv();
var https = require('https');
var options = {
  key:  fs.readFileSync('./key.pem'),
  cert: fs.readFileSync('./cert.pem')
};
var server = https.createServer(options, app).listen(3000,//appEnv.port,
  function() {
    console.log( "server stating on " + "3000" + " ..." );
  }
)

//app.listen(3000);
//console.log('Server is online.');

app.post('/',upload.single('data'), function(req, res) {
  var file = __dirname + "/public/images/photo.jpg"// + req.file.originalname;
  fs.readFile(req.file.path, function (err, data) {
    fs.writeFile(file, data, function (err) {
        if (err) {
            console.log(err);
        } else {
            response = {
                message: 'Success!',
                filename: req.file.originalname
            };
        }
        console.log(response);
        exec('face_recognition ../photo/known ./public/images/', (err, stdout, stderr) => {
          if (err) { console.log("error : " + err); }
          lines = stdout.split('\n');
          lines.pop();
          console.log(lines);
          var bool = false;
          lines.forEach(function(line){
            if (!line.match(/unknown_person/))
              bool = true;
          });
          if (bool) {
            console.log("response true.");
            res.end("true");
          } else {
            console.log("response false.");
            res.end("false");
          }
          if (!bool)
            exec('python ../mail/mail.py', (err, stdout, stderr) => {
                if (err) { console.log("error : " + err); }
                console.log(stdout);
              }
            );
        });
    });
  });
})
