--Initialization script for the Mission lua Environment (SSE)

dofile('Scripts/ScriptingSystem.lua')

-- Add LuaSocket to the LUAPATH, so that it can be found.
package.path  = package.path..";.\\LuaSocket\\?.lua;"

--Sanitize Mission Scripting environment
--This makes unavailable some unsecure functions. 
--Mission downloaded from server to client may contain potentialy harmful lua code that may use these functions.
--You can remove the code below and make availble these functions at your own risk.

local function sanitizeModule(name)
	local veafName = "veafSanitized_"..name
	_G[veafName] = _G[name]
	package.loaded[veafName] = package.loaded[name]
	_G[name] = nil
	package.loaded[name] = nil
end

do
	witchcraft = {}
	witchcraft.host = "localhost"
	witchcraft.port = 3001
	dofile(lfs.writedir().."Scripts\\witchcraft.lua")
end
	
do
	sanitizeModule('os')
	sanitizeModule('io')
	sanitizeModule('lfs')
	require = nil
	loadlib = nil
end