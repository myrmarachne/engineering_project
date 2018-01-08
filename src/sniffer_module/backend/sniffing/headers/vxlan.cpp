#include "vxlan.hpp"

int VXLANGPEHeader::length(){
  return VXLAN_GPE_LEN;
}

void VXLANGPEHeader::set_next(){
  if (fields == nullptr) return;
  switch (fields->next_protocol) {
    case VXLAN_GPE_PROTO_IPv4:
      next = new IPv4Header(buff_offset + length());
      break;
    case VXLAN_GPE_PROTO_ETHERNET:
      next = new EthernetHeader(buff_offset + length());
      break;
    case VXLAN_GPE_PROTO_MH:
      next = new MeasureHeader(buff_offset + length());
      break;

  }
}
