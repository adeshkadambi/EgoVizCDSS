import { test_val } from './patient/reports/data';
import { Patient, LineGraph } from './patient.model';
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

  dataSub: Subscription;
  propData: LineGraph[];

  constructor(private patientService:PatientService) {}

  ngOnInit(): void {
    this.patientSub = this.patientService.patientChanged.subscribe(
      patient => {
        if (patient) {
          this.selectedPatient = true;
          this.currentPatient = this.patientService.getCurrent();
          this.dataSub = this.patientService.propLoaded.subscribe(props => {
            this.propData = props;
            console.log(this.propData);
          });
        } else {
          this.selectedPatient = false;
          this.propData = null;
          console.log(this.propData);
        }
    });
  }

  checkPatient(){
    this.patientService.newData(test_val);
  }

  goBack(){
    this.patientService.exitPatient();
  }

  ngOnDestroy() {
    this.patientService.exitPatient();
    this.patientSub.unsubscribe();
  }

}
