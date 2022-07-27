// dllmain.h: 模块类的声明。

class CCOMLibModule : public ATL::CAtlDllModuleT< CCOMLibModule >
{
public :
	DECLARE_LIBID(LIBID_COMLibLib)
	DECLARE_REGISTRY_APPID_RESOURCEID(IDR_COMLIB, "{456f5dd1-d5f9-4c20-b9cd-d5a7c55ae12d}")

	int hashContainerIdToPort(char* containerId);
};

extern class CCOMLibModule _AtlModule;
