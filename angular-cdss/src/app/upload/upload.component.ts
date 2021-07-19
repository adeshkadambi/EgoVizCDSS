import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, FormControl, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { HandPresence } from './HandPresence';
import { HandObjInt } from './HandObjInt';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  upForm = new FormGroup({
    file: new FormControl('', [Validators.required]),
    fileSource: new FormControl('', [Validators.required])
  });

  constructor(private http: HttpClient){}

  headers = ["No contact", "Self contact", "Another Person", "Portable Object", "Stationary Object", "Total Interactions"]
  state_map = ["N", "S", "O", "P", "F", "T"]
  state_map2 = {"N":"No contact", "S":"Self contact", "O":"Another Person", "P":"Portable Object", "F":"Stationary Object", "T":"Total Interactions"}
  HO_labels = 	["l_int", "r_int", "l_dur", "r_dur", "l_num", "r_num"];	
  HO_labelmap = {
		"l_int":"[L] Interaction \nproportion (%)",
		"r_int":"[R] Interaction \nproportion (%)",
		"l_dur":"[L] Avg. Interaction \nDuration (s)",
		"r_dur":"[R] Avg. Interaction \nDuration (s)",
		"l_num":"[L] Number of \nInteractions \nper hour (#/hr)",
		"r_num":"[R] Number of \nInteractions \nper hour (#/hr)",
  }


  get f(){
    return this.upForm.controls;
  }

  onFileChange(event) {
    if (event.target.files!.length > 0) {
      const file = event.target.files![0];
      this.upForm.patchValue({
        fileSource: file
      });
    }
  }

  predictions_AB: number[] = [];
  predictionUrl_AB: string = "http://127.0.0.1:5000/uploadpredictAB/";
  submitted_AB: boolean = false;
  response_received_AB: boolean = false;

  predictions_DF: HandPresence;
  predictionUrl_DF: string = "http://127.0.0.1:5000/uploadpredictDF/";
  submitted_DF: boolean = false;
  response_received_DF: boolean = false;

  predictions_HO: HandObjInt;
  predictionUrl_HO: string = "http://127.0.0.1:5000/uploadpredictHO/"
  submitted_HO: boolean = false;
  response_received_HO: boolean = false;

  onSubmit_AB(){
    const formData = new FormData();
    formData.append('input_file', this.upForm.get('fileSource')!.value)
    this.response_received_AB = false;

    try{
      console.log(formData.getAll('input_file'));
    } catch(error) {
      alert('Invalid Submission.');
    }
    
    this.http.post(this.predictionUrl_AB, formData)
      .subscribe(
        response => {
          console.log(response);
          // alert('Uploaded Successfully');
          this.predictions_AB = <number[]>response;
          this.response_received_AB = true;
        }
      );
    
      this.submitted_AB = true;
  }
  onSubmit_DF(){
    const formData = new FormData();
    formData.append('input_file', this.upForm.get('fileSource')!.value)
    this.response_received_DF = false;

    try{
      console.log(formData.getAll('input_file'));
    } catch(error) {
      alert('Invalid Submission.');
    }
    
    this.http.post(this.predictionUrl_DF, formData)
      .subscribe(
        response => {
          console.log(response);
          // alert('Uploaded Successfully');
          this.predictions_DF = <HandPresence>response;
          this.response_received_DF = true;
        }
      );
    
      this.submitted_DF = true;
  }
  onSubmit_HO(){
    const formData = new FormData();
    formData.append('input_file', this.upForm.get('fileSource')!.value)
    this.response_received_HO = false;

    try{
      console.log(formData.getAll('input_file'));
    } catch(error) {
      alert('Invalid Submission.');
    }
    
    this.http.post(this.predictionUrl_HO, formData)
      .subscribe(
        response => {
          console.log(response);
          // alert('Uploaded Successfully');
          this.predictions_HO = <HandObjInt>response;
          this.response_received_HO = true;
        }
      );
      this.submitted_HO = true;
  }
}
