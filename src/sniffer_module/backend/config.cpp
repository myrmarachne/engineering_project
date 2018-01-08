#include "config.hpp"
#include <errno.h>
#include <string.h>

bool Config::load_config(string buffer){

  /* Function that parses JSON configuration file and loads configuration
     structures from it */

  Document document;

  document.Parse<0>(buffer.c_str());

  if(!document.IsObject()){
    return false;
  }

  if(!document.HasMember("DataBaseConnector")){
    return false;
  }
  const Value & db_connector = document["DataBaseConnector"];
  db_connector_config(db_connector);


  if(!document.HasMember("MeasureData")){
    return false;
  }
  const Value & md_connector = document["MeasureData"];
  md_connector_config(md_connector);

  if(!document.HasMember("SLAConnectionHandler")){
    return false;
  }

  const Value & broker_connector = document["SLAConnectionHandler"];
  broker_connector_config(broker_connector);

  if (document.HasMember("Interface") && document["Interface"].IsString())
    this->dev_name = document["Interface"].GetString();

  return true;
}

void Config::md_connector_config(const Value & document){
  if (document.HasMember("MAX_SIZE") && document["MAX_SIZE"].IsNumber())
    md_struct.MAX_SIZE = document["MAX_SIZE"].GetInt();

  if (document.HasMember("MAX_WORKERS") && document["MAX_WORKERS"].IsNumber())
    md_struct.MAX_WORKERS = document["MAX_WORKERS"].GetInt();

  if (document.HasMember("HOURS") && document["HOURS"].IsNumber())
    md_struct.HOURS = document["HOURS"].GetInt();

  if (document.HasMember("MINUTES") && document["MINUTES"].IsNumber())
    md_struct.MINUTES = document["MINUTES"].GetInt();

  if (document.HasMember("SECONDS") && document["SECONDS"].IsNumber())
    md_struct.SECONDS = document["SECONDS"].GetInt();
}

void Config::db_connector_config(const Value & document){

  if (document.HasMember("HOSTNAME") && document["HOSTNAME"].IsString())
    db_struct.HOSTNAME = (document["HOSTNAME"].GetString());

  if (document.HasMember("DATABASE") && document["DATABASE"].IsString())
    db_struct.DATABASE = document["DATABASE"].GetString();

  if (document.HasMember("USERNAME") && document["USERNAME"].IsString())
    db_struct.USERNAME = document["USERNAME"].GetString();

  if (document.HasMember("PASSWORD") && document["PASSWORD"].IsString())
    db_struct.PASSWORD = document["PASSWORD"].GetString();

  if(document.HasMember("PORT_NO") && document["PORT_NO"].IsNumber())
    db_struct.PORT_NO = document["PORT_NO"].GetInt();

  /* Create map with tables names and linkt to source files */
  if(document.HasMember("TABLES")){
    const Value & tables = document["TABLES"];

    for (Value::ConstMemberIterator iter = tables.MemberBegin(); iter != tables.MemberEnd(); iter++){

      if (iter->name.IsString() && iter->value.IsString()){
        (db_struct.TABLES)[iter->name.GetString()] = iter->value.GetString();
      }
    }
  }

}

void Config::broker_connector_config(const Value & document){

  if (document.HasMember("HOSTNAME") && document["HOSTNAME"].IsString())
    broker_struct.HOSTNAME = (document["HOSTNAME"].GetString());

  if (document.HasMember("USERNAME") && document["USERNAME"].IsString())
    broker_struct.USERNAME = document["USERNAME"].GetString();

  if (document.HasMember("PASSWORD") && document["PASSWORD"].IsString())
    broker_struct.PASSWORD = document["PASSWORD"].GetString();

  if(document.HasMember("PORT") && document["PORT"].IsNumber())
    broker_struct.PORT = document["PORT"].GetInt();

}


db_struct_t Config::get_db_config(){
  return this->db_struct;
}

md_struct_t Config::get_md_config(){
  return this->md_struct;
}

string Config::get_dev_name(){
  return this->dev_name;
}

broker_struct_t Config::get_broker_parameters(){
  return this->broker_struct;
}
