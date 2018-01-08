control TopIngress(
	inout parsed_hdrs headers,
	inout metadata_t meta,
	inout standard_metadata_t standard_metadata){

	action drop() {
        mark_to_drop();
		exit;
	}

	action ipv4_forward(ipv4_addr next_hop, egress_spec port) {
		/* Forward packet to the specified port */
        standard_metadata.egress_spec = port;

		/* Setting next hop address */
		meta.ingress_metadata.next_hop = next_hop;

        /* Modify IP Header */
        /* Decrement TTL */
        headers.ipv4_hdr.ttl = headers.ipv4_hdr.ttl - 1;

	}

	action add_switch_id(sw_id_t sw_id){
		meta.switch_metadata.sw_id = sw_id;
	}

	action rewrite_smac(bit<48> smac) {
    	headers.eth_hdr.src_addr = smac;
	}

	action rewrite_dmac(bit<48> dmac) {
    	headers.eth_hdr.dst_addr = dmac;
	}

	action set_priority(bit<8> priority){
		standard_metadata.priority = priority;
	}

	action add_measure_opt(){

		headers.measure_hdr.count = headers.measure_hdr.count + 1;

		headers.hdrs_stack.push_front(1);
		headers.hdrs_stack[0].timestamp_1 = (bit<32>)(standard_metadata.time_of_day >> 32);
		headers.hdrs_stack[0].timestamp_2 = (bit<32>)(standard_metadata.time_of_day);
		headers.hdrs_stack[0].timedelta = (bit<32>)(standard_metadata.deq_timedelta);


		headers.hdrs_stack[0].sw_id = meta.switch_metadata.sw_id;


		headers.udp_hdr.length = headers.udp_hdr.length + MEASURE_OPT_LEN;
		headers.ipv4_hdr.total_len = headers.ipv4_hdr.total_len + MEASURE_OPT_LEN;
		meta.ingress_metadata.opt_added = 1;

	}

	table ipv4_lpm {
        key = {
            headers.ipv4_hdr.dst_addr: lpm;
        }
        actions = {
            ipv4_forward;
			drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction(); // dodac drop
	}

	table switch_id {
		actions = {
			add_switch_id;
			NoAction;
		}
        default_action = NoAction();
	}

	table internal_mac {
		key  = {
        standard_metadata.egress_spec: exact;
    	}
		actions = {
			rewrite_smac;
			NoAction;
		}
		default_action = NoAction();
	}


	table external_mac {
		key  = {
        meta.ingress_metadata.next_hop: exact;
    	}
		actions = {
			rewrite_dmac;
			NoAction;
		}
		default_action = NoAction();
	}

	table priority {
		key  = {
			headers.ipv4_hdr.dst_addr: exact;
			headers.ipv4_hdr.src_addr: exact;
			meta.parser_metadata.dst_port: exact;
			meta.parser_metadata.src_port: exact;
			meta.parser_metadata.protocol: exact;
    	}
		actions = {
			set_priority;
			NoAction;
		}
		default_action = NoAction();
	}

	table measure_opts_add {
        key = {
		    headers.measure_hdr.dst_addr: exact;
			headers.measure_hdr.src_addr: exact;
			headers.measure_hdr.dst_port: exact;
			headers.measure_hdr.src_port: exact;
			headers.measure_hdr.protocol: exact;
        }
        actions = {
            add_measure_opt;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
	}


	apply {

			if (headers.ipv4_hdr.isValid()){
				if (headers.ipv4_hdr.ttl < 1)
					drop();
				else {
					/* Packet forwarding */
					ipv4_lpm.apply();
					external_mac.apply();
					internal_mac.apply();

					/* Setting the switch ID */
					switch_id.apply();

					/* Setting priority for packet queueing between ingress and egress */
					priority.apply();

					/*
						Clone doesn't have any forwarding changes + no option is added
						(the original packet is cloned to egress with added metadata)
					*/
					if (headers.measure_hdr.isValid()){
						/*
						Clone doesn't have any forwarding changes + no option is added
						(the original packet is cloned to egress with added metadata)
						*/
						clone3(CloneType.I2E, (bit<32>)32w250, {meta, standard_metadata});
						if (headers.measure_hdr.modify == 1){
							if(headers.measure_hdr.count < MAX_OPTIONS){
								measure_opts_add.apply();
							}
						}
					}


				}
			}

	}

}
