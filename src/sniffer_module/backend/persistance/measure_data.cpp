#include "measure_data.hpp"

MeasureData::~MeasureData(){

  /* Apply workers mutex to disable registering of new workers */
  unique_lock<mutex> lck(workers_mtx);

  while(!workers.empty())
    workers.pop_back();       /* Delete worker from the vector */

  work.notify_all(); /* Wake all sleeping workers */
}

MeasureData::MeasureData(md_struct_t md_struct){
  set_up(md_struct);
}

void MeasureData::set_up(md_struct_t md_struct){
  unique_lock<mutex> lck(param_mtx);

  this->max_size = md_struct.MAX_SIZE;

  if (md_struct.MAX_WORKERS > this->max_workers)
    this->max_workers = md_struct.MAX_WORKERS;

  this->seconds = to_seconds(md_struct.HOURS, md_struct.MINUTES, md_struct.SECONDS);

  lck.unlock();

  on_buffer_add();

}

void MeasureData::append(list<IHeader *> & headers){
  unique_lock<mutex> lck(buffer_mutex);
  buffer.splice(buffer.end(), headers);
  on_buffer_add();
}

list<IHeader *> MeasureData::get_list(){
  unique_lock<mutex> lck(buffer_mutex);
  list<IHeader *> headers;
  headers.splice(headers.end(), buffer);
  lck.unlock();
  return headers;
}


bool MeasureData::register_worker(Worker * worker){

  unique_lock<mutex> lck(workers_mtx);
  if (workers.size() < max_workers){

    try {
      workers.push_back(worker);

      return true;
    } catch (const std::bad_alloc &){
      /* Problem with memory allocation */
      return false;
    } catch (const std::exception &){
      /* Any other exception while adding the element to vector occured */
      return false;
    } catch (...){
      return false;
    }
  } else return false;

  lck.unlock();
}

void MeasureData::unregister_worker(Worker * worker){
  unique_lock<mutex> lck(workers_mtx);
  workers.erase(std::remove(workers.begin(), workers.end(), worker), workers.end());
  lck.unlock();
}


void MeasureData::on_buffer_add(){
  if (buffer.size() > max_size)
    work.notify_one();
}

void MeasureData::set_buf_timer(bool & continue_work){
  unique_lock<mutex> lck(time_mutex);
  while (continue_work && buffer.empty())
    work.wait_for(lck, chrono::seconds(10));
}

long long MeasureData::to_seconds(int hours, int minutes, int seconds){
 return (seconds + minutes * 60 + hours * 3600);
}
