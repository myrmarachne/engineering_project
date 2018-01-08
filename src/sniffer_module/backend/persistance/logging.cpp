#include "logging.hpp"
using namespace std;

void Logger::send(string exchange, string routing_key, string message){
	auto evbase = event_base_new();

	/*Initialize connection parameters*/
	LibEventHandlerMyError handler(evbase);

	AMQP::TcpConnection connection(&handler, AMQP::Address("10.0.2.15", 5672, AMQP::Login("guest", "guest"), "/"));

  AMQP::TcpChannel channel (&connection);
  channel.onError([&evbase](const char* message)
      {
          std::cout << "Channel error: " << message << std::endl;
          event_base_loopbreak(evbase);
      });
  channel.declareExchange("topic_logs3", AMQP::topic)
      .onError([&](const char* msg)
      {
          std::cout << "ERROR: " << msg << std::endl;
      }).onSuccess (
            [&]()
            {
							channel.publish("topic_logs3", routing_key, message);
              event_base_loopbreak(evbase);
            }
					);

		event_base_dispatch(evbase);
		event_base_free(evbase);
		connection.close();

}

void Logger::log_error(string message){
	openlog("sla_project", LOG_PID, LOG_SYSLOG);
	syslog(LOG_ERR, message.c_str());
	closelog();
}

void Logger::log_warning(string message){
	openlog("sla_project", LOG_PID, LOG_SYSLOG);
	syslog(LOG_WARNING, message.c_str());
	closelog();
}
