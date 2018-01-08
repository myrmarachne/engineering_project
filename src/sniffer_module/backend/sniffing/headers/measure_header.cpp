#include "measure_header.hpp"

int MeasureHeader::length(){
  return MEASURE_HDR_LEN;
}

void MeasureHeader::set_next(){
  if (fields == nullptr) return;
  if (fields->count > 0){
    next = new Option(buff_offset + length(), fields->count, fields->next_header);
  } else {
    switch (ntohs(fields->next_header)) {
      case ETHERTYPE_IP:
        next = new IPv4Header(buff_offset + length());
        break;

    }
  }
}
