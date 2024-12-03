import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-manage',
  templateUrl: './manage.component.html',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  styleUrls: ['./manage.component.css'],
})
export class ManageComponent implements OnInit {
  users: any[] = [];
  selectedUser: any = null;
  editForm: FormGroup;

  private apiUrl = 'http://localhost:5000/api/auth';  // Define the base API URL

  constructor(
    private authService: AuthService,
    private http: HttpClient,
    private router: Router,
    private fb: FormBuilder
  ) {
    // Initialize the form group with default values
    this.editForm = this.fb.group({
      name: ['', Validators.required],
      phoneNumber: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    // Fetch the list of users from the backend
    this.getUsers();
  }

  getUsers(): void {
    // Use apiUrl for the GET request
    this.http.get<any[]>(`${this.apiUrl}/users`).subscribe((response) => {
      this.users = response;
    });
  }

  selectUser(user: any): void {
    this.selectedUser = user;

    // Populate the form with the selected user's data
    this.editForm.setValue({
      name: user.name,
      phoneNumber: user.phoneNumber || '',  // Handle cases where phoneNumber may be null
    });
  }

  updateUser(): void {
    if (this.editForm.invalid) {
      return; // Handle validation if form is not valid
    }

    const updatedUser = this.editForm.value;

    // Use apiUrl for the PUT request
    this.http
      .put(`${this.apiUrl}/user/${this.selectedUser.email}`, updatedUser)
      .subscribe(
        (response) => {
          console.log('User updated successfully:', response);
          this.getUsers(); // Refresh user list after update
          this.selectedUser = null; // Reset selected user
        },
        (error) => {
          console.error('Error updating user:', error);
        }
      );
  }

  deleteUser(email: string): void {
    // Use apiUrl for the DELETE request
    this.http.delete(`${this.apiUrl}/user/${email}`).subscribe(
      (response) => {
        console.log('User deleted successfully:', response);
        this.getUsers(); // Refresh user list after deletion
      },
      (error) => {
        console.error('Error deleting user:', error);
      }
    );
  }
}
