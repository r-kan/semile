#ifndef MONITOR_H
#define MONITOR_H

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
  protected:
    void addMessage(const std::string message) { _message += message; }
    const std::string _function;
    const std::string _file;
    const int _lineNo;
    std::string _message;
};

void SetDisableMonitor(bool disable);
void SetMonitorOutputFilename(const std::string&);

}

#endif

