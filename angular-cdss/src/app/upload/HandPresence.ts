export class HandPresence
{
	L:number;
	R:number;
	Empty:number;
	B:number; // Both hands in frame
	num_L:number;
	num_R:number;
	num_empty:number;
	frames:number;

	constructor(L, R, Empty, B, num_L, num_R, num_empty, frames)
	{
		this.L = L;
		this.R = R;
		this.Empty = Empty;
		this.B = B;
		this.num_L = num_L;
		this.num_R = num_R;
		this.num_empty = num_empty;
		this.frames = frames;
	}
}