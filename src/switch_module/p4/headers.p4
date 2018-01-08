/****************************** CONSTANTS *******************************/

const bit<16> ETHERTYPE_IPV4 = 0x800;
const bit<8> PROTOCOL_MEASURE = 0xFE;

const bit<8> IP_PROTOCOL_UDP = 0x11;
const bit<8> IP_PROTOCOL_TCP = 0x06;


const bit<16> PORT_FOR_MH = 1111;
const bit<16> UDP_PORT_VXLAN = 4789;
const bit<16> UDP_PORT_VXLAN_GPE = 4790;

typedef bit<9>  egress_spec;
typedef bit<48> mac_addr;
typedef bit<32> ipv4_addr;
typedef bit<32> sw_id_t;
typedef bit<16> port_nr;
typedef bit<64> timestamp;


#define MAX_OPTIONS 5
#define MEASURE_OPT_LEN 16
#define VXLAN_GPE_LEN 8
#define MEASURE_HDR_LEN 19
#define UDP_LEN 8
/****************************** HEADERS *******************************/


header vxlan_gpe_hdr_t {
	bit<8>		flags;
	bit<16>		reserved;
	bit<8>		next_protocol;
	bit<24>		vni;
	bit<8>		reserved2;
}

header vxlan_hdr_t {
	bit<8>		flags;
	bit<24>		reserved;
	bit<24>		vni;
	bit<8>		reserved2;
}


/* Standard Ethernet Header */
header eth_hdr_t {
	mac_addr 	dst_addr;
	mac_addr 	src_addr;
	bit<16> 	ether_type;
}

/* Standard IPv4 Header (without options) */
header ipv4_hdr_t {
	bit<4> 		version;
	bit<4> 		ihl;
	bit<6>      dscp;
	bit<2>		ecn;
    bit<16>     total_len;
    bit<16>     identification;
    bit<3>      flags;
    bit<13>     frag_offset;
    bit<8>      ttl;
    bit<8>      protocol;
    bit<16>     hdr_checksum;
    ipv4_addr  	src_addr;
    ipv4_addr  	dst_addr;
}


header measure_hdr_t {
	bit<1>		modify;
	bit<7>		reserved;
	bit<8>		count;
	bit<16>		next_hdr;	// = ethertype
	port_nr		src_port;
	port_nr		dst_port;
	ipv4_addr	src_addr;
	ipv4_addr	dst_addr;
	bit<16>		seq_nr;
	bit<8>		protocol;

}

header measure_opt_t {
	sw_id_t		sw_id;
	bit<32>		timestamp_1;
	bit<32>		timestamp_2;
	bit<32>		timedelta;
}


header udp_hdr_t {
	port_nr		src_port;
	port_nr		dst_port;
	bit<16>		length;
	bit<16>		checksum;
}

header payload_t{
	varbit<6400> data;	// TODO: DOSTOSWAC WARTOSC
}

header tail_t{
	bit<32>		data;
}


typedef measure_opt_t[MAX_OPTIONS] hdrs_stack_t;

/* Structure of parsed packet */
struct parsed_hdrs {
	eth_hdr_t 		eth_inner_hdr;
	ipv4_hdr_t 		ipv4_inner_hdr;

	measure_hdr_t 	measure_hdr;
	hdrs_stack_t	hdrs_stack;

	eth_hdr_t		eth_hdr;
	ipv4_hdr_t		ipv4_hdr;
	udp_hdr_t		udp_hdr;

	vxlan_gpe_hdr_t vxlan_gpe_hdr;

	payload_t 		payload;	//TODO
	tail_t 			tail;

}

struct egress_metadata_t {
    bit<16>  	length;
}


struct ingress_metadata_t {
    bit<16>  	length;
	bit<64>		timestamp;
	ipv4_addr  	src_addr;
	ipv4_addr  	dst_addr;
	bit<1>		opt_added;

	ipv4_addr	next_hop;

	egress_spec port;
}

struct parser_metadata_t {
    bit<8>  	remaining;
    bit<16> 	next_hdr;

	bit<8>		protocol;
	port_nr		src_port;
	port_nr		dst_port;

	bit<32>		length;
	bit<32>		payload; /* length of payload data */

	bit<1>		recirculated;
	bit<32>		crc;
	bit<8>		loop;

}

struct switch_metadata_t{
	sw_id_t		sw_id;
}

struct count_metadata_t{
	bit<32>		global_counter;
	bit<16>		flow_counter;
	bit<1>		create_flag;
	bit<1>		delete_flag;
	bit<16>		enumerate;

	bit<1>		modify;
}

struct intrinsic_metadata_t {
	bit<48> ingress_global_timestamp;
	bit<8> lf_field_list;
	bit<16> mcast_grp;
	bit<16> egress_rid;
	bit<8> resubmit_flag;
	bit<8> recirculate_flag;

}

struct metadata_t {
	ingress_metadata_t 	ingress_metadata;
	egress_metadata_t 	egress_metadata;
	parser_metadata_t 	parser_metadata;
	switch_metadata_t	switch_metadata;
	count_metadata_t	count_metadata;
	intrinsic_metadata_t intrinsic_metadata;
}

error { IPv4BadHeader }
