#ifndef HEADER_HPP
#define HEADER_HPP

#include <netinet/in.h>

class IHeader{
public:
  virtual ~IHeader(){ }
  IHeader * next = nullptr;
  virtual bool parse (const u_char *buffer, int buf_len){ };
  virtual void set_next() { };
  bool measure_data = false;
  bool option = false;

};

template<class T>
class Header : public IHeader{
public:

    Header(int buff_offset){
      this->buff_offset = buff_offset;
    }

    Header(){
      Header(0);
    }

    virtual ~Header(){ }
    bool parse (const u_char *buffer, int buf_len);
    T * fields = nullptr;


protected:
  bool check_len(int buf_len);
  int buff_offset;
  virtual int length(){ };

};
#endif
