// ATLSimpleObject.cpp: CATLSimpleObject 的实现

#include "pch.h"
#include "ATLSimpleObject.h"
#include "dllmain.h"


// CATLSimpleObject



int CATLSimpleObject::hashContainerIdToPort(char* containerId)
{
    // TODO: 在此处添加实现代码.
	unsigned int seed = 131;
	unsigned int hash = 0;
	while (*containerId)
	{
		hash = hash * seed + (*containerId++);
	}
	hash = hash & 0x7FFFFFFF;
	return 20000 + (hash % 10000);
    return 0;
}
