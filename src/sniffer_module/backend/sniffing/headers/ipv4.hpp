#ifndef IPv4_HPP
#define IPv4_HPP

#include "udp.hpp"
#include <netinet/ip.h>


#define IP_PROTOCOL_UDP 17

class IPv4Header : public Header<iphdr>{

public:

  using Header::Header;

  int length();
  void set_next();

};
#endif
