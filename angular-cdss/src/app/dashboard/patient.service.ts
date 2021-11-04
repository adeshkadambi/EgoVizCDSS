import { AngularFirestore } from '@angular/fire/firestore';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { Patient, Data, MultiSeries } from './patient.model';


import * as firebase from 'firebase/app';
import 'firebase/firestore';

@Injectable()
export class PatientService {

    // patient change
    patientChanged = new Subject<Patient>();
    private currentPatient: Patient = null;

    // fetch from db
    patientsLoaded = new Subject<Patient[]>();
    private patientList: Patient[] = [];

    //fetch proportion
    propLoaded = new Subject<MultiSeries<Date>>();
    private propList: MultiSeries<Date> = [];

    constructor(private db:AngularFirestore) {}

    fetchPatients(userId:string){
        this.db
        .collection('patients', ref => ref.where("uid", '==', userId))
        .snapshotChanges()
        .pipe(map(docArray => {
        // get all patients and map to Patient model.
            return docArray.map(doc => {
                return {
                    id: doc.payload.doc.id,
                    age: doc.payload.doc.data()['age'],
                    name: doc.payload.doc.data()['name'],
                    description: doc.payload.doc.data()['description'],
                    doctor: doc.payload.doc.data()['uid']
                };
            });
        }))
        .subscribe((patients:Patient[])=>{
            this.patientList = patients;
            this.patientsLoaded.next([...this.patientList]);
        });
    }

    selectPatient(selectedId:string) {
        this.currentPatient = this.patientList.find(pt => pt.id == selectedId);
        this.patientChanged.next({ ...this.currentPatient });

        this.db
        .collection("patients")
        .doc(selectedId)
        .collection("proportion")
        .snapshotChanges()
        .pipe(map(docArray => {
        // get all data and map to LineGraph model.
            return docArray.map(doc => {
                return {
                    name: doc.payload.doc.id,
                    series: doc.payload.doc.data()['series']
                };
            });
        }))
        .subscribe((props: MultiSeries<Date>)=>{
            this.propList = props;
            this.propLoaded.next([...this.propList]);
        });

    }

    exitPatient() {
        this.currentPatient = null;
        this.patientChanged.next(null);
    }

    getCurrent() {
        return { ...this.currentPatient };
    }

    newData(data: Data<Date>) {
        this.db
        .collection("patients")
        .doc("J0glR58bwyAIzQFZDldn")
        .collection("proportion")
        .doc("LeftHand")
        .update({
            series: firebase.default.firestore.FieldValue.arrayUnion({"name": data.name, "value": data.value})
        });
    }

}