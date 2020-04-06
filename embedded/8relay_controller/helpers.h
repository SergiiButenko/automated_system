#include "settings.h"


ESP8266WebServer server(80);
const char* serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";


void displayDeviceId() {
  String msg = "{";
  msg += "\"device_id\":\"" + String(device_id) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.send(200, "application/json", msg);
}


void displayVersion() {
  String msg = "{";
  msg += "\"flash_version\":\"" + String(flash_version) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.send(200, "application/json", msg);
}

void send_status() {
  String msg = "{";
  for (byte i = 1; i < num_of_relay - 1; i = i + 1) {
    msg += "\"" + String(i) + "\":\"" + String(digitalRead(relay_pins[i])) + "\",";
  }
  msg += "\"" + String(num_of_relay - 1) + "\":\"" + String(digitalRead(relay_pins[num_of_relay - 1])) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.send(200, "application/json", msg);
}

void turn_on() {
  String relay = server.arg("relay");
  digitalWrite(relay.toInt(), 1);

  send_status();
}

void turn_off() {
  String relay = server.arg("relay");
  digitalWrite(relay.toInt(), 0);

  send_status();
}

void handleNotFound() {
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
}

void scan_wifi() {
  Serial.println("Scan start");

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("Scan done");
  if (n == 0) {
    Serial.println("Error: No networks found");
    return;
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
      delay(10);
    }
  }
  Serial.println("");
}


void wait_wifi_conn() {
  // Wait for connection
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(1000);
    ESP.restart();
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void test_relay() {
  for (byte i = 1; i < num_of_relay; i = i + 1) {
    digitalWrite(relay_pins[i], 0);
    delay(1000);
    digitalWrite(relay_pins[i], 1);
    delay(1000);
    digitalWrite(relay_pins[i], 0);
  }
}

void test_system() {
  send_status();
  
  test_relay();
  scan_wifi();
}
