import { PatientService } from './../patient.service';
import { Patient } from './../patient.model';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { AngularFireAuth } from '@angular/fire/auth';


@Component({
  selector: 'app-patient',
  templateUrl: './patient.component.html',
  styleUrls: ['./patient.component.scss']
})
export class PatientComponent implements OnInit, OnDestroy {

  patients: Patient[];
  patientSub: Subscription;
  patientId: string = null;

  constructor(private afAuth: AngularFireAuth, private patientService:PatientService) {}

  ngOnInit(): void {
    // if user is auth, fetch user's patients
    this.afAuth.authState.subscribe(user => {
      if(user) {
        this.patientService.fetchPatients(user.uid);
        this.patientSub = this.patientService.patientsLoaded.subscribe(patients => {
          this.patients = patients;
        });
      }
    });
  }

  onPatientClick(patientid:string) {
    this.patientService.selectPatient(patientid);
  }

  ngOnDestroy() {
    this.patientSub.unsubscribe();
  }

}
