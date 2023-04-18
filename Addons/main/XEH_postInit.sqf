#include "script_component.hpp"

private _onSubmitReviewId = ["onSubmitReview", {
	params ["_message", "_player"]; 

	[_message, _player] call FUNC(submitReview);
	
}] call CBA_fnc_addEventHandler;

// private _onSubmitBugReportId = ["onSubmitBugReport", {systemChat str _this}] call CBA_fnc_addEventHandler;

// private _onSubmitRatingId = ["onSubmitRating", {systemChat str _this}] call CBA_fnc_addEventHandler;