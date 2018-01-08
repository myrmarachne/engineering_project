#include <iostream>
#include <amqpcpp.h>

#include <unistd.h>
#include <event2/event.h>
#include <amqpcpp/libevent.h>

#include <map>
#include <string>
#include <mutex>
#include <condition_variable>

#include "../rapidjson/document.h"
#include "../rapidjson/filereadstream.h"

using namespace std;

class LibEventHandlerMyError : public AMQP::LibEventHandler {
public:
    LibEventHandlerMyError(struct event_base* evbase) : LibEventHandler(evbase), evbase_(evbase_) {}
    void onError(AMQP::TcpConnection *connection, const char *message) override
    {
        std::cout << "Error: " << message << std::endl;
        event_base_loopbreak(evbase_);
    }
private:
    struct event_base* evbase_ {nullptr};
};


struct sla_params {
  struct delay_t{
    long long warning;
    long long alert;
  } delay;
};

struct parsed_result {
  sla_params params;
  string flow;
  string action;
};

class SLAParser {
public:
   static parsed_result parse(const AMQP::Message& m, int len);

};

class SLAConnectionHandler {
public:
    using EventBasePtrT = std::unique_ptr<struct event_base, std::function<void(struct event_base*)> >;
    using EventPtrT = std::unique_ptr<struct event, std::function<void(struct event*)> >;

    EventBasePtrT evbase_;
    EventPtrT stdin_event_;
    LibEventHandlerMyError evhandler_;

    SLAConnectionHandler();
    virtual ~SLAConnectionHandler(){ cout<<"gine"<<endl;}

    void start();
    void stop();
    void run();
    string nr = "";

    operator AMQP::TcpHandler*(){
        return &evhandler_;
    }

    void add_to_map(string flow, sla_params params);
    void delete_from_map(string flow);

    void print_map();
    static void parse(const AMQP::Message &message, SLAConnectionHandler *handler);

    sla_params get_sla(string flow);//

    bool is_writer_waiting();

private:
    static void _stop(evutil_socket_t fd, short what, void *evbase);

    mutex mtx, mtx2;

    condition_variable cv;

    int readers = 0;

    bool writer_is_waiting = false;

    static SLAParser parser;

    map<string, sla_params> sla;
};
