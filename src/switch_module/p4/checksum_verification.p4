control checksumVerification(inout parsed_hdrs headers, inout metadata_t meta){

	//Checksum16() ipv4_checksum;
	bit<16> ck;

	apply {
		/*if (headers.ipv4_hdr.isValid()){
			ck = ipv4_checksum.get(
				{
				headers.ipv4_hdr.version,
				headers.ipv4_hdr.ihl,
				headers.ipv4_hdr.dscp,
				headers.ipv4_hdr.ecn,
				headers.ipv4_hdr.total_len,
				headers.ipv4_hdr.identification,
				headers.ipv4_hdr.flags,
				headers.ipv4_hdr.frag_offset,
				headers.ipv4_hdr.ttl,
				headers.ipv4_hdr.protocol,
				headers.ipv4_hdr.src_addr,
				headers.ipv4_hdr.dst_addr
				});

			if (headers.ipv4_hdr.hdr_checksum != ck){
				mark_to_drop();
			}
		}*/
	}
}
