#include "Monitor.h"
#include <sys/time.h> // for 'gettimeofday'
#include <assert.h>
#include <utility> // for 'pair'
#include <deque>
#include <map>
#include <queue>
#include <sstream>
#include <fstream>
#include <iomanip>
#include <ctime>

using namespace std;

namespace semile
{

struct LogEntry
{
  LogEntry(unsigned int no, const string& log):_no(no), _log(log) {}
  unsigned int _no;
  string _log;
  bool _finalized = false;
};

struct CompareLogEntry
{
  bool operator()(const LogEntry* e1, const LogEntry* e2) 
  {
    assert(e1 && e2);
    assert(e1->_no != e2->_no);
    return e1->_no > e2->_no;
  }
};

/*===========================================================
 * *** MonitorLog
 *===========================================================*/

static const char*
GetTimeString()
{
  time_t rawtime;
  time (&rawtime);

  struct tm* timeinfo = localtime(&rawtime);

  static char curtime[80];
  strftime(curtime, 80, "%Y%m%d%H%M%S", timeinfo);

  return curtime;
}

class MonitorLog
{
  public:
    MonitorLog(const string logFile):_logFile(logFile + "_" + GetTimeString()) {}
    ~MonitorLog() { flush(); assert(_logs.empty() && _logQueue.empty()); delete _out; }
    void addFullLog(unsigned int no, const string log);
    void createLog(unsigned int no, const string& log);
    void addAndFinalizeLog(unsigned int no, const string& log);
  private:
    void flush();
    const string _logFile;
    map<unsigned int, LogEntry*> _logs;
    priority_queue<LogEntry*, vector<LogEntry*>, CompareLogEntry> _logQueue;
    ofstream* _out = NULL;
};

void
MonitorLog::flush()
{
  while (true)
  {
    if (_logQueue.empty()) { break; }

    LogEntry* entry = _logQueue.top();
    if (false == entry->_finalized) { break; }

    if (NULL == _out) {
      _out = new ofstream(_logFile);
    }
    (*_out) << entry->_log << endl;
    _logQueue.pop();

    auto entryInMap = _logs.find(entry->_no);
    assert(entryInMap != _logs.end());
    _logs.erase(entryInMap);
    delete entry;
  }
}

void 
MonitorLog::addFullLog(unsigned int no, const string log)
{
  assert(_logs.find(no) == _logs.end());
  LogEntry* entry = new LogEntry(no, log);
  entry->_finalized = true;
  _logs[no] = entry;
  _logQueue.push(entry);
  flush();
}

void 
MonitorLog::createLog(unsigned int no, const string& log)
{
  assert(_logs.find(no) == _logs.end());
  LogEntry* entry = new LogEntry(no, log);
  _logs[no] = entry;
  _logQueue.push(entry);
}

void 
MonitorLog::addAndFinalizeLog(unsigned int no, const string& log)
{
  auto entry = _logs.find(no);
  assert(entry != _logs.end());
  entry->second->_log += log;
  entry->second->_finalized = true;
  flush();
}

/*===========================================================
 * *** GlobalMonitor
 *===========================================================*/

class GlobalMonitor
{
  public:
    GlobalMonitor():_outFile("semile") {}
    ~GlobalMonitor() { delete _out; }
    void pushExecution(const ExecutionMonitor* em);
    void popExecution();
    void setOutFile(const string& filename) { _outFile = filename; }
  private:
    void log(const pair<unsigned int, const ExecutionMonitor*>& emEntry, bool isPush) const;
    string _outFile;
    mutable unsigned int _no = 0;
    deque<pair<unsigned int, const ExecutionMonitor*>> _curExecution; // we use deque as 'stack' here (not use std::stack bcoz it does not provide iterator as we need)
    mutable MonitorLog* _out = NULL;
};

static GlobalMonitor gMonitor;

void SetMonitorOutputFilename(const string& filename) { gMonitor.setOutFile(filename); }

static double 
currentRealTime()
{
  struct timeval tv;
  bool res = gettimeofday(&tv, NULL);
  assert(0 == res);

  return static_cast<double>(tv.tv_sec) + static_cast<double>(tv.tv_usec) / 1000000;
}

void 
GlobalMonitor::log(const pair<unsigned int, const ExecutionMonitor*>& emEntry, bool isPush) const
{
  // out format: +{file_1 function_1 lineNo_1,file_2 function_2 lineNo_2, ...,file_n function_n lineNo_n}+time msg
  stringstream stream;
  stream << "+{";
  for (auto iter = _curExecution.begin(); iter != _curExecution.end(); ++iter)
  {
    const ExecutionMonitor* execution = (*iter).second;
    stream << execution->_file << " " << execution->_function << " " << execution->_lineNo;
    if (iter + 1 != _curExecution.end()) { // not the last entry
      stream << ",";
    }
  }

  stream << "}+";
  stream << fixed << setprecision(9) << currentRealTime() << " ";

  if (NULL == _out) {
    _out = new MonitorLog(_outFile);
  }
  
  if (isPush)
  {
    _out->createLog(emEntry.first, stream.str());
  }
  else
  {
    _out->addAndFinalizeLog(emEntry.first, emEntry.second->_message);
    _out->addFullLog(_no++, stream.str());
  }
}

void 
GlobalMonitor::pushExecution(const ExecutionMonitor* em) 
{ 
  _curExecution.push_back(make_pair(_no++, em));

  log(_curExecution.back(), true);
}

void 
GlobalMonitor::popExecution() 
{ 
  auto entry = _curExecution.back();  
  _curExecution.pop_back();

  log(entry, false);
}

/*===========================================================
 * *** ExecutionMonitor
 *===========================================================*/

static bool gMonitorEnabled = true;
static bool 
IsMonitorEnabled() 
{ 
  static bool isEnvQueried = false; 
  
  if (false == isEnvQueried) 
  { 
    char* envStr = getenv("SEMILE_ENABLE"); 
    if (envStr) 
    { 
      int envVal = atoi(envStr);
      gMonitorEnabled = (envVal >= 1)? true: false;
    } 
    isEnvQueried = true; 
  } 

  return gMonitorEnabled; 
}

ExecutionMonitor::ExecutionMonitor(
  string function, 
  string file, 
  int lineNo)
 :_function(function), 
  _file(file), 
  _lineNo(lineNo)
{
  if (false == IsMonitorEnabled()) { return; }
  
  gMonitor.pushExecution(this);
}

ExecutionMonitor::~ExecutionMonitor() 
{
  if (false == IsMonitorEnabled()) { return; }
  
  gMonitor.popExecution();
}

}

