export interface Patient {
    id: string;
    age: number;
    description: string;
    doctor: string;
}

export interface Data<K> {
    "name": K;
    "value": number;
    "extra"?: Object;
}

export interface MultiDataPoints<K> {
    "name": string;
    "series": Data<K>[]
}

export type MultiSeries<K> = MultiDataPoints<K>[];

export type SingleSeries<K> = Data<K>[];