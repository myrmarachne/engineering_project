control TopEgress(
	inout parsed_hdrs headers,
	inout metadata_t meta,
	inout standard_metadata_t standard_metadata){

	register<bit<16>>(1024)	counters;
	register<bit<16>>(1024)	enumeration_counters;

	action add_measure_opt(){

		headers.measure_hdr.count = headers.measure_hdr.count + 1;

		headers.hdrs_stack.push_front(1);
		headers.hdrs_stack[0].timestamp_1 = (bit<32>)(standard_metadata.time_of_day >> 32);
		headers.hdrs_stack[0].timestamp_2 = (bit<32>)(standard_metadata.time_of_day);
		headers.hdrs_stack[0].timedelta = (bit<32>)(standard_metadata.deq_timedelta);


		headers.hdrs_stack[0].sw_id = meta.switch_metadata.sw_id;


		headers.udp_hdr.length = headers.udp_hdr.length + MEASURE_OPT_LEN;
		headers.ipv4_hdr.total_len = headers.ipv4_hdr.total_len + MEASURE_OPT_LEN;
	}

	action add_vxlan_gpe_header(){

		headers.vxlan_gpe_hdr.setValid();
		headers.vxlan_gpe_hdr.next_protocol = 0xD;	// Typ oznaczajacy Measure Header - dodac te wartosc jako parametr action
		headers.vxlan_gpe_hdr.flags = headers.vxlan_gpe_hdr.flags | 4;

		headers.udp_hdr.length = headers.udp_hdr.length + VXLAN_GPE_LEN;
		headers.ipv4_hdr.total_len = headers.ipv4_hdr.total_len  + VXLAN_GPE_LEN;
	}

	action add_udp_encapsulation(){
		headers.udp_hdr.setValid();
		headers.udp_hdr.dst_port = UDP_PORT_VXLAN_GPE;
		headers.udp_hdr.src_port = 1111;
		headers.udp_hdr.checksum = 0;
		headers.udp_hdr.length = 8 + headers.ipv4_inner_hdr.total_len;	// Na razie - wyłącznie dla ipv4, dodac ew enkapsulacje ethernetowa

		headers.ipv4_hdr.total_len = headers.ipv4_hdr.total_len + 8;
	}

	action add_ipv4_encapsulation(){
		headers.ipv4_inner_hdr = headers.ipv4_hdr;
		headers.ipv4_hdr.protocol = IP_PROTOCOL_UDP;
		headers.ipv4_hdr.total_len = ((bit<16>) headers.ipv4_hdr.ihl) * 4 + headers.ipv4_hdr.total_len;
	}

	action add_measure_header(){

		add_ipv4_encapsulation();
		add_udp_encapsulation();
		add_vxlan_gpe_header();
		// Na razie - wyłącznie dla ipv4, bez ethernetowej enkapsulacji

		//checksum update

		headers.measure_hdr.setValid();
		headers.measure_hdr.count = 0;
		headers.measure_hdr.next_hdr = meta.parser_metadata.next_hdr;
		headers.measure_hdr.seq_nr = meta.count_metadata.flow_counter - 1;	// Numbering from 0
		headers.measure_hdr.src_port = meta.parser_metadata.src_port;
		headers.measure_hdr.dst_port = meta.parser_metadata.dst_port;
		headers.measure_hdr.protocol = meta.parser_metadata.protocol;
		headers.measure_hdr.src_addr = headers.ipv4_inner_hdr.src_addr;
		headers.measure_hdr.dst_addr = headers.ipv4_inner_hdr.dst_addr;

		headers.measure_hdr.modify = meta.count_metadata.modify;	// TODO: na razie kazdy ustala modify na 1

		// Length update
		headers.udp_hdr.length = headers.udp_hdr.length + MEASURE_HDR_LEN;
		headers.ipv4_hdr.total_len = headers.ipv4_hdr.total_len + MEASURE_HDR_LEN;

		add_measure_opt();

	}

	action delete_vxlan_encapsulation(){
		headers.ipv4_hdr = headers.ipv4_inner_hdr;

		headers.udp_hdr.setInvalid();
		headers.vxlan_gpe_hdr.setInvalid();

		headers.measure_hdr.setInvalid();
		headers.ipv4_inner_hdr.setInvalid();
		headers.hdrs_stack.pop_front(headers.measure_hdr.count);
	}

	action delete_measure_header(){
		meta.count_metadata.delete_flag = 1;
	}


	action mirror_data_from_clone(bit<9> port){

		/* Adding measure option for last switch */
		add_measure_opt();
		meta.ingress_metadata.port = port;

	}

	action set_counters(bit<32> index, bit<16> enumerate, bit<1> modify) {

		@atomic{
			counters.read(meta.count_metadata.flow_counter, index);

			enumeration_counters.read(meta.count_metadata.enumerate, index);

			if (meta.count_metadata.enumerate+1 >= enumerate){
				meta.count_metadata.enumerate = 0;
			} else {
				meta.count_metadata.enumerate = meta.count_metadata.enumerate + 1;
			}
			enumeration_counters.write(index, meta.count_metadata.enumerate);

			if (meta.count_metadata.enumerate == 1){
				meta.count_metadata.create_flag = 1;
				meta.count_metadata.flow_counter = meta.count_metadata.flow_counter+1;
			}
			counters.write(index, meta.count_metadata.flow_counter);

		}

		meta.count_metadata.modify = modify;
	}


	table mh_delete {
		key = {
			// Na razie wybor wylacznie w zaleznosci od docelowego adresu
			headers.ipv4_hdr.dst_addr: lpm;
		}

		actions = {
			delete_measure_header;
			NoAction;
		}

		size = 1024;
		default_action = NoAction();
	}

	table mh_create {
		key = {
			// Na razie wybor wylacznie w zaleznosci od docelowego adresu
			headers.ipv4_hdr.dst_addr: exact;
			headers.ipv4_hdr.src_addr: exact;
			meta.parser_metadata.dst_port: exact;
			meta.parser_metadata.src_port: exact;
			meta.parser_metadata.protocol: exact;
		}

		actions = {
			set_counters;
			NoAction;
		}

		size = 1024;
		default_action = NoAction();
	}

	table redirect {
		key = {
			headers.ipv4_hdr.dst_addr: lpm;
		}
		actions = {
			mirror_data_from_clone;
			NoAction;
		}
		size = 10;
		default_action = NoAction();
	}


	apply {

			if(meta.ingress_metadata.opt_added == 1){
				headers.hdrs_stack[0].timedelta = (bit<32>)(standard_metadata.deq_timedelta);
			}


			if (standard_metadata.instance_type == 32w0){
				/* Original packet */

				if (!headers.measure_hdr.isValid()){

					mh_create.apply();
					if (meta.count_metadata.create_flag == 1){
						add_measure_header();
					}

				} else {

					mh_delete.apply();
					if (meta.count_metadata.delete_flag == 1){
						delete_vxlan_encapsulation();
					}

				}
			}

			if (standard_metadata.instance_type == 32w1){
				/*
					Original parsed packet, without any changes in the ingress.
					No ip forwarding changes done - they're not necessary
					(this copy could only be mirrored to selected port)
				*/

				redirect.apply();

			}

			if (headers.ipv4_hdr.isValid()){
				/* Calculate FCS only when there is an IPv4 Header */

				bit<32> num = 0;

				hash(num, HashAlgorithm.crc32,
					32w0, {
						headers.eth_hdr,
						headers.ipv4_hdr,
						headers.udp_hdr,
						headers.vxlan_gpe_hdr,
						headers.measure_hdr,
						headers.hdrs_stack[0],
						headers.hdrs_stack[1],
						headers.hdrs_stack[2],
						headers.hdrs_stack[3],
						headers.hdrs_stack[4],

						headers.ipv4_inner_hdr,
						headers.payload
							}, 32w2147483647);


				if (!headers.tail.isValid())
						headers.tail.setValid();

				headers.tail.data = (bit<32>) ((num>>24)&0xff) | // move byte 3 to byte 0
							((num<<8)&0xff0000) | // move byte 1 to byte 2
							((num>>8)&0xff00) | // move byte 2 to byte 1
							((num<<24)&0xff000000);

				truncate((bit<32>) (14 + headers.ipv4_hdr.total_len + 4));
			}

	}
}
