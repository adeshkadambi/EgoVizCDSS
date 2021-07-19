import { InteractionType } from "./InteractionType";

export class HandObjInt
{
	l_dur:InteractionType
	r_dur:InteractionType
	l_int:InteractionType
	r_int:InteractionType
	l_num:InteractionType
	r_num:InteractionType

	constructor(l_dur, r_dur, l_int, r_int, l_num, r_num)
	{
		this.l_dur = l_dur;
		this.r_dur = r_dur;
		this.l_int = l_int;
		this.r_int = r_int;
		this.l_num = l_num;
		this.r_num = r_num;
	}

	get_labels() {
		return ["l_dur", "r_dur", "l_int", "r_int", "l_num", "r_num"];	
	}

	get_labelmap() {
		return {
			"l_int":"[L] Interaction proportion (%)",
			"r_int":"[R] Interaction proportion (%)",
			"l_dur":"[L] Avg. Interaction Duration (s)",
			"r_dur":"[R] Avg. Interaction Duration (s)",
			"l_num":"[L] Number of Interactions per hour (#/hr)",
			"r_num":"[R] Number of Interactions per hour (#/hr)",
		}
	}
}