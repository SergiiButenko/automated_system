#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
//#include <ESPmDNS.h>
#include <ESP8266HTTPUpdateServer.h>

#ifndef STASSID
#define STASSID "faza_2"
#define STAPSK "Kobe_2016"
#endif

const char* device_id = "irrigation1";
const char* ssid = STASSID;
const char* password = STAPSK;

const int r1 = 5;
const int r2 = 4;
const int r3 = 0;
const int r4 = 2;
const int r5 = 14;
const int r6 = 12;
const int r7 = 13;
const int r8 = 15;
// const int led = 13;

ESP8266WebServer server(80);
const char* serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";

void displayDeviceId() {
  server.send(200, "text/plain", device_id);
}

void send_status() {
  String msg = "{";
  msg += "\"1\":\"" + String(digitalRead(r1)) + "\",";
  msg += "\"2\":\"" + String(digitalRead(r2)) + "\",";
  msg += "\"3\":\"" + String(digitalRead(r3)) + "\",";
  msg += "\"4\":\"" + String(digitalRead(r4)) + "\",";
  msg += "\"5\":\"" + String(digitalRead(r5)) + "\",";
  msg += "\"6\":\"" + String(digitalRead(r6)) + "\",";
  msg += "\"7\":\"" + String(digitalRead(r7)) + "\",";
  msg += "\"8\":\"" + String(digitalRead(r8)) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.send(200, "application/json", msg);
}

void handleNotFound() {
  // digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.send(404, "text/plain", message);
  // digitalWrite(led, 0);
}

/* setup function */
void setup(void) {
  // pinMode(led, OUTPUT);
  // digitalWrite(led, 0);

  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r4, OUTPUT);
  pinMode(r5, OUTPUT);
  pinMode(r6, OUTPUT);
  pinMode(r7, OUTPUT);
  pinMode(r8, OUTPUT);

  digitalWrite(r1, 0);
  digitalWrite(r2, 0);
  digitalWrite(r3, 0);
  digitalWrite(r4, 0);
  digitalWrite(r5, 0);
  digitalWrite(r6, 0);
  digitalWrite(r7, 0);
  digitalWrite(r8, 0);


  Serial.begin(115200);

  Serial.println("Booting Sketch...");
  WiFi.hostname(device_id);
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);

  // Wait for connection
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/status", send_status);
  server.on("/id", displayDeviceId);

  server.on("/on", []() {
    String relay = server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 1);
    if (relay == "2")  digitalWrite(r2, 1);
    if (relay == "3")  digitalWrite(r3, 1);
    if (relay == "4")  digitalWrite(r4, 1);
    if (relay == "5")  digitalWrite(r5, 1);
    if (relay == "6")  digitalWrite(r6, 1);
    if (relay == "7")  digitalWrite(r7, 1);
    if (relay == "8")  digitalWrite(r8, 1);

    send_status();
  });

  server.on("/off", []() {
    String relay = server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 0);
    if (relay == "2")  digitalWrite(r2, 0);
    if (relay == "3")  digitalWrite(r3, 0);
    if (relay == "4")  digitalWrite(r4, 0);
    if (relay == "5")  digitalWrite(r5, 0);
    if (relay == "6")  digitalWrite(r6, 0);
    if (relay == "7")  digitalWrite(r7, 0);
    if (relay == "8")  digitalWrite(r8, 0);

    send_status();
  });

  server.on("/version", []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/plain", "mar10-09-06");
  });
  /*return index page which is stored in serverIndex */

  server.on("/status", send_status);
  server.onNotFound(handleNotFound);

  server.on("/", HTTP_GET, []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/html", serverIndex);
  });

  server.on("/update", HTTP_POST, []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/plain", (Update.hasError()) ? "FAIL" : "OK");
    ESP.restart();
  }, []() {
    HTTPUpload& upload = server.upload();
    if (upload.status == UPLOAD_FILE_START) {
      Serial.setDebugOutput(true);
      WiFiUDP::stopAll();
      Serial.printf("Update: %s\n", upload.filename.c_str());
      uint32_t maxSketchSpace = (ESP.getFreeSketchSpace() - 0x1000) & 0xFFFFF000;
      if (!Update.begin(maxSketchSpace)) { //start with max available size
        Update.printError(Serial);
      }
    } else if (upload.status == UPLOAD_FILE_WRITE) {
      if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
        Update.printError(Serial);
      }
    } else if (upload.status == UPLOAD_FILE_END) {
      if (Update.end(true)) { //true to set the size to the current progress
        Serial.printf("Update Success: %u\nRebooting...\n", upload.totalSize);
      } else {
        Update.printError(Serial);
      }
      Serial.setDebugOutput(false);
    }
    yield();
  });

  server.begin();
  /*use mdns for device_id name resolution*/
  if (!MDNS.begin(device_id, WiFi.localIP())) { //http://esp32.local
    Serial.println("Error setting up MDNS responder!");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("mDNS responder started");
  MDNS.addService("http", "tcp", 80);
  Serial.printf("Ready! Open http://%s.local in your browser\n", device_id);
}

void loop(void) {
  server.handleClient();
  MDNS.update();
  delay(1);
}
