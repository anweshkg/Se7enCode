var express = require("express");
var app = express();
const multer = require("multer");
var bodyParser = require("body-parser");
const { CosmosClient } = require("@azure/cosmos");
const http = require("https"); // or 'https' for https:// URLs
require("dotenv").config();

const spawn = require("child_process").spawn;
const client = new CosmosClient({
  endpoint: process.env.ENDPOINT,
  key: process.env.KEY,
});
fs = require("fs");

const facedata = async function face_fetch(oid) {
  try {
    const querySpec = {
      query: `SELECT usergroup.fid from usergroup WHERE usergroup.oid="d23edd7a-b716-44a3-8431-c728585daabc"`,
    };
    const { resources: results } = await client
      .database("keyDatabase")
      .container("keyContainer")
      .items.query(querySpec)
      .fetchAll();

    for (var queryResult of results) {
      let resultString = JSON.stringify(queryResult);

      return new Promise((resolve, reject) => {
        resolve(JSON.parse(resultString).fid);
      });
    }
  } catch (error) {
    console.log(error);
    return false;
  }
};

async function speech_file(oid) {
  const querySpec = {
    query: `SELECT usergroup.sid from usergroup WHERE usergroup.oid="d23edd7a-b716-44a3-8431-c728585daabc"`,
  };

  const { resources: results } = await client
    .database("keyDatabase")
    .container("keyContainer")
    .items.query(querySpec)
    .fetchAll();
  for (var queryResult of results) {
    let resultString = JSON.stringify(queryResult);
    console.log(JSON.parse(resultString).sid);
    return new Promise((resolve, reject) => {
      resolve(JSON.parse(resultString).sid);
    });
  }
}

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./files/");
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    let originalName = file.originalname;
    let extension = originalName.split(".")[1];
    cb(null, file.fieldname + "-" + uniqueSuffix + "." + extension);
  },
});

const upload = multer({ storage: storage });
var HTTP_PORT = 8000;

app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});

app.route("/face").post(upload.single("file"), (req, res) => {
  var send = false;
  console.log("connection recieved");
  facedata(req.body.oid.toString()).then((fid) => {
    var pythonProcess = spawn("python", [
      "face_final.py",
      fid.toString(),
      req.file.filename,
    ]);
    pythonProcess.stdout.on("data", (data) => {
        console.log(data.toString())

      if (send) {
        return;
      } else {
        if (
          data
            .toString()
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
            .includes("False")
        ) {
          console.log("Rejected");
          pythonProcess.kill();

          send  =true;
          return res.send({ status: "invalid" });
        } else if (
          data
            .toString()
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
            .includes("True")
        ) {
          console.log("Accepted");
          pythonProcess.kill();
          send = true;
          return res.send({ status: "auth" });
        }
      }
    });
  });
});

app.route("/speech").post(upload.single("file"), (req, response) => {
  speech_file(req.body.oid).then((url) => {
    console.log(url);
    http.get(url, (res) => {
      const path = "voice\\" + req.body.oid.toString() + ".txt";
      const writeStream = fs.createWriteStream(path);

      res.pipe(writeStream);

      writeStream.on("finish", () => {
        writeStream.close();
        console.log("Download Completed");
        console.log("Execute");
        var pythonProcess = spawn("python", [
          "speak_rek.py",
          "voice\\" + req.body.oid.toString() + ".txt",
          req.file.path,
        ]);
        pythonProcess.stdout.on("data", (data) => {
          console.log("Read");
          console.log(data.toString());
          if (
            data
              .toString()
              .replace(" ", "")
              .replace("\n", "")
              .replace("\r", "")
              .includes("Pass")
          ) {
          } else if (
            data
              .toString()
              .replace(" ", "")
              .replace("\n", "")
              .replace("\r", "")
              .includes("True")
          ) {
            response.send({ status: "voice_auth" });
          } else {
            response.send({ status: "invalid" });
          }
        });
      });
    });
  });
});

// Start server
app.listen(HTTP_PORT, () => {
  console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT));
});

// Root path
app.get("/", (req, res, next) => {
  console.log("Retuned");
  res.json({ message: "Ok" });
});
