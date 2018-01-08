g++ -o sniffing/headers/ethernet.o -c sniffing/headers/ethernet.cpp -std=c++11
g++ -o sniffing/headers/ipv4.o -c sniffing/headers/ipv4.cpp -std=c++11
g++ -o sniffing/headers/udp.o -c sniffing/headers/udp.cpp -std=c++11
g++ -o sniffing/headers/vxlan.o -c sniffing/headers/vxlan.cpp -std=c++11
g++ -o sniffing/headers/measure_header.o -c sniffing/headers/measure_header.cpp -std=c++11
g++ -o sniffing/headers/measure_option.o -c sniffing/headers/measure_option.cpp -std=c++11
g++ -o sniffing/parser.o -c sniffing/parser.cpp -std=c++11
g++ -o persistance/measure_data.o -c persistance/measure_data.cpp -std=c++11
g++ -o persistance/db_connector.o -c persistance/db_connector.cpp -std=c++11
g++ -o persistance/worker.o -c persistance/worker.cpp -std=c++11
g++ -o config.o -c config.cpp -std=c++11
g++ -o persistance/sla_checker.o -c persistance/sla_checker.cpp -std=c++11 
g++ -o persistance/logging.o -c persistance/logging.cpp -std=c++11
g++ -o sniffing/sniffer.o -c sniffing/sniffer.cpp -std=c++11


g++  sniff.cpp  -o sniff -std=c++11 sniffing/parser.o persistance/db_connector.o persistance/worker.o persistance/sla_checker.o sniffing/sniffer.o persistance/logging.o persistance/measure_data.o sniffing/headers/ethernet.o sniffing/headers/ipv4.o sniffing/headers/vxlan.o sniffing/headers/measure_header.o sniffing/headers/measure_option.o sniffing/headers/udp.o config.o `mysql_config --cflags --libs` -lpcap -L/usr/lib/mysql -lmysqlclient -L.  -levent_core -lamqpcpp
