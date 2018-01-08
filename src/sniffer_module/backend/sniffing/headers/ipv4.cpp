#include "ipv4.hpp"

int IPv4Header::length(){
  if (fields != nullptr){
    return ((int)(fields->ihl)*4);
  }
  else return 20;
};

void IPv4Header::set_next(){
  if (fields == nullptr) return;
  switch (fields->protocol) {
    case IP_PROTOCOL_UDP:
      next = new UDPHeader(buff_offset + length());
      break;

  }
}
