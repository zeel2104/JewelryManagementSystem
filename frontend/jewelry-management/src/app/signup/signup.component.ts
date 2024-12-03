import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule, NavbarComponent, RouterModule]
})
export class SignupComponent {
  errorMessage: string = '';
  successMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(signupForm: any): void {
    const userData = {
      name: signupForm.value.name,
      email: signupForm.value.email,
      password: signupForm.value.password
    };

    this.authService.signUp(userData).subscribe(
      (response: any) => {
        console.log('Sign up successful', response);
        this.successMessage = 'Account created successfully. You can now sign in!';
        this.errorMessage = '';
        signupForm.reset();
        // Redirect to Sign In page after 2 seconds
        setTimeout(() => {
          this.router.navigate(['/signin']);
        }, 2000);
      //  signupForm.reset(); // Clear form after successful signup
      },
      (error: any) => {
        console.error('Sign up error', error);
        this.errorMessage = error.error ? error.error.message : 'An error occurred during signup.';
        this.successMessage = '';
      }
    );
  }
}
