#ifndef DB_CONNECTOR_HPP
#define DB_CONNECTOR_HPP

#include <mysql/mysql.h>

#include "../config.hpp"
#include <sstream>
#include <fstream>

#include <mutex>

using namespace std;

class DataBaseConnector {
public:

  DataBaseConnector(){ };
  virtual ~DataBaseConnector(){ };

  long long add_to_applications(uint8_t protocol, uint16_t port1, uint16_t port2);
  long long add_to_options(int measurement_ID, uint64_t  timestamp, uint32_t timedelta, uint32_t sw_id);
  long long add_to_measurments(int ID, bool swapped, string ip_src, string ip_dst, int seq_nr);
  bool set_up_db(db_struct_t db_struct);

private:

  MYSQL * connection;

  string HOSTNAME;
  string DATABASE;
  string USERNAME;
  string PASSWORD;
  string SOCKET;
  int PORT_NO;
  int OPT;

  bool create_db(string db_name);
  bool table_exists(string table);
  bool create_table(string table);

  bool connect();
  void disconnect();

};

#endif
