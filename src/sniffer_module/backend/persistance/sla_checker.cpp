#ifndef SLA_CHECKER_HPP
#define SLA_CHECKER_HPP

#include "sla_checker.hpp"

using namespace std;
using namespace rapidjson;

SLAConnectionHandler::SLAConnectionHandler() : evbase_(event_base_new(), event_base_free)
, stdin_event_(event_new(evbase_.get(), STDIN_FILENO, EV_READ, _stop,
            evbase_.get()), event_free)
, evhandler_(evbase_.get()){
  event_add(stdin_event_.get(), nullptr);
}

void SLAConnectionHandler::start(){
  //  std::cout << "Waiting for messages. Press enter to exit." << std::endl;
    event_base_dispatch(evbase_.get());
}

void SLAConnectionHandler::_stop(evutil_socket_t fd, short what, void *evbase){
  //  std::cout << "Safely braking event loop." << std::endl;
    event_base_loopbreak(reinterpret_cast<event_base*>(evbase));
}

void SLAConnectionHandler::stop(){
  cout<<"KONIEC"<<endl;

  event_base_loopbreak(evbase_.get());
}

void SLAConnectionHandler::add_to_map(string flow, sla_params params){

  writer_is_waiting = true;

  unique_lock<mutex> lck(mtx);
  while(readers > 0);
  /* Check if entry already exists */
  map<string, sla_params>::iterator it;
  it = sla.find(flow);
  if (it != sla.end())
    it->second = params;
  else
    sla.insert(pair<string, sla_params>(flow, params));
  writer_is_waiting = false;
  lck.unlock();
  cv.notify_all();

}

void SLAConnectionHandler::delete_from_map(string flow){
  writer_is_waiting = true;

  unique_lock<mutex> lck(mtx);
  while(readers > 0);

  map<string, sla_params>::iterator it;
  it = sla.find(flow);
  if (it != sla.end())
    sla.erase(it);

  writer_is_waiting = false;
  lck.unlock();
  cv.notify_all();
}

void SLAConnectionHandler::print_map(){
  map<string, sla_params>::iterator it;
  cout<<"oto mapa"<<endl;
  for (it=sla.begin(); it!=sla.end(); ++it)
    cout << it->first <<endl;
}

void SLAConnectionHandler::parse(const AMQP::Message &message, SLAConnectionHandler *handler){
  int len = handler->nr.length();
  parsed_result result = parser.parse(message, len);
  string flow = result.flow;
  sla_params parameters = result.params;
  if (result.action == "ADD"){
    handler->add_to_map(flow, parameters);
  } else if (result.action == "DELETE") {
    handler->delete_from_map(flow);
  } else if (result.action == "MODIFY") {

    handler->add_to_map(flow, parameters);
  }
}


parsed_result SLAParser::parse(const AMQP::Message& m, int len){
//  std::cout << m.routingkey() << " "<< m.body() << std::endl;
//  cout<<m.bodySize()<<endl;
  char buffer[65536];
  strncpy(buffer, m.body(), m.bodySize());
  buffer[m.bodySize()] = '\0';
  Document document;
  document.Parse(buffer);
  parsed_result result;

  if(document.IsObject()){
    string flow;
    sla_params parameters;
    string action;


    if (document.HasMember("flow") && document["flow"].IsString()){
      flow = document["flow"].GetString();

      if (document.HasMember("action") && document["action"].IsString()){

        if (document.HasMember("delay") && document["delay"].IsObject()){
          const Value & document2 = document["delay"];

          long long warning, alert;

          if(document2.HasMember("warning") && document2["warning"].IsString()){
            string::size_type sz = 0;
            warning = stoll(document2["warning"].GetString(), &sz, 10);
          } else warning = -1;

          if(document2.HasMember("alert") && document2["alert"].IsString()){
            string::size_type sz = 0;
            alert = stoll(document2["alert"].GetString(), &sz, 10);
          } else alert = -1;

          parameters.delay.warning = warning;
          parameters.delay.alert = alert;

        }

        action = document["action"].GetString();

      }

      result.flow = flow;
      result.params = parameters;
      result.action = action;

    }
  }
  return result;
}

bool SLAConnectionHandler::is_writer_waiting(){
  return writer_is_waiting;
}

sla_params SLAConnectionHandler::get_sla(string flow){
  unique_lock<mutex> lck(mtx2);
  cv.wait(lck, [this]{return !is_writer_waiting();});

  mtx.lock();
  readers++;
  mtx.unlock();

  sla_params parameters = sla[flow];

  mtx.lock();
  readers--;
  mtx.unlock();

  return parameters;
}

#endif
