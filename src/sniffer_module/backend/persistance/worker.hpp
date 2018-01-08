#ifndef WORKER_HPP
#define  WORKER_HPP

#include "measure_data.hpp"
#include "db_connector.hpp"
#include "logging.hpp"
#include <arpa/inet.h> // inet ntoa
#include <string>
#include <map>

using namespace std;

#define MAX_OPTIONS 15

class Worker : public DataBaseConnector {
public:

  Worker(db_struct_t db_struct);
  virtual ~Worker(){ }

  void stop();
  void run(MeasureData * measure_data);
  void listen(MeasureData * measure_data);
  void append(list<IHeader *> headers);
  void sla_check(SLAConnectionHandler * handler);

private:
  bool work = true;
  list<IHeader *> buffer;
  int insert_measure_header(MeasureHeader * mh);
  uint64_t insert_option(Option * mo, int measurement_ID);

  string get_flow_string(MeasureHeader * mh);

  Logger * logger;
  SLAConnectionHandler * sla_handler;
  map<string, bool> alert;

};

#endif
