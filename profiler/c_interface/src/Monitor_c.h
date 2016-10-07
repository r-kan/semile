#ifndef SEMILE_MONITOR_C_H
#define SEMILE_MONITOR_C_H

// the c language interface for semile

void* CreateSemileInstance(const char* func, const char* file, int line);
void DestroySemileInstance(void*);

void AddSemileMessage(void* inst, const char*);

void SetSemileOutputFilename(const char*);

#ifndef SEMILE_DISABLE
#define SEMILE_BEGIN CreateSemileInstance(__func__, __FILE__, __LINE__)
#define SEMILE_BEGIN_N(name) CreateSemileInstance(#name, __FILE__, __LINE__)
#define SEMILE_MSG_C(inst, msg) AddSemileMessage(inst, msg)
#define SEMILE_END(inst) DestroySemileInstance(inst)
#else
#define SEMILE_BEGIN
#define SEMILE_BEGIN_N(name)
#define SEMILE_MSG_C(inst, msg)
#define SEMILE_END(inst)
#endif

#endif

