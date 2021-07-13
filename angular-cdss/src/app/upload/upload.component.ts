import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, FormControl, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { HandPresence } from './HandPresence';

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
}
