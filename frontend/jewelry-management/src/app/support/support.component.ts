import { Component, OnInit } from '@angular/core';
import { SupportService } from '../services/support.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-support',
  templateUrl: './support.component.html',
  styleUrls: ['./support.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class SupportComponent implements OnInit {
  faqs: any[] = [];
  name: string = '';
  email: string = '';
  message: string = '';
  inquirySent: boolean = false;

  constructor(private supportService: SupportService) {}

  ngOnInit(): void {
    this.loadFaqs();
  }

  // Load FAQs from backend
  loadFaqs(): void {
    this.supportService.getFaqs().subscribe(
      data => {
        this.faqs = data;
      },
      error => {
        console.error('Error loading FAQs:', error);
      }
    );
  }

  // Send support inquiry
  sendInquiry(): void {
    if (this.name && this.email && this.message) {
      this.supportService.sendSupportInquiry(this.name, this.email, this.message).subscribe(
        response => {
          console.log('Support inquiry sent:', response);
          this.inquirySent = true;
          // Reset form
          this.name = '';
          this.email = '';
          this.message = '';
        },
        error => {
          console.error('Error sending support inquiry:', error);
        }
      );
    } else {
      alert('Please fill out all fields.');
    }
  }
}
