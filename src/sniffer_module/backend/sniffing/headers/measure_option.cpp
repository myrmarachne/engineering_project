#include "measure_option.hpp"

 #include <stdint.h>
#include <iostream>

using namespace std;

int Option::length(){
  return MEASURE_OPT_LEN;
}

void Option::set_next(){
  if (fields == nullptr) return;
  if (this->remaining > 1){
    next = new Option(buff_offset + length(), this->remaining-1, this->next_header);
  } else {
    switch (ntohs(this->next_header)) {
      case ETHERTYPE_IP:
        next = new IPv4Header(buff_offset + length());
        break;

    }
  }
}
