#include "sniffer.hpp"

using namespace std;


void Sniffer::error(const char* function_name){
  printf("[%s]: \n", function_name);
  exit(1);
}

void Sniffer::error_buf(const char* function_name, char *errbuf){
  printf("[%s]: %s\n", function_name, errbuf);
  exit(1);
}

void callback(uint8_t *args, const struct pcap_pkthdr *header, const u_char *packet){
  Parser * parser = (Parser *) args;
  parser->parse(packet, header->len);
}

void Sniffer::sniff(string dev_name){
  /* Setting up sniffing on Interface */

  pcap_t *handle;
  int fd;
  struct pollfd fds[1];

  /* Array filled with appropriate error messages */
  char errbuf[PCAP_ERRBUF_SIZE];

  /* Obtaining packet capture handle, no timeout, promiscuous mode */
  handle = pcap_open_live(dev_name.c_str(), SNAPSHOT_LENGTH, 1, 1000, errbuf);
  if (handle == nullptr)
      error_buf("pcap_open_live", errbuf);

  if (pcap_setnonblock(handle, 1, errbuf) == -1)
      error_buf("pcap_setnonblock", errbuf);

  if ((fd = pcap_get_selectable_fd(handle)) == -1)
    error_buf("pcap_get_selectable_fd", errbuf);

  /* Setting filter for traffic to udp with destination port 4790 */
  char filter_exp[] = "udp dst port 4790";
  struct bpf_program fp;

  /* Compile the filter expression */
   if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == -1)
    error_buf("pcap_compile", errbuf);

   /* Apply the compiled filter */
   if (pcap_setfilter(handle, &fp) == -1)
      error_buf("pcap_setfilter", errbuf);

  while (true) {

    memset(fds, 0 , sizeof(fds));

    fds[0].fd = fd;
    fds[0].events = POLLIN;
    fds[0].revents = 0;

    if (poll(fds, 1, 1000) < 0)
      printf("%s\n", "There was en error caused by select()");
    else{
      if (pcap_dispatch(handle, -1, callback, (u_char *)parser) == -1)
        error("pcap_dispatch");
    }
  }
}
