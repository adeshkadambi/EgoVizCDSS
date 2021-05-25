# EgoViz Documentation

## Data Storage & Confidentiality 
Processed videos and insights will also be stored in Google Cloud Firestore, a flexible, scalable NoSQL cloud database, in order to display insights in a dashboard format to participants. The Cloud Firestore database will be configured to the `northamerica-northeast1` resource region located in Montreal. Therefore, all data will physically be stored in Canada. We will ensure HIPAA compliance with Cloud Firestore using the guidelines provided by Google Cloud. Participants will be able to view processed video and insights for their patients upon secure login and user authentication. All patient data will be deleted from Cloud Firestore 30 days after data collection and interviews are complete, but will remain on secure servers at the University Centre for future analyses. Non-identifiable video may be used in publications and presentations for academic and teaching purposes. Names and other identifying information apart from the images will never be included in any way. 

### Database Structure

```
collection: patients
  document: patientid {
    name: string
    description: string
    age: number
    doctorid: string
  }
```
