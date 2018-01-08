#ifndef MEASURE_HEADER_HPP
#define  MEASURE_HEADER_HPP

#include "measure_option.hpp"
#include <net/ethernet.h>

typedef struct mh_hdr mh_hdr;

#define MEASURE_HDR_LEN 19

struct mh_hdr{

    #if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
    uint8_t	  modify:1,
              reserved:7;
    #elif __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
    uint8_t   reserved:7,
              modify:1;
    #endif

    uint8_t count;
    uint16_t next_header;
    uint16_t src_port;
    uint16_t dst_port;
    struct in_addr  ip_src;
    struct in_addr  ip_dst;
    uint16_t seq_nr;
    uint8_t protocol;

};

class MeasureHeader : public Header<mh_hdr>{

public:

  MeasureHeader(){ }

  MeasureHeader(int buff_offset){
    this->buff_offset = buff_offset;
    this->measure_data = true;
  }

  long long flow_ID = -1;

  int length();
  void set_next();

};

#endif
