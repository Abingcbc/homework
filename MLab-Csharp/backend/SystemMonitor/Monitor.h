#pragma once

#include <iostream> 
#include <string>
#include <string.h>
#include <winsock2.h> // include must before window.h
#include <iphlpapi.h>
#include <windows.h>  

static const int kMaxInfoBuffer = 256;
#define  GBYTES  1073741824  
#define  MBYTES  1048576  
#define  KBYTES  1024  
#define  DKBYTES 1024.0

extern "C"
{
	__declspec(dllexport) std::string __stdcall getMemoryInfo()
	{
		std::string memory_info;
		MEMORYSTATUSEX statusex;
		statusex.dwLength = sizeof(statusex);
		if (GlobalMemoryStatusEx(&statusex))
		{
			unsigned long long total = 0, remain_total = 0, avl = 0, remain_avl = 0;
			double decimal_total = 0, decimal_avl = 0;
			remain_total = statusex.ullTotalPhys % GBYTES;
			total = statusex.ullTotalPhys / GBYTES;
			avl = statusex.ullAvailPhys / GBYTES;
			remain_avl = statusex.ullAvailPhys % GBYTES;
			if (remain_total > 0)
				decimal_total = (remain_total / MBYTES) / DKBYTES;
			if (remain_avl > 0)
				decimal_avl = (remain_avl / MBYTES) / DKBYTES;

			decimal_total += (double)total;
			decimal_avl += (double)avl;
			char  buffer[kMaxInfoBuffer];
			sprintf_s(buffer, kMaxInfoBuffer, "total %.2f GB (%.2f GB available)", decimal_total, decimal_avl);
			memory_info.append(buffer);
		}
		std::cout << memory_info << std::endl;
		return memory_info;
	}

}