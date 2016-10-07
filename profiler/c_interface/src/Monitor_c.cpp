extern "C"
{
#include "Monitor_c.h"
}
#include <string>
#include "Monitor.h"
#include <assert.h>

using namespace std;
using namespace semile;

void* 
CreateSemileInstance(const char* func, const char* file, int line)
{
  return new semile::ExecutionMonitor(func, file, line);
}

void 
DestroySemileInstance(void* inst_)
{
  semile::ExecutionMonitor* inst = static_cast<semile::ExecutionMonitor*>(inst_);
  delete inst;
}

void 
AddSemileMessage(void* inst_, const char* msg)
{
  assert(inst_);
  semile::ExecutionMonitor* inst = static_cast<semile::ExecutionMonitor*>(inst_);
  inst->addMessage(msg);
}

void 
SetSemileOutputFilename(const char* name_)
{
  const string name = name_;
  SetMonitorOutputFilename(name);
}

