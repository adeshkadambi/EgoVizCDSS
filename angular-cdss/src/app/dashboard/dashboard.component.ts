import { AngularFirestore } from '@angular/fire/firestore';
import { Component, OnInit } from '@angular/core';
import { Patient } from './patient.model';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { AngularFireAuth } from '@angular/fire/auth';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  patients: Observable<Patient[]>;
  userId: string;

  constructor(private db:AngularFirestore, private afAuth: AngularFireAuth) {}

  ngOnInit(): void {

    this.afAuth.authState.subscribe(user => {
      if(user) {
        this.userId = user.uid;
      }
    });

    // Without timeout, usedId is undefined when query runs.
    setTimeout(()=> {
      this.patients= this.db
      .collection('patients', ref => ref.where("uid", '==', this.userId))
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
          }
        })
      }));
    }, 100);
  }
}
