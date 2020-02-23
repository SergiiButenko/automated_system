char ssid[] = "NotebookNet";            // WiFi Router ssid
char pass[] = "0660101327";             // WiFi Router password
const char* host = "http://mozz.asuscomm.com:9000";
const char* device_shotname = "weather_station_solar";
const char* device_id = "a575212a-ee1c-4237-910f-9fb4c9a32190";
const char* api_key = "123";         // API write key 


const int delay_between_requests = 10000;
const int retry_limit = 5;

/****** MQTT Settings ********************************************************/

const char* mqtt_server = "192.xxx.xxx.xxx";      // MQTT Server (broker) address


/****** Additional Settings **************************************************/

#define LANGUAGE 'EN'               //either 'DE' for German or 'EN' for English

#define TEMP_CORR (-1)              //Manual correction of temp sensor (mine reads 1 degree too high)
#define HUMI_CORR (+4)               // Changing temperature -1 equals humidity +4 (average, not precise but good enough for me)

#define ELEVATION (505)             //Enter your elevation in m ASL to calculate rel pressure (ASL/QNH) at your place

#define sleepTimeMin (10)           //setting of deepsleep time in minutes (default: 10)

// NTP   --> Just a remark - the program needs the time only for the timestamp, so for the Zambretti forecast
//           the timezone and the DST (Daylight Saving Time) is irrelevant. This is why I did not take care of DST 
//           in the code. I saw a fork on Github (truckershitch) which I believe has covered this.

#define NTP_SERVER      "ch.pool.ntp.org"
#define TZ              1           // (utc+) TZ in hours
#define DST_MN          60          // use 60mn for summer time in some countries

#define TZ_SEC          ((TZ)*3600)  // don't change this
#define DST_SEC         ((DST_MN)*60)// don't change this

/**********Blynk & ThingSpeak assginments ---------------------------------

Blynk:

virtual pin 0 Temperature (Celcius)
virtual pin 1 Humidity (%)
virtual pin 2 Absolute Pressure (hPa)
virtual pin 3 Relative Pressure (hPa)
virtual pin 4 Battery Volts (V)
virtual pin 5 Dewpoint (Celcius)
virtual pin 6 HeatIndex (Celcius)
virtual pin 7 Zambrettis Words
virtual pin 8 Accuracy in percent (%)
virtual pin 9 Trend in Words
virtual pin 10 Dewpoint Spread

ThingSpeak:

Field 1: Relative Pressure (hPa)
Field 2: Temperature (Celcius)
Field 3: Humidity (%)
Field 4: Battery (V)
Field 5: Absolute Pressure (hPa)
Field 6: Dewpoint (Celcius)
Field 7: HeatIndex (Celcius) 
Status: Zambrettis Words + Trend in Words + Accuracy

MQTT:

home/weather/solarweatherstation/tempc
home/weather/solarweatherstation/heatindexc
home/weather/solarweatherstation/dewpointc
home/weather/solarweatherstation/spreadc
home/weather/solarweatherstation/abshpa
home/weather/solarweatherstation/relhpa
home/weather/solarweatherstation/humi
home/weather/solarweatherstation/battv
home/weather/solarweatherstation/zambrettisays
home/weather/solarweatherstation/trend
home/weather/solarweatherstation/accuracy

***************************************************************************/
