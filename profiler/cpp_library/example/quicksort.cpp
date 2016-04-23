#include <assert.h>
#include <time.h>
#include <vector>
#include <string>
#include <sstream>
#include <Monitor.h>

using namespace std;
using namespace semile;

void quicksort(vector<int>& x, int start_pos, int end_pos);

void 
quicksort_impl(vector<int>& x, int start_pos, int end_pos)
{
  timespec ts;
  ts.tv_sec = 0;
  ts.tv_nsec = 100000000;
  nanosleep(&ts, NULL);

  if (start_pos < end_pos)
  {
    int pivot = start_pos;
    int i = start_pos;
    int j = end_pos;
    int temp;

    while (i < j)
    {
      while (x[i] <= x[pivot] && i < end_pos) {
        ++i;
      }
      while (x[j] > x[pivot]) {
        --j;
      }
      if (i < j)
      {
        temp = x[i];
        x[i] = x[j];
        x[j] = temp;
      }
    }

    temp = x[pivot];
    x[pivot] = x[j];
    x[j] = temp;
    
    quicksort(x, start_pos, j - 1);
    quicksort(x, j + 1, end_pos);
  }
}

class QuicksortMonitor: public ExecutionMonitor
{
  public:
    QuicksortMonitor(const vector<int>& x, int start_pos, int end_pos):ExecutionMonitor("quicksort", __FILE__, __LINE__) 
    { 
      addMsg(x, start_pos, end_pos);  
    }
    void operator()(vector<int>& x, int start_pos, int end_pos) 
    { 
      return quicksort_impl(x, start_pos, end_pos); 
    }
    void addMsg(const vector<int>& x, int start_pos, int end_pos)
    {  
      stringstream stream;
      for (int i = start_pos; i <= end_pos; ++i) {
        stream << x[i] << " ";
      }
      addMessage(stream.str());
    }
};

void 
quicksort(vector<int>& x, int start_pos, int end_pos)
{
  QuicksortMonitor monitor(x, start_pos, end_pos);
  monitor(x, start_pos, end_pos);
}

