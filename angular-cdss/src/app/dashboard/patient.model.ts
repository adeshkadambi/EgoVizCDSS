export interface Patient {
    id: string;
    age: number;
    description: string;
    doctor: string;
}

export interface Data {
    name: Date;
    value: number;
}

export interface LineGraph {
    name: string;
    series: Data[];
}