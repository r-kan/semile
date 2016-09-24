#ifndef SEMILE_MONITOR_H
#define SEMILE_MONITOR_H

#include <string>

namespace semile
{

class GlobalMonitor;

class ExecutionMonitor
{
  friend class GlobalMonitor;
  public:
    ExecutionMonitor(std::string function, 
                          std::string file, 
                          int lineNo);
    virtual ~ExecutionMonitor();
    void addMessage(const std::string message) { _message += message; }
  protected:
    const std::string _function;
    const std::string _file;
    const int _lineNo;
    std::string _message;
};

void SetDisableMonitor(bool disable);
void SetMonitorOutputFilename(const std::string&);

}

#define SEMILE_INST_NAME semile_ax0by1 // a messy name to not pollute namespace too much (:>)
#define SEMILE semile::ExecutionMonitor SEMILE_INST_NAME = semile::ExecutionMonitor(__func__, __FILE__, __LINE__)
#define SEMILE_N(name) semile::ExecutionMonitor SEMILE_INST_NAME = semile::ExecutionMonitor(#name, __FILE__, __LINE__)
#define SEMILE_MSG(msg) SEMILE_INST_NAME.addMessage(msg)

#endif

