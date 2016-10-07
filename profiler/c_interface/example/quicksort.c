#include <assert.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <Monitor_c.h>


char gbuf[100];

static char* 
GetStr(int* x, int start_pos, int end_pos, char end_line)
{  
  memset(gbuf, 0, 100);
  int i = 0, off = 0;
  for (i = start_pos; i <= end_pos; ++i) {
    off += sprintf(gbuf + off, "%i ", x[i]);
    if (end_line && i == end_pos) { sprintf(gbuf + off, "\\n"); }
  }  
  return gbuf;
}

static char* 
GetStr2(int value, char end_line)
{  
  int off = sprintf(gbuf, "%i", value);
  if (end_line) { sprintf(gbuf + off, "\\n"); }
  return gbuf;
}

static void
Swap(int* x, int i, int j)
{
  int temp = x[i];
  x[i] = x[j];
  x[j] = temp;
}

void 
quicksort(int* x, int start_pos, int end_pos)
{ 
  void* inst = SEMILE_BEGIN_N(abc);
  SEMILE_MSG_C(inst, GetStr(x, start_pos, end_pos, 1));

  struct timespec ts;
  ts.tv_sec = 0;
  ts.tv_nsec = 100000000;
  nanosleep(&ts, NULL);

  char buf[100];
  if (start_pos < end_pos)
  {
    int pivot = start_pos;
    int off = sprintf(buf, "pivot: ");
    sprintf(buf + off, "%s", GetStr2(x[pivot], 1));
    SEMILE_MSG_C(inst, buf);
    
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
        int off = sprintf(buf, "%s <=> ", GetStr2(x[i], 0));
        sprintf(buf + off, "%s\\n", GetStr2(x[j], 0));
        SEMILE_MSG_C(inst, buf);
        Swap(x, i, j);
      }
    }

    if (j != pivot)
    {
      int off = sprintf(buf, "%s <=> ", GetStr2(x[pivot], 0));
      sprintf(buf + off, "%s\\n", GetStr2(x[j], 0));
      SEMILE_MSG_C(inst, buf);
      Swap(x, pivot, j);   
    }
    
    quicksort(x, start_pos, j - 1);
    quicksort(x, j + 1, end_pos);
  }

  SEMILE_MSG_C(inst, GetStr(x, start_pos, end_pos, 0));
  SEMILE_END(inst);
}

