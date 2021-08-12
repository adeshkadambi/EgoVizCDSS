import { LineGraph } from './../../patient.model';
import { Subscription } from 'rxjs';
import { PatientService } from './../../patient.service';
import { multi } from './data';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgxChartsModule } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent implements OnInit, OnDestroy {

  dataSub: Subscription;
  propData: LineGraph[];

  multi: any[];
  view: any[] = [700, 300];

  // options
  legend: boolean = true;
  showLabels: boolean = true;
  animations: boolean = true;
  xAxis: boolean = true;
  yAxis: boolean = true;
  showYAxisLabel: boolean = true;
  showXAxisLabel: boolean = true;
  xAxisLabel: string = 'Date';
  yAxisLabel: string = 'Percentage (%)';
  timeline: boolean = false;

  colorScheme = {
    domain: ['#EB5757', '#2F80ED']
  };


  constructor(private patientService:PatientService) { 
    Object.assign(this, { multi });
  }

  ngOnInit(): void {
    this.dataSub = this.patientService.propLoaded.subscribe(props => {
      this.propData = props;
    });

    console.log(this.propData);
  }

  ngOnDestroy() {
    this.dataSub.unsubscribe();
  }

}
