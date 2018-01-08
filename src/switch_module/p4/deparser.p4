control TopDeparser(
	packet_out packet,
	in parsed_hdrs headers){

	apply {

			packet.emit(headers.eth_hdr);

			packet.emit(headers.ipv4_hdr);
			packet.emit(headers.udp_hdr);

			packet.emit(headers.vxlan_gpe_hdr);
			packet.emit(headers.measure_hdr);
		    packet.emit(headers.hdrs_stack);

			packet.emit(headers.ipv4_inner_hdr);

			packet.emit(headers.payload);

			packet.emit(headers.tail);

	}
}
