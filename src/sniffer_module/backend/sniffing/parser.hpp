#ifndef PARSER_HPP
#define PARSER_HPP

#include "../persistance/measure_data.hpp"

using namespace std;

class Parser{
public:

    Parser(MeasureData * measure_data);
    virtual ~Parser(){ }

    void parse(const u_char *buffer, int buf_len);

private:
    MeasureData * measure_data;
    void add_to_list(IHeader * headers);

};
#endif
