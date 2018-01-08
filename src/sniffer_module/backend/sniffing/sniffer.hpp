#ifndef SNIFFER_HPP
#define  SNIFFER_HPP

#include <pcap.h>
#include <cstdlib>   // exit
#include <poll.h>

#include "parser.hpp"


#define SNAPSHOT_LENGTH 65535

void callback(uint8_t *args, const struct pcap_pkthdr *header, const u_char *packet);


class Sniffer {
public:
  Sniffer(Parser * p){
    parser = p;
  }
  virtual ~Sniffer(){ }
  void sniff(string dev_name);


private:
  void error(const char* function_name);
  void error_buf(const char* function_name, char *errbuf);
  Parser * parser;
};


#endif
