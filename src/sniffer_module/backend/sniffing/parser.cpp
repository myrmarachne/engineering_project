#include "parser.hpp"

Parser::Parser(MeasureData * measure_data){
  this->measure_data = measure_data;
}

void Parser::parse(const u_char *buffer, int buf_len){

  bool measure_flag = false;

  /* Parsing starts always from ethernet Header */
  IHeader * headers = new EthernetHeader();
  headers->parse(buffer, buf_len);
  headers->set_next();

  IHeader * temp = nullptr; /* pointer to parsed headers linked list */

  temp = headers->next;

  while(temp != nullptr){
      temp->parse(buffer, buf_len);
      temp->set_next();
      if(!measure_flag && temp->measure_data){
        measure_flag = true;
        headers = temp;
      }
      temp = temp->next;
  }

  if (measure_flag) add_to_list(headers);

}

void Parser::add_to_list(IHeader * headers){
  IHeader * temp = headers;
  list<IHeader *> m_hdrs;

  while(temp != nullptr){

      /*
        Writing only packets with measure data to the measure_data buffer
        (linked list) - measure headers (headers with measure_data flag set to
        true) from the linked list with all parsed headers are being moved to
        the measure_buff list
      */

    if(temp->measure_data)
       m_hdrs.push_back(temp);
    temp = temp->next;
  }

  if (measure_data != nullptr)
    measure_data->append(m_hdrs);

}
