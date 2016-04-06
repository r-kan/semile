#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <vector>

using namespace std;

void quicksort(vector<int>&, int, int);

int main()
{
  int valueSize = 7;
  int groupSize = 3;

  srand(time(NULL));

  for (int i = 0; i < groupSize; ++i)
  {
    vector<int> x;
    for (int j = 0; j < valueSize; ++j) {
      x.push_back(rand() % (valueSize * groupSize));
    }
    
    quicksort(x, 0 , valueSize - 1);
  }
  
  return 0;
}

