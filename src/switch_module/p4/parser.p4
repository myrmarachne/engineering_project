/* Every incoming frame must have a frame tail */
/* FCS is not being checked for incoming packet */

parser TopParser(
	packet_in packet,
	out parsed_hdrs headers,
	inout metadata_t meta,
	inout standard_metadata_t standard_metadata){

	state start {
		packet.extract(headers.eth_hdr);
		meta.parser_metadata.next_hdr = headers.eth_hdr.ether_type;
		meta.parser_metadata.length = 14;
		transition parse_ethernet;
	}

	state parse_ethernet {
		transition select(headers.eth_hdr.ether_type) {
			ETHERTYPE_IPV4		:	parse_ipv4;
			default				:	accept;
		}
	}

	state parse_ipv4 {
		packet.extract(headers.ipv4_hdr);
		verify(headers.ipv4_hdr.version == 4, error.IPv4BadHeader);
		verify(headers.ipv4_hdr.ihl >= 5, error.IPv4BadHeader);
		//verify(headers.ipv4_hdr.total_len >= 46, error.IPv4BadHeader);

		meta.parser_metadata.protocol = headers.ipv4_hdr.protocol;
		meta.parser_metadata.length = meta.parser_metadata.length + ((bit<32>) headers.ipv4_hdr.ihl) * 4;
		transition select(headers.ipv4_hdr.protocol){
			IP_PROTOCOL_UDP		:	parse_port_numbers;
			IP_PROTOCOL_TCP		:	parse_port_numbers;
			/* Possibility of extending for other protocols */
			default				:	parse_payload;
		}
	}

	state parse_port_numbers {
		meta.parser_metadata.src_port = packet.lookahead<bit<16>>();
		meta.parser_metadata.dst_port = (bit<16>) (packet.lookahead<bit<32>>());

		transition select(meta.parser_metadata.protocol, meta.parser_metadata.dst_port){
			(IP_PROTOCOL_UDP, UDP_PORT_VXLAN_GPE) 	: check_vxlan_gpe;
			default									: parse_payload;
		}

	}

	state check_vxlan_gpe {
		transition select((bit<8>) (packet.lookahead<bit<96>>()), (bit<1>) (packet.lookahead<bit<70>>())){
			(0xD, 1)	:	parse_udp;
			default 	: 	parse_payload;
		}
	}

	state parse_udp {
		packet.extract(headers.udp_hdr);
		meta.parser_metadata.length = meta.parser_metadata.length + UDP_LEN;

		transition select(headers.udp_hdr.dst_port){
			UDP_PORT_VXLAN_GPE	:	parse_vxlan_gpe;
			default				:	parse_payload;
		}
	}

	state parse_vxlan_gpe {
		packet.extract(headers.vxlan_gpe_hdr);
		meta.parser_metadata.length = meta.parser_metadata.length + VXLAN_GPE_LEN;

		transition select(headers.vxlan_gpe_hdr.next_protocol){
			0xD		:	parse_measure_hdr;
			default : 	parse_payload;
		}
	}

	state parse_measure_hdr {
		packet.extract(headers.measure_hdr);
		meta.parser_metadata.length = meta.parser_metadata.length + MEASURE_HDR_LEN;
		meta.parser_metadata.remaining = headers.measure_hdr.count;

		transition select(meta.parser_metadata.remaining) {
			0			:	parse_inner_packet;
			default 	:	parse_measure_opts;
		}
	}

	state parse_measure_opts {
		packet.extract(headers.hdrs_stack.next);
		meta.parser_metadata.length = meta.parser_metadata.length + MEASURE_OPT_LEN;

		meta.parser_metadata.remaining = meta.parser_metadata.remaining - 1;
		transition select(meta.parser_metadata.remaining) {
			0 		:	parse_inner_packet;
			default	:	parse_measure_opts;
		}
	}

	state parse_inner_packet {
		transition select(headers.measure_hdr.next_hdr) {
			ETHERTYPE_IPV4		:	parse_inner_ipv4;
			default				:	parse_payload;
		}
	}

	state parse_inner_ipv4 {
		packet.extract(headers.ipv4_inner_hdr);
		meta.parser_metadata.length = meta.parser_metadata.length + ((bit<32>) headers.ipv4_inner_hdr.ihl) * 4;
		transition parse_payload;
	}

	state parse_payload {
		meta.parser_metadata.payload = 14 +  ((bit<32>) headers.ipv4_hdr.total_len) - meta.parser_metadata.length;
		packet.extract(headers.payload, (meta.parser_metadata.payload) * 8);

		packet.extract(headers.tail);
		transition accept;
	}

}
