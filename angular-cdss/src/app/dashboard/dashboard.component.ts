import { Patient } from './patient.model';
import { PatientService } from './patient.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {

  selectedPatient = false;
  patientSub: Subscription;
  currentPatient:Patient;

  constructor(private patientService:PatientService) {}

  ngOnInit(): void {
    this.patientSub = this.patientService.patientChanged.subscribe(
      patient => {
        if (patient) {
          this.selectedPatient = true;
          this.currentPatient = this.patientService.getCurrent();
        } else {
          this.selectedPatient = false;
        }
    });
  }

  checkPatient(){
    console.log(this.patientService.getCurrent());
  }

  goBack(){
    this.patientService.exitPatient();
  }

  ngOnDestroy() {
    this.patientService.exitPatient();
    this.patientSub.unsubscribe();
  }

}
