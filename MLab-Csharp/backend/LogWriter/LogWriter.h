#pragma once

#include <fstream> 
#include <iostream>
#include <string>

using namespace std;

namespace LogManagement {
	public ref class LogWriter
	{
		int write_string_to_file_append(const std::string& file_string, const std::string str);
	};
}
