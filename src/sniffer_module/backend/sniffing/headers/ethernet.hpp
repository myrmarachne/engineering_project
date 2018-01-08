#ifndef ETHERNET_HPP
#define ETHERNET_HPP

#include "header.hpp"
#include "ipv4.hpp"

#include <net/ethernet.h>


class EthernetHeader : public Header<ether_header>{

public:
  using Header::Header;

  int length();
  void set_next();

};

#endif
