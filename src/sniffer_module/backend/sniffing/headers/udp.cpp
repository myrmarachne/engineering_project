#include "udp.hpp"

int UDPHeader::length(){
  return UDP_HDR_LEN;
}

void UDPHeader::set_next(){
  if (fields == nullptr) return;
  switch (ntohs(fields->dest)) {
    case UDP_PORT_VXLAN_GPE:
      next = new VXLANGPEHeader(buff_offset + length());
      break;
    default:
      break;
  }
}
