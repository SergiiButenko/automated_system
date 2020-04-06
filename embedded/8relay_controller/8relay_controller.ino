#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPUpdateServer.h>
#include "helpers.h"

/* setup function */
void setup(void) {
  for (byte i = 1; i < num_of_relay; i = i + 1) {
    pinMode(relay_pins[i], OUTPUT);
    digitalWrite(relay_pins[i], 0);
  }

  Serial.begin(115200);

  WiFi.hostname(device_id);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  wait_wifi_conn();

  server.on("/status", send_status);
  server.on("/test", test_system);
  server.on("/device_id", displayDeviceId);
  server.on("/version", displayVersion);
  server.on("/on", turn_on);
  server.on("/off", turn_off);
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
  if (!MDNS.begin(device_id, WiFi.localIP())) {
    Serial.println("Error setting up MDNS responder!");
    return;
  }

  Serial.println("mDNS responder started");
  MDNS.addService("http", "tcp", 80);
  Serial.printf("Ready! Open http://%s.local in your browser\n", device_id);
}

void loop(void) {
  wait_wifi_conn();
  server.handleClient();
  MDNS.update();
  delay(1);
}
