#ifndef CONFIG_HPP
#define CONFIG_HPP

#include <map>
#include <unistd.h>
#include <stdio.h>

#include "rapidjson/document.h"

using namespace rapidjson;
using namespace std;

struct db_struct_t{
  string HOSTNAME = "";
  string DATABASE = "";
  string USERNAME = "";
  string PASSWORD = "";
  int PORT_NO = 0;
  typedef map<string, string> tables_t;
  tables_t TABLES;
};

struct md_struct_t{
  int MAX_SIZE = 0;
  int MAX_WORKERS = 0;
  int HOURS = 0;
  int MINUTES = 0;
  int SECONDS = 0;
};

struct broker_struct_t{
  string HOSTNAME = "127.0.0.1";
  int PORT = 5672;
  string USERNAME = "guest";
  string PASSWORD = "guest";
};

class Config {
public:
  Config(){ };
  virtual ~Config(){};

  bool load_config(string buffer);

  db_struct_t get_db_config();
  md_struct_t get_md_config();
  broker_struct_t get_broker_parameters();
  string get_dev_name();

private:
  void db_connector_config(const Value & document);
  void md_connector_config(const Value & document);
  void broker_connector_config(const Value & document);

  db_struct_t db_struct;
  md_struct_t md_struct;
  broker_struct_t broker_struct;
  string dev_name = "";

};

#endif
