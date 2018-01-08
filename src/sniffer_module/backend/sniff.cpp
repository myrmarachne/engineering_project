#include <mysql/mysql.h>

#include <iostream>
#include <algorithm>
#include <thread>
#include <chrono>
#include <amqpcpp.h>
#include <fstream>
#include <sstream>

#include <functional>
#include <unistd.h>
#include <event2/event.h>
#include <amqpcpp/libevent.h>
#include <time.h>

#include "persistance/worker.hpp"
#include "persistance/measure_data.hpp"
#include "config.hpp"
#include "sniffing/sniffer.hpp"

#include <thread>

using namespace std;

Parser * parser;

void callback(uint8_t *args, const struct pcap_pkthdr *header, const u_char *packet);

void sla_checker_callback(Config * config, SLAConnectionHandler * handler);
void thread_callback(MeasureData * measure_data, Config * config, SLAConnectionHandler * handler);

int main(int argc, char **argv){

  if (mysql_library_init(0, NULL, NULL)) {
    printf("Could not initialize MySQL library\n");
    return false;
  }

  string path_to_sniff_file = argv[0];
  string file_name = "/conf/conf.json";
  string new_dir = path_to_sniff_file.substr(0, path_to_sniff_file.size() - 5);

  if (chdir(new_dir.c_str()) < 0){
    printf("An error with chdir occurred %s\n", strerror(errno));
  }

  char cwd[1024];
  getcwd(cwd, sizeof(cwd));

  strcat(cwd, file_name.c_str());
  FILE * pFile = fopen(cwd, "rb");
  ifstream file(cwd);
  stringstream buffer;

  buffer << file.rdbuf();
  string str = buffer.str();

  Config * config = new Config();

  config->load_config(str);

  MeasureData * measure_data = new MeasureData(config->get_md_config());
  SLAConnectionHandler * handler = new SLAConnectionHandler();

  thread new_thread = thread(thread_callback, measure_data, config, handler);
  new_thread.detach();

  thread new_thread2 = thread(thread_callback, measure_data, config, handler);
  new_thread2.detach();

  thread sla_checker = thread(sla_checker_callback, config, handler);
  sla_checker.detach();

  parser = new Parser(measure_data);

  Sniffer * sniffer = new Sniffer(parser);
  sniffer->sniff(config->get_dev_name());

  mysql_library_end();

  return 0;
}


void thread_callback(MeasureData * measure_data, Config * config, SLAConnectionHandler * handler){
  Worker * worker;
    try {
      worker = new Worker(config->get_db_config());
      worker->sla_check(handler);
      worker->listen(measure_data);

    } catch (const char * msg){
      printf("%s\n", msg);
      exit(1);
    }

}

void sla_checker_callback(Config * config, SLAConnectionHandler * handler){

    broker_struct_t broker_struct = config->get_broker_parameters();

    // Create an AMQP connection object
    auto evbase = event_base_new();
    AMQP::TcpConnection connection((*handler), AMQP::Address(broker_struct.HOSTNAME, broker_struct.PORT, AMQP::Login(broker_struct.USERNAME, broker_struct.PASSWORD), "/"));

    // Create a channel
    AMQP::TcpChannel channel(&connection);

    channel.onError([handler](const char* message){
        handler->stop();
    });

    time_t number = time(NULL);
    handler->nr = to_string(number);

    channel.declareExchange("topic_logs3", AMQP::topic).onSuccess([&](){
                channel.publish("topic_logs3", "SLA.get", "{ \"GET\" : "+handler->nr+"}");
                event_base_loopbreak(evbase);
                event_base_dispatch(evbase);
                event_base_free(evbase);
            }
        );

    channel.declareQueue("logs");
    channel.bindQueue("topic_logs3", "logs", "SLA."+handler->nr);

    channel.consume("logs", AMQP::noack).onReceived (
                [handler, &channel](const AMQP::Message& m, uint64_t deliveryTag, bool redelivered){
                    handler->parse(m, handler);
                    handler->print_map();
                }
              );

    handler->start();
    cout<<"KONIEC2"<<endl;


    connection.close();
}
