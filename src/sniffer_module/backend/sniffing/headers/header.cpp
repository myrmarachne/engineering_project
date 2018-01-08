#include "header.hpp"

template<class T>
bool Header<T>::check_len(int buf_len){
  if (buff_offset + length() > buf_len) return false;
  else return true;
}

template<class T>
bool Header<T>::parse(const u_char *buffer, int buf_len){
   if (check_len(buf_len)){
     fields = (T *) (buffer + buff_offset);
     return true;
   }
   return false;
}
