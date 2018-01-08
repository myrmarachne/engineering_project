/*
  Class responsible for buffering measure data and writing them to database
  after timeout
  */
#include "worker.hpp"


#include <iostream> //DO TESTOOOOOOOOOOOOW

Worker::Worker(db_struct_t db_struct){
    if (!set_up_db(db_struct)){
        throw "Setting up the data base connector failed";
    }
};


void Worker::sla_check(SLAConnectionHandler * handler){
  this->sla_handler = handler;
}

void Worker::run(MeasureData * measure_data){

  /* Initialize logger */
  logger = new Logger();

  while (this->work) {
    /* Set timer for getting data */
    measure_data->set_buf_timer(work);
    if (measure_data != nullptr && this->work){
      append(measure_data->get_list());
    }
    else stop();
    }
}

void Worker::stop(){
  this->work = false;
}


void Worker::listen(MeasureData * measure_data){

  if (measure_data->register_worker(this))
    run(measure_data);

}

void Worker::append(list<IHeader *> headers){
    int measurement_ID = -1;
    buffer.splice(buffer.end(), headers);

    list<IHeader *>::iterator iter = buffer.begin();

    string flow = "";
    uint64_t enqueue[MAX_OPTIONS];
    uint64_t timestamps[MAX_OPTIONS];
    long switchIDs[MAX_OPTIONS];
    int pointer = 0; /* points to the next empty cell in above tables */

    while(iter != buffer.end()){
        if ((*iter)->option == true){
          /* Measure Option */

          if (measurement_ID != -1){
            /* Last measurment header was added successfully */
            Option * mo = dynamic_cast<Option*>(*iter);
            mo->measurement_ID = measurement_ID;

            /* Option was added successfully and can be removed from buffer: */
            uint64_t temp = insert_option(mo, measurement_ID);

            enqueue[pointer] = ntohl((*mo->fields).timedelta);
            timestamps[pointer] = temp;
            switchIDs[pointer] = ntohl((*mo->fields).sw_id);
            pointer++;

            if (temp != -1)
                iter = buffer.erase(iter);
            else ++iter;

          } else ++iter;

        } else {
          /* Measure Header */

          MeasureHeader * mh = dynamic_cast<MeasureHeader*>(*iter);

          sla_params parameters;

          if (this->sla_handler != nullptr){
            parameters = sla_handler->get_sla(flow);
          }
          cout<<"param "<<parameters.delay.alert<<" "<<parameters.delay.warning<<endl;
          if (flow != "" && parameters.delay.alert > 0 && parameters.delay.warning > 0){
            /* It\"s next Measure Header - put into logger the current delay and flow */
            /******** TODO *********/
            --pointer;

            if (pointer > 0){
                /* There are at leat two options added */
                if (timestamps[0] > 0 && timestamps[pointer] > 0){
                    /* Both options were added successfully */
                    /* Calculate delay as timestamps[pointer] - timestamps[0] */
                    uint64_t delay = timestamps[0] - timestamps[pointer];

                //    for (int i=0; i<=pointer;i++)
                  //    cout<<timestamps[i]<<endl;
                    /* Check SLA */



                    cout<<parameters.delay.alert <<" "<< delay<<endl;

                    /* Compare SLA value with current delay */
                    if (parameters.delay.alert <= delay){
                        /* Handle error */
                        for (int i=0; i<=pointer; i++){
                          char buffer[300];
                          snprintf(buffer, sizeof(buffer), "[%ld] [%s] [switch: %ld] [enqueue: %ld] delay: %ld ", timestamps[i], flow.c_str(), switchIDs[i], enqueue[i], delay);
                          string s = buffer;
                          logger->log_error(s);
                        }

                        alert[flow] = true;

                        char msg_buf[300];
                        snprintf(msg_buf, sizeof(msg_buf), "{\"seq_nr\" : %d, \"delay\" : %ld, \"state\": \"ALERT\", \"created\" : \"%ld\"}", ntohs((*mh->fields).seq_nr), delay, switchIDs[pointer]);
                        string msg = msg_buf;

                        logger->send("topic_logs3", "measured."+flow, msg);

                    } else if (parameters.delay.warning <= delay){
                        /* Handle warning */
                        /**** TODO ***/

                        for (int i=0; i<=pointer; i++){
                          char buffer[300];
                          snprintf(buffer, sizeof(buffer), "[%ld] [%s] [switch: %ld] [enqueue: %ld] delay: %ld ", timestamps[i], flow.c_str(), switchIDs[i], enqueue[i], delay);
                          string s = buffer;
                          logger->log_warning(s);
                        }

                        alert[flow] = true;

                        char msg_buf[300];
                        snprintf(msg_buf, sizeof(msg_buf), "{\"seq_nr\" : %d, \"delay\" : %ld, \"state\": \"WARNING\", \"created\" : \"%ld\"}", ntohs((*mh->fields).seq_nr), delay, switchIDs[pointer]);
                        string msg = msg_buf;

                        logger->send("topic_logs3", "measured."+flow, msg);

                    }
                    else if (alert.count(flow) > 0 && alert[flow]){
                      alert[flow] = false;

                      char msg_buf[300];
                      snprintf(msg_buf, sizeof(msg_buf), "{\"seq_nr\" : %d, \"delay\" : %ld, \"state\": \"OK\", \"created\" : \"%ld\"}", ntohs((*mh->fields).seq_nr), delay, switchIDs[pointer]);
                      string msg = msg_buf;

                      logger->send("topic_logs3", "measured."+flow, msg);

                    }


                }
            }


          }
          flow = get_flow_string(mh);
          /* Measure header was added successfully - it could be removed from buffer: */
          if ((measurement_ID = insert_measure_header(mh)) != -1)
            iter = buffer.erase(iter);
          else ++iter;
          pointer = 0;

        }
      }
      if (flow != ""){
        /* There exists one more measure header */


      }


}

string Worker::get_flow_string(MeasureHeader * mh){
  string ip_src, ip_dst;


  ip_src = inet_ntoa((*mh->fields).ip_src);
  ip_dst = inet_ntoa((*mh->fields).ip_dst);

  string port1, port2;
  string protocol;

  port1 = to_string(ntohs((*mh->fields).src_port));
  port2 = to_string(ntohs((*mh->fields).dst_port));

  protocol = to_string((*mh->fields).protocol);

  string flow = ip_dst + "." + ip_src + "." + port2 + "." + port1 + "." + protocol;
  return flow;
}

uint64_t Worker::insert_option(Option * mo, int measurement_ID){
  /* Return -1 in case of failure and timestamp for success */

  /* Value according to current implementation of p */

  int64_t one_64bits = 1;

  uint64_t timestamp = (((uint64_t) htonl((*mo->fields).timestamp_1) << 32) + htonl((*mo->fields).timestamp_2)) * (1e9) / (one_64bits << 32);
  if (add_to_options(measurement_ID, timestamp, ntohl((*mo->fields).timedelta), ntohl((*mo->fields).sw_id)) == -1)
    return -1;
  else return timestamp;
}

int Worker::insert_measure_header(MeasureHeader * mh){
/*  Returns Measurment ID or -1 in case of failure */
  long long ID = mh->flow_ID;
  bool swapped = false;

  if (mh->flow_ID == -1){

      /* Add to Applications Table */
      uint16_t port1, port2;
      uint8_t protocol;

      if (ntohs((*mh->fields).src_port) < ntohs((*mh->fields).dst_port)){
        port1 = ntohs((*mh->fields).src_port);
        port2 = ntohs((*mh->fields).dst_port);
      } else {
        port2 = ntohs((*mh->fields).src_port);
        port1 = ntohs((*mh->fields).dst_port);
        swapped = true;
      }


      protocol = (*mh->fields).protocol;

      /* Applications ID */
      if ((ID = add_to_applications(protocol, port1, port2)) == -1)
        return -1;

      /* Add to Measurments Header */
      mh->flow_ID = ID;
  }

  int measurement_ID = add_to_measurments(ID, swapped, inet_ntoa((*mh->fields).ip_src), inet_ntoa((*mh->fields).ip_dst), ntohs((*mh->fields).seq_nr));
  return measurement_ID;
}
