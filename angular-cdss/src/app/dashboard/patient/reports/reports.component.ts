import { MultiSeries, SingleSeries } from './../../patient.model';
import ChartSettings from './charts.model';
import { Subscription } from 'rxjs';
import { PatientService } from './../../patient.service';
import { multi, minutes_recorded, patient_notes, activity_breakdown, posture_use, postures } from './data';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { DatePipe } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { NgxChartsModule } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent implements OnInit, OnDestroy {

  view: "quantity" | "quality" = "quantity";

  dataSub: Subscription;
  propData: MultiSeries<Date>;

  multi: MultiSeries<Date>;
  minutes_recorded: SingleSeries<number>;
  patient_notes: Array<{date: Date, note: string}>;
  activity_breakdown: SingleSeries<string>; // set to Date
  posture_use: MultiSeries<string>; //set to Date
  postures: Array<{name: string, image: string}>

  // options
  barSettings: ChartSettings = {
    chartType: "bar",
    scheme: {
      domain: ['#d6d6d6']
    },
    legend: false,
    animations: true,

    xAxis: true,
    yAxis: false,
    showYAxisLabel: false,
    showXAxisLabel: true,
    xAxisLabel: 'Date',

    showDataLabel: true,
    roundEdges: false,
  }

  lineSettings: ChartSettings = {
    chartType: "line",
    scheme: {
      domain: ['#EB5757', '#2F80ED']
    },
    legend: false,
    animations: true,

    xAxis: true,
    yAxis: true,
    showYAxisLabel: true,
    showXAxisLabel: true,
    xAxisLabel: 'Date',
    yAxisLabel: 'Percentage (%)',

    timeline: false,
  }

  pieSettings: ChartSettings = {
    chartType: "pie",
    scheme: {
      domain: ['#9B51E0', '#ACB9FF', '#503795', '#000000']
    },
    legend: false,
    animations: true,

    showLabels: false,
  }

  stackSettings: ChartSettings = {
    chartType: "stack",
    scheme: {
        domain: ["#8ABFF2", "#4F8AD3", "#E3873E", "#FADB7B"]
    },
    legend: false,
    animations: true,

    xAxis: true,
    yAxis: true,
    showYAxisLabel: true,
    showXAxisLabel: true,
    xAxisLabel: "Date",
    yAxisLabel: "Percentage (%)",

    showDataLabel: false,
    roundEdges: false,
  };

  constructor(private patientService: PatientService, private datePipe: DatePipe) { 
    Object.assign(this, { multi, minutes_recorded, patient_notes, activity_breakdown, posture_use, postures });
  }

  ngOnInit() {
    this.dataSub = this.patientService.propLoaded.subscribe(props => {
      this.propData = props;
    });
    console.log(this.propData);
  }

  ngOnDestroy() {
    this.dataSub.unsubscribe();
  }

  togglePage = () => {
    this.view = this.view === "quantity" ? "quality" : "quantity"; 
  }
}
