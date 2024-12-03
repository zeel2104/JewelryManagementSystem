

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; 
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../navbar/navbar.component';


@Component({
  selector: 'app-contact-us',
  templateUrl: './contact-us.component.html',
  styleUrls: ['./contact-us.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent]

})
export class ContactUsComponent {
  contactForm = {
    name: '',
    email: '',
    message: ''
  };

  constructor(private http: HttpClient) {}

  onSubmit() {
    this.http.post('http://localhost:5000/api/contact', this.contactForm).subscribe(
      (response: any) => {
        alert(response.message);
        this.contactForm = { name: '', email: '', message: '' }; // Reset the form
      },
      (error) => {
        console.error('Error sending message:', error);
        alert('Failed to send message. Please try again.');
      }
    );
  }
}
