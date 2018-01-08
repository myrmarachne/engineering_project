#ifndef VXLAN_GPE_HPP
#define VXLAN_GPE_HPP

#include "ethernet.hpp"
#include "measure_header.hpp"

#define VXLAN_GPE_PROTO_IPv4 0x1
#define VXLAN_GPE_PROTO_IPv6 0x2
#define VXLAN_GPE_PROTO_ETHERNET 0x3
#define VXLAN_GPE_PROTO_MH 0xD

#define VXLAN_GPE_LEN 8

typedef struct vxlan_gpe_hdr vxlan_gpe_hdr;
struct vxlan_gpe_hdr{
  #if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
  uint8_t	  reserved_bits:2,
            version:1,
            instance:1,
            next_protocol_bit:1,
            bum_traffic:1,
            oam_flag:1;
  #elif __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
  uint8_t   oam_flag:1,
            bum_traffic:1,
            next_protocol_bit:1,
            instance:1,
            version:1,
            reserved_bits:2;
  #endif

  uint8_t reserved_byte1;
  uint8_t reserved_byte2;
  uint8_t next_protocol;

  #if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
  uint32_t  reserved_byte3:8,
            vni:24;
  #elif __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
  uint32_t  vni:24,
            reserved_byte3:8;
  #endif
};


class VXLANGPEHeader : public Header<vxlan_gpe_hdr>{

public:

  using Header::Header;

  int length();
  void set_next();

};
#endif
