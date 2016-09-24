#include <assert.h>
#include <time.h>
#include <vector>
#include <string>
#include <sstream>
#include <Monitor.h>

using namespace std;

static string 
GetStr(const vector<int>& x, int start_pos, int end_pos, bool end_line = true)
{  
  static stringstream stream;
  stream.str("");
  for (int i = start_pos; i <= end_pos; ++i) {
    stream << x[i] << " ";
    if (end_line && i == end_pos) { stream << "\\n"; }
  }  
  return stream.str();
}

static string 
GetStr(int value)
{  
  static stringstream stream;
  stream.str("");
  stream << value;
  return stream.str();
}

static void
Swap(vector<int>& x, int i, int j)
{
  int temp = x[i];
  x[i] = x[j];
  x[j] = temp;
}

void 
quicksort(vector<int>& x, int start_pos, int end_pos)
{ 
  SEMILE_N(abc);
  SEMILE_MSG(GetStr(x, start_pos, end_pos));

  timespec ts;
  ts.tv_sec = 0;
  ts.tv_nsec = 100000000;
  nanosleep(&ts, NULL);

  if (start_pos < end_pos)
  {
    int pivot = start_pos;
    SEMILE_MSG("pivot: " + GetStr(x[pivot]) + "\\n");
    
    int i = start_pos;
    int j = end_pos;

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
        SEMILE_MSG(GetStr(x[i]) + " <=> " + GetStr(x[j]) + "\\n");
        Swap(x, i, j);
      }
    }

    if (j != pivot)
    {
      SEMILE_MSG(GetStr(x[pivot]) + " <=> " + GetStr(x[j]) + "\\n");
      Swap(x, pivot, j);   
    }
    
    quicksort(x, start_pos, j - 1);
    quicksort(x, j + 1, end_pos);
  }

  SEMILE_MSG(GetStr(x, start_pos, end_pos, false));
}

