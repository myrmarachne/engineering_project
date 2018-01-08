#ifndef MEASURE_DATA_HPP
#define  MEASURE_DATA_HPP

#include "../sniffing/headers/measure_option.hpp"
#include "../config.hpp"

#include <chrono>
#include <mutex>
#include <list>
#include <vector>
#include <algorithm>
#include <condition_variable>

using namespace std;

class Worker;

class MeasureData{

public:

  MeasureData(md_struct_t md_struct);
  virtual ~MeasureData();

  void append(list<IHeader *> & headers);
  list<IHeader *> get_list();

  /*
    Functions for registering and unregistring workers for events connected
    with getting data from buffer
  */
  bool register_worker(Worker * worker);
  void unregister_worker(Worker * worker);

  void set_up(md_struct_t md_struct);

  void set_buf_timer(bool & continue_work);


private:
  /*
    Vector of registered workers observing the Measure Data class (with
    corresponding mutex)
  */
  mutex workers_mtx;
  vector<Worker *> workers;

  /*
    List of headers of packets, which are measure data headers and options (with
    corresponding mutex)
  */
  mutex buffer_mutex;
  list<IHeader*> buffer;

  /*
    Mutex and condition variable for setting timeout for multiple workers
    for accessing the main buffer
  */
  mutex time_mutex;
  condition_variable work;

  /* MeasureData parameters with their mutex */
  long long seconds;
  int max_workers;
  int max_size;
  mutex param_mtx;

  void on_buffer_add();

  /* Function for parsing time to seconds */
  long long to_seconds(int hours, int minutes, int seconds);


};

#endif
