#include "ethernet.hpp"

int EthernetHeader::length(){
  return 14;
}

void EthernetHeader::set_next(){
  if (fields == nullptr) return;
  switch (ntohs(fields->ether_type)) {
    case ETHERTYPE_IP:
      next = new IPv4Header(buff_offset + length());
      break;

  }
}
