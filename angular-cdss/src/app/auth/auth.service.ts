import { User } from './user.model';
import { AuthData } from './auth-data.model';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { AngularFireAuth } from "@angular/fire/auth";

@Injectable()
export class AuthService {

    authChange = new Subject<boolean>();
    private isAuthenticated = false;

    constructor(private router:Router, private afAuth:AngularFireAuth) {

    }

    registerUser(authData:AuthData) {
        this.afAuth
            .createUserWithEmailAndPassword(authData.email, authData.password)
            .then(result => {
                this.authSuccess();
            })
            .catch(error => {
                console.log(error);
            });
    }

    login(authData:AuthData) {
        this.afAuth
            .signInWithEmailAndPassword(authData.email, authData.password)
            .then(result => {
                this.authSuccess();
                this.isAuthenticated = true;
            })
            .catch(error => {
                console.log(error);
            });
    }

    logout() {
        this.isAuthenticated = false;
        this.authChange.next(false);
        this.afAuth.signOut();
        this.router.navigate(['/login']);
    }

    isAuth() {
        return this.isAuthenticated;
    }

    private authSuccess() {
        this.authChange.next(true);
        this.router.navigate(['/dashboard']);
    }
}