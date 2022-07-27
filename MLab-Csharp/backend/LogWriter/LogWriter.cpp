#include "pch.h"

#include "LogWriter.h"


namespace LogManagement {
	int LogWriter::write_string_to_file_append(const std::string& file_string, const std::string str)
	{
		std::ofstream OsWrite(file_string, std::ofstream::app);
		OsWrite << str;
		OsWrite << std::endl;
		OsWrite.close();
		return 0;
	}
}
