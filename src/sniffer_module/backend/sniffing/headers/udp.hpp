#ifndef UDP_HPP
#define UDP_HPP

#include "vxlan.hpp"
#include <netinet/udp.h>

#define UDP_HDR_LEN 8
#define UDP_PORT_VXLAN_GPE 4790


class UDPHeader : public Header<udphdr>{
public:

  using Header::Header;
  int length();
  void set_next();

};
#endif
