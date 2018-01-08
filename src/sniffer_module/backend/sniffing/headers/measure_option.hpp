#ifndef MEASURE_OPT_HPP
#define MEASURE_OPT_HPP

#include "header.cpp"
#include "ipv4.hpp"

#include <net/ethernet.h>

#define MEASURE_OPT_LEN 16

struct mh_opt{
  uint32_t  sw_id;
  uint32_t  timestamp_1;
  uint32_t  timestamp_2;
  uint32_t  timedelta;
};

class Option : public Header<mh_opt> {
public:
    Option(int buff_offset, uint8_t remaining, uint16_t next_header){
      this->buff_offset = buff_offset;
      this->remaining = remaining;
      this->next_header = next_header;
      this->measure_data = true;
      this->option = true;
    }

    uint8_t remaining = 0;
    uint16_t next_header = 0;

    long long measurement_ID = -1;

    int length();
    void set_next();

};

#endif
