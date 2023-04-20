#include "script_component.hpp"

params [
	["_message", "", [""]],
	["_unit", objNull, [objNull]]
];

if (_message == "" || _unit == objNull) exitWith {};





private _thread_id = ["gc_websitefunctions.call_submit_review", [_message, getPlayerUID _unit, missionName]] call py3_fnc_callExtension;
private _has_call_finished = ["gc_websitefunctions.has_call_finished", [_thread_id]] call py3_fnc_callExtension;

[
	{
		private _thread_id_pfh = _this getVariable "params" select 0;
		private _has_call_finished_pfh = ["gc_websitefunctions.has_call_finished", [_thread_id_pfh]] call py3_fnc_callExtension;
		if (_has_call_finished_pfh) then {
			(_this getVariable "params") set [1, true];
		};
	},
	1,
	[_thread_id, _has_call_finished, _unit],
	{
		
	},
	{
		private _value = ["gc_websitefunctions.get_call_value", [_this getVariable "params" select 0]] call py3_fnc_callExtension;
		["reviewResponse", [_value], _this getVariable "params" select 2] call CBA_fnc_targetEvent;
	},
	{
		!(_this getVariable "params" select 1); // ?????
	},
	{
		_this getVariable "params" select 1; // ?????
	}

] call CBA_fnc_createPerFrameHandlerObject;