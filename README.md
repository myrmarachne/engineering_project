# Leveraging network programming techniques for quality of service assurance

## Introduction
Along with the rapid growth of modern networks and the emerging idea of network convergence, the network management becomes much more complex and requires many specialized tools, especially in terms of implementing appropriate Quality of Service policies.
The emerging idea of Software Defined Networking (SDN) is arising to solve these problems. The application of the programmable data plane may help to optimize the already existing solutions or even help to develop new ones.
In my enginnering thesis I proposed an architecture of a system, that could ease the process of implementing the QoS policies, using SDN and programmable data planes.

## Overview
The aim of the presented project was to propose a set of network tools - a system based upon Software Defined Networking technologies and programmable data planes, which would allow to monitor the values of selected Quality of Service parameters and eventually modify the network actions, in order to provide a certain level of QoS parameters.
The system is created based upon virtual network devices and open-source SDN technology standards. It provides API for distributed applications, which allows to collect necessary measurements used to obtain the values of specific QoS one-way parameters. The measurements are provided in an easy-readable form, which simplifies the process of data analysis.

### Proposed architecture
The system is divided into three main subsystems - Data Analysis, Real time Analysis and Tagging Subsystem. The Data Analysis Subsystem consists of desktop application generating graphs and providing data statistics. The Real time Analysis Subsystem consist of applications that continuously monitor the network - they analyze the obtained measurements. In case of failure these applications will react as fast as possible to change the default behavior of network to maintain the necessary level of Quality of Service. Moreover, all of the measurements are saved in database, so that it is possible to create statistics based on them. The logic of this subsystem is decentralized, divided between many network units. The Tagging Subsystem consists of the switches data plane software. It allows creating specific headers containing the necessary measurements, as well as deleting them in order to obtain original packets. It is possible to change the QoS policy during switch operation.
In order to start monitoring and ensuring specific values of Quality of Service parameters it is required to add basic configuration on the switch - parameters to identify the flow, that need to be monitored and tagged with specially defined headers, using interactive switch CLI.
Afterwards, the parameters of server connection should be provided. After this configuration it is possible to run application analyzing data, which would generate appropriate graphs and statistics.

### Functional principle
The system consists of 6 modules: data analysis module, control module, communication module (to communicate with persistence module), persistence module, capturing module and tagging module.
The key functionality is provided by the tagging module - it is responsible for creating new headers containing specific measurements and encapsulating original packets with them.
When the switch recognizes packets belonging to the monitored flow it creates the Measurement Header and Measurement Option headers with appropriate measurements and timestamps and encapsulates original packets.
According to the flow specific configuration, some of the switches on the path of the packet (possibly all, at least two - the first and last one) add their own Measurement Options with ingress timestamps. The last configured switch in the path decapsulates the packet, collects the measurements and sends then them to the modules of Real Time Analysis subsystem.

### Technology stack
The test environment was created using Mininet (with python) and library scapy (to generate network traffic).

#### Data analysis module and Communication module
Both modules were created in python, the graphical user interfaces were created using the PyQt 5.

#### Control module
Communication between the control module and the persistance module, and communication between the control module and data analysis module was implemented using python and library pika (control module side) and using C++11 and library AMQP CPP (persistance module side).

#### Persistance module and Capturing module
These modules were created in C++11 using, among others following libraries: AMQP CPP, RapidJSON, MySQL C API, libpcap. Data was written in MariaDB database.

#### Tagging module
The tagging module was created using the P4_16 language with Behavioral Model version 2. 

## Installation
This installation guide was created for Ubuntu (14.04+). In order to install the project correctly, all needed dependecies should be resolved. In case of using Ubuntu the `install_deps.sh` can be used to achieve it.

The first step would be installing the Behavioral model 2 and compilator p4c. 

In order to use the desktop applcation it is also needed to install python (3.5+) and PyQt 5. On Ubuntu it can be achieved through `apt-get install python3-pyqt5`. All other python dependencies can be installed using pip and the requirements.txt file, which can be found in src/analyze_data.

The application also need MySQL and RabbitMQ servers to be installed, as well as the MySQL client (` apt-get install libmysqlclient-dev`). 

The sniffer module needs the AMQP CPP. Installation guide of this library can be found under following link: https://github.com/CopernicaMarketingSoftware/AMQP-CPP. In order to compile the project the GCC with libpcap and libevent are needed. 

In order to configure and compile the whole system run the script `configure.sh` and `make`.
