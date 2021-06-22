import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, FormControl, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

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

  predictions: number[] = [];
  predictionUrl: string = "http://127.0.0.1:5000/uploadpredict/";
  submitted: boolean = false;
  response_received: boolean = false;

  onSubmit(){
    const formData = new FormData();
    formData.append('input_file', this.upForm.get('fileSource')!.value)
    this.response_received = false;

    try{
      console.log(formData.getAll('input_file'));
    } catch(error) {
      alert('Invalid Submission.');
    }
    
    this.http.post(this.predictionUrl, formData)
      .subscribe(
        response => {
          console.log(response);
          // alert('Uploaded Successfully');
          this.predictions = <number[]>response;
          this.response_received = true;
        }
      );
    
      this.submitted = true;
  }
}
