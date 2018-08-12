# Monitor-System-for-Flume
The whole monitor system is comprised of threee main modules. The back end code is written in Python and the front end in JavaScript.
* The Captor module integrates with Flume, retrieving information on data consumption from the Flume metrics payload. It then stores this information into Redis. This module also includes the front end code for real time data visualization using Highstock.
* The Eagle module is responsible for monitoring the data and alerting Wechat users for exception conditions using Tornado.
* The last one is the Wechat server that encapsulates the official Wechat SDK to handle http requests using Tornado. 
