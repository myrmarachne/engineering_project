#ifndef LOGGER_HPP
#define  LOGGER_HPP

#include <iostream>
#include <amqpcpp.h>

#include <unistd.h>
#include <event2/event.h>
#include <amqpcpp/libevent.h>
#include <syslog.h>

#include "sla_checker.hpp"

class Logger {
public:
  Logger(){ }
  virtual ~Logger(){ }
  void send(string exchange, string routing_key, string message);
  void log_error(string message);
  void log_warning(string message);

private:


};



#endif
