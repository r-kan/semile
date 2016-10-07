#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void quicksort(int*, int, int);

int main()
{
  int valueSize = 7;
  int groupSize = 3;

  srand(time(NULL));

  int i = 0, j = 0;
  for (i = 0; i < groupSize; ++i)
  {
    int x[valueSize];
    for (j = 0; j < valueSize; ++j) {
      x[j] = rand() % (valueSize * groupSize);
    }
    
    quicksort(x, 0 , valueSize - 1);
  }
  
  return 0;
}

