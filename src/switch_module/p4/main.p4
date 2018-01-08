/* -*- P4_16 -*- */

#include <core.p4>
#include <v1model.p4>

#include "headers.p4"
#include "parser.p4"
#include "checksum_verification.p4"
#include "ingress.p4"
#include "egress.p4"
#include "checksum_compute.p4"
#include "deparser.p4"

V1Switch(
	TopParser(), checksumVerification(), TopIngress(),
	TopEgress(), computeChecksum(), TopDeparser()
) main;
