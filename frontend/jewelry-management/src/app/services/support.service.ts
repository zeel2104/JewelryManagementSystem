import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SupportService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // Method to get FAQ data
  getFaqs(): Observable<any> {
    return this.http.get(`${this.apiUrl}/faqs`);
  }

  // Method to send support inquiry
  sendSupportInquiry(name: string, email: string, message: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/support`, { name, email, message });
  }
}
