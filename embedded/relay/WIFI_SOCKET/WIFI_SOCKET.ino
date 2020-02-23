#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

//const char* ssid = "NotebookNet";
//const char* password = "0660101327";
const char* ssid = "faza_2";
const char* password = "Kobe_2016";

ESP8266WebServer server(80);

const int l1 = D5;
const int r1 = D7;

void blink_connected() {
  digitalWrite(l1, 0);
  delay(100);
  digitalWrite(l1, 1);
  delay(100);
  digitalWrite(l1, 0);
  delay(100);
  digitalWrite(l1, 0);
  delay(100);
  digitalWrite(l1, 1);
  delay(100);
  digitalWrite(l1, 0);
  delay(100);
  digitalWrite(l1, 0);
  delay(100);
  digitalWrite(l1, 1);
  delay(100);
  digitalWrite(l1, 0);
}

void blink_led() {
  digitalWrite(l1, 0);
  delay(200);
  digitalWrite(l1, 1);
}

void handleRoot() {
  server.send(200, "text/plain", "hello from esp8266!");
  blink_led();
}

void handleNotFound(){
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  blink_led();
}


void send_status(){
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    server.send(200, "application/json", "{\"1\":" + String(r1_status) + ", \"2\":" + String(r2_status) + "}");
}

void setup(void){
  Serial.println("setup");
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);
 
  digitalWrite(r1, 0);
  digitalWrite(r2, 0);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  
  Serial.begin(115200);
  WiFi.setAutoConnect (true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("done");
  blink_led();
  
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    blink_led();   
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  blink_connected();

  server.on("/", handleRoot);

  server.on("/test", [](){
    server.send(200, "text/plain", "this works as well");
    blink_led();
  });

  server.on("/on", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 1);
    if (relay == "2")  digitalWrite(r2, 1);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    digitalWrite(l1, r1_status);
    digitalWrite(l2, r2_status);
    send_status();
    blink_led();
  });

  server.on("/off", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 0);
    if (relay == "2")  digitalWrite(r2, 0);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    digitalWrite(l1, r1_status);
    digitalWrite(l2, r2_status);
    send_status();
    blink_led();
  });

  server.on("/status", [](){
    send_status();
    blink_led();
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();
}
