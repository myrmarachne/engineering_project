#include "db_connector.hpp"

#include <iostream> //do coutów
using namespace std;

bool DataBaseConnector::set_up_db(db_struct_t db){
  /* Setting up database */
  HOSTNAME = db.HOSTNAME;
  USERNAME = db.USERNAME;
  PASSWORD = db.PASSWORD;
  DATABASE = db.DATABASE;
  PORT_NO = db.PORT_NO;

  if (!create_db(DATABASE))
    return false;

  /* Setting up tables */
  for (auto& table : db.TABLES){
    if (!table_exists(table.first)){
      if(!create_table(table.second))
        return false;
      }
  }

  return true;
}

bool DataBaseConnector::connect(){
  /* Initiation of a connection handle structure */

  if ((this->connection = mysql_init(nullptr)) == nullptr){
    /* TODO: Komunikat bledu - insufficient memory to allocate a new object */
    return false;
  }

  /* Creation of a connection */
  if (!mysql_real_connect(this->connection, HOSTNAME.c_str(), USERNAME.c_str(), PASSWORD.c_str(),
    DATABASE.c_str(), PORT_NO, nullptr, 0)){
      return false;
    }

  return true;
}

bool DataBaseConnector::table_exists(string table){
  if (!connect()) return false;

  /* Creating legal string from table name */
  char table_legal[2*table.length() + 1];
  size_t size = mysql_real_escape_string(this->connection, table_legal, table.c_str(), table.length());
  if (size == -1){
    disconnect();
    return false;
  }

  const char * command = "SHOW TABLES LIKE '%s'";
  size_t command_len = strlen(command);

  char query[command_len + size];
  int len = snprintf(query, command_len + size, command, table_legal);

  if (mysql_real_query(this->connection, query, len)){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return false;
  }

  MYSQL_RES *result = mysql_store_result(this->connection);

  if (result == nullptr){
    disconnect();
    return false;
  }

  if (mysql_num_rows(result) == 0){
    /* Empty set of results - the table doesn't exist */
    disconnect();
    return false;
  }

  disconnect();
  return true;

}

bool DataBaseConnector::create_table(string table_def_src){

  if (!connect()) return false;

  ifstream input(table_def_src);
  stringstream sstr;

  while(input >> sstr.rdbuf());

  if (mysql_real_query(this->connection, (sstr.str()).c_str(), (sstr.str()).length())){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return false;
  }

  disconnect();
  return true;
}

void DataBaseConnector::disconnect(){
  /* Closing of the connection */
  mysql_close(this->connection);
}


bool DataBaseConnector::create_db(string db_name){
  /* Creation of database with name db_name (if such database do not exist
  already). Returns true if database was successfully created or if database
  with provided name already exists. Returns false in case of error. */

  if ((this->connection = mysql_init(nullptr)) == nullptr){
    /* TODO: Komunikat bledu - insufficient memory to allocate a new object */
    cout<<mysql_error(this->connection)<<endl;
    return false;
  }

  /* Creation of a connection with DATABASE parameter set to nullptr */
  if (!mysql_real_connect(this->connection, HOSTNAME.c_str(), USERNAME.c_str(), PASSWORD.c_str(),
    nullptr, PORT_NO, nullptr, 0)) {
      cout<<mysql_error(this->connection)<<endl;
      return false;
}

  char db_legal[2*db_name.length() + 1];
  size_t size = mysql_real_escape_string(this->connection, db_legal, db_name.c_str(), db_name.length());
  if (size == -1){
    disconnect();
    return false;
  }
  const char * command = "CREATE DATABASE IF NOT EXISTS %s";
  size_t command_len = strlen(command);

  char query[command_len + size];
  int len = snprintf(query, command_len + size, command, db_legal);


  if (mysql_real_query(this->connection, query, len)){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return false;
  }

  disconnect();
  return true;

}


long long DataBaseConnector::add_to_applications(uint8_t protocol, uint16_t port1, uint16_t port2){
  /* Returns ID of specified flow or -1 in case of failure */

  string command = "INSERT INTO Applications(protocol, port1, port2)\
                    SELECT * FROM (SELECT %u AS protocol, %u AS port1, %u AS port2) AS temp\
                    WHERE NOT EXISTS (\
                      SELECT ID FROM Applications WHERE\
                      protocol = %u AND port1 = %u AND port2 = %u\
                    ) LIMIT 1";
  char query[command.length() + 2*(to_string(port1).length() + to_string(port2).length() + to_string(protocol).length())];
  int len = snprintf(query, command.length() + 2*(to_string(port1).length() + to_string(port2).length() + to_string(protocol).length()), command.c_str(), protocol, port1, port2, protocol, port1, port2);

  string command2 = "SELECT ID FROM Applications WHERE protocol=%u AND port1=%u AND port2=%u";
  char query2[command2.length() + sizeof(port1) + sizeof(port2) + sizeof(protocol)];
  int len2 = snprintf(query2, command2.length() + sizeof(port1) + sizeof(port2) + sizeof(protocol), command2.c_str(), protocol, port1, port2);

  if (!connect())
    return -1;

  if(mysql_query(this->connection, query)){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return -1;
  }


  if (mysql_query(this->connection, query2)){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return -1;
  }

  MYSQL_RES *result = mysql_store_result(this->connection);

  if (result == nullptr){
    disconnect();
    return -1;
  }

  MYSQL_ROW row = mysql_fetch_row(result);

  mysql_free_result(result);

  if (mysql_next_result(this->connection) != -1){
    /*  Successful and there are more results or an error occurred - there
        shouldn't be more than 1 result */
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return -1;
  }

  disconnect();
  return atoll(row[0]);

}

long long DataBaseConnector::add_to_options(int measurement_ID, uint64_t  timestamp, uint32_t timedelta, uint32_t sw_id){

  string command = "INSERT INTO Options(measurement_ID, timestamp, timedelta, switch_ID)\
                    SELECT * FROM (SELECT %u AS measurement_ID, %lu AS timestamp, %u AS timedelta, %u AS switch_ID) AS temp\
                    WHERE NOT EXISTS (\
                    SELECT measurement_ID FROM Options WHERE\
                    measurement_ID = %u AND timestamp = %lu AND timedelta = %u AND switch_ID = %u\
                    ) LIMIT 1";
  char query[command.length() + 2*(to_string(measurement_ID).length() + to_string(timestamp).length() + to_string(timedelta).length() + to_string(sw_id).length())];
  int len = snprintf(query, command.length() + 2*(to_string(measurement_ID).length() + to_string(timestamp).length() + to_string(timedelta).length() + to_string(sw_id).length()), command.c_str(), measurement_ID, timestamp, timedelta, sw_id, measurement_ID, timestamp, timedelta, sw_id);
  
  if (!connect())
    return -1;

  if (mysql_query(this->connection, query)){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return -1;
  }

  disconnect();
  return 0;

}

long long DataBaseConnector::add_to_measurments(int ID, bool swapped, string ip_src, string ip_dst, int seq_nr){
  /* There could be more then one entry with the same parameters in case of f.e resetting the switch */

  string command = "INSERT INTO Measurments (ID, swapped, IP_src, IP_dst, seq_nr) VALUES (%u, %u, INET_ATON('%s'), INET_ATON('%s'), '%u')";
  char ip_src_legal[2*ip_src.length() + 1];
  size_t size = mysql_real_escape_string(this->connection, ip_src_legal, ip_src.c_str(), ip_src.length());
  if (size == -1){
    disconnect();
    return false;
  }

  char ip_dst_legal[2*ip_dst.length() + 1];
  size_t size2 = mysql_real_escape_string(this->connection, ip_dst_legal, ip_dst.c_str(), ip_dst.length());
  if (size2 == -1){
    disconnect();
    return false;
  }

  char query[command.length() + to_string(ID).length() + 1 + strlen(ip_src_legal) + strlen(ip_dst_legal) + to_string(seq_nr).length()];
  int len = snprintf(query, command.length() + to_string(ID).length() + 1 + strlen(ip_src_legal) + strlen(ip_dst_legal) +  to_string(seq_nr).length(), command.c_str(), ID, swapped, ip_src_legal, ip_dst_legal, seq_nr);

  if (!connect())
    return -1;

  if (mysql_real_query(this->connection, query, len)){
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return -1;
  }

  long long measurement_ID = mysql_insert_id(this->connection);

  if (!ID){
    /*  Row wasn't successfully inseted */
    cout<<mysql_error(this->connection)<<endl;
    disconnect();
    return -1;
  }

  disconnect();
  return measurement_ID;

}
