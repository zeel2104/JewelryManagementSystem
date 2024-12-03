import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api/auth';
  private readonly USER_KEY = 'currentUser';
  private memoryStorage: Record<string, any> = {};

  // BehaviorSubject to track login state
  private userSubject = new BehaviorSubject<string | null>(this.getCurrentUser());

  user$: Observable<string | null> = this.userSubject.asObservable(); // Expose as Observable

  constructor(private http: HttpClient) {}

  signIn(credentials: { email: string; password: string }): Observable<any> {
    return new Observable((observer) => {
      this.http.post(`${this.apiUrl}/signin`, credentials).subscribe(
        (response: any) => {
          this.saveUser(response.name);
          this.userSubject.next(response.name); // Update the BehaviorSubject
          observer.next(response);
          observer.complete();
        },
        (error) => observer.error(error)
      );
    });
  }

  signUp(userData: { email: string; password: string; name: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup`, userData);
  }

  getAllUsers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/users`);
  }

  getUser(email: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/user/${email}`);
  }
  sendResetLink(email: string) {
    return this.http.post('/api/auth/forgot-password', { email });
  }

  resetPassword(email: string, newPassword: string) {
    return this.http.post('/api/auth/reset-password', { email, newPassword });
  }

  saveUser(userName: string): void {
    if (this.isLocalStorageAvailable()) {
      localStorage.setItem(this.USER_KEY, userName);
    } else {
      this.memoryStorage[this.USER_KEY] = userName;
    }
    this.userSubject.next(userName); // Update BehaviorSubject
  }

  getCurrentUser(): string | null {
    if (this.isLocalStorageAvailable()) {
      try {
        console.log("using localstorage")
        return localStorage.getItem(this.USER_KEY) || null;
      } catch (error) {
        return null;
      }
    }
    console.log("using memory")
    return this.memoryStorage[this.USER_KEY] || null;
  }

  clearCurrentUser(): void {
    if (this.isLocalStorageAvailable()) {
      localStorage.removeItem(this.USER_KEY);
    } else {
      delete this.memoryStorage[this.USER_KEY];
    }
    this.userSubject.next(null); // Update BehaviorSubject to null
  }

  isLoggedIn(): boolean {
    return !!this.getCurrentUser();
  }

  private isLocalStorageAvailable(): boolean {
    try {
      const testKey = '__test__';
      localStorage.setItem(testKey, 'test');
      localStorage.removeItem(testKey);
      return true;
    } catch (error) {
      return false;
    }
  }
}

































// import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Observable } from 'rxjs';

// @Injectable({
//   providedIn: 'root',
// })
// export class AuthService {
//   private apiUrl = 'http://localhost:5000/api/auth';
//   private readonly USER_KEY = 'currentUser'; // Key for storing user data
//   private memoryStorage: Record<string, any> = {}; // Fallback for environments without localStorage

//   constructor(private http: HttpClient) {}

//   // Sign-in method
//   signIn(credentials: { email: string; password: string }): Observable<any> {
//     console.log("sign in")
//     return new Observable(observer => {
//       this.http.post(`${this.apiUrl}/signin`, credentials).subscribe(
//         (response: any) => {
//           console.log("response singnin : "+JSON.stringify(response))
//           this.saveUser(response.user); // Save user after successful login
//           observer.next(response);
//           observer.complete();
//         },
//         error => observer.error(error)
//       );
//     });
//   }
//   public signUp(userData: { email: string; password: string; name: string }): Observable<any> {
//     return this.http.post(`${this.apiUrl}/signup`, userData);
//   }

//   // Save user to localStorage or fallback to memory
//   public saveUser(user: any): void {
//     console.log("SAVE USER")
//     if (this.isLocalStorageAvailable()) {
//       try {
//         console.log("user : "+user)
//         localStorage.setItem(this.USER_KEY, JSON.stringify(user));
//       } catch (error) {
//         console.error('Error saving user to localStorage:', error);
//       }
//     } else {
//       console.log("USER : "+user);
//       this.memoryStorage[this.USER_KEY] = user;
//     }
//   }

//   // Get user from localStorage or memory
//   getCurrentUser(): any {
//     if (this.isLocalStorageAvailable()) {
//       try {
//         console.log("key: "+this.USER_KEY);
//         const user = localStorage.getItem(this.USER_KEY);
//         console.log("user: "+user);
//         return user ? JSON.parse(user) : null;
//       } catch (error) {
//         console.error('Error retrieving user from localStorage:', error);
//         return null;
//       }
//     }
//     console.log("Memory: "+ JSON.stringify(this.memoryStorage))
//     return this.memoryStorage[this.USER_KEY] || null;
//   }

//   // Clear user from localStorage or memory
//   clearCurrentUser(): void {
//     if (this.isLocalStorageAvailable()) {
//       try {
//         localStorage.removeItem(this.USER_KEY);
//       } catch (error) {
//         console.error('Error clearing user from localStorage:', error);
//       }
//     } else {
//       delete this.memoryStorage[this.USER_KEY];
//     }
//   }

//   // Check if user is logged in
//   isLoggedIn(): boolean {
//     console.log("this.currentUser"+this.getCurrentUser())
//     return !!this.getCurrentUser();
//   }

//   // Check if localStorage is available
//   private isLocalStorageAvailable(): boolean {
//     try {
//       const testKey = '__test__';
//       localStorage.setItem(testKey, 'test');
//       localStorage.removeItem(testKey);
//       return true;
//     } catch (e) {
//       console.log("LocalStorage : False"+e)
//       return false;
//     }
//   }
// }










































// import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Observable } from 'rxjs';

// @Injectable({
//   providedIn: 'root',
// })
// export class AuthService {
//   private apiUrl = 'http://localhost:5000/api/auth';
//   private readonly USER_KEY = 'currentUser'; // Key for storing user data
//   private memoryStorage: Record<string, any> = {}; // Fallback for non-browser environments

//   constructor(private http: HttpClient) {}

//   // Sign-in method
//   signIn(credentials: { email: string; password: string }): Observable<any> {
//     return this.http.post(`${this.apiUrl}/signin`, credentials);
//   }

//   // Sign-up method
//   signUp(userData: { email: string; password: string; name: string }): Observable<any> {
//     return this.http.post(`${this.apiUrl}/signup`, userData);
//   }

//   // Save user to localStorage or fallback to memory
//   saveUser(user: any): void {
//     if (this.isLocalStorageAvailable()) {
//       try {
//         localStorage.setItem(this.USER_KEY, JSON.stringify(user));
//       } catch (error) {
//         console.error('Error saving user to localStorage:', error);
//       }
//     } else {
//       this.memoryStorage[this.USER_KEY] = user;
//     }
//   }

//   // Get user from localStorage or memory
//   getCurrentUser(): any {
//     if (this.isLocalStorageAvailable()) {
//       try {
//         const user = localStorage.getItem(this.USER_KEY);
//         return user ? JSON.parse(user) : null;
//       } catch (error) {
//         console.error('Error retrieving user from localStorage:', error);
//         return null;
//       }
//     }
//     return this.memoryStorage[this.USER_KEY] || null;
//   }

//   // Clear user from localStorage or memory
//   clearCurrentUser(): void {
//     if (this.isLocalStorageAvailable()) {
//       try {
//         localStorage.removeItem(this.USER_KEY);
//       } catch (error) {
//         console.error('Error clearing user from localStorage:', error);
//       }
//     } else {
//       delete this.memoryStorage[this.USER_KEY];
//     }
//   }

//   // Check if user is logged in
//   isLoggedIn(): boolean {
//     return !!this.getCurrentUser();
//   }

//   // Check if localStorage is available
//   private isLocalStorageAvailable(): boolean {
//     try {
//       const testKey = '__test__';
//       localStorage.setItem(testKey, 'test');
//       localStorage.removeItem(testKey);
//       return true;
//     } catch {
//       console.warn('localStorage is not available.');
//       return false;
//     }
//   }
// }
