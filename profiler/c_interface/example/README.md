Use the following to give profile specificaiton
* **SEMILE_BEGIN**: to allocate a profile resource  
* **SEMILE_BEGIN_N(**_abc_**)**: to allocate a profile resource with name _abc_  
* **SEMILE_END**: to release a profile resource  
* **SEMILE_MSG_C**: to add debug message  


Check <a href='https://github.com/r-kan/semile/blob/master/profiler/c_interface/example/quicksort.c'>quicksort.c</a> for a complete example with code snippet:
```c
void quicksort(int* x, int start_pos, int end_pos)
{
  void* inst = SEMILE_BEGIN;
  SEMILE_MSG_C(inst, GetStr(x, start_pos, end_pos));
  ...
  SEMILE_END(inst);
}
```
