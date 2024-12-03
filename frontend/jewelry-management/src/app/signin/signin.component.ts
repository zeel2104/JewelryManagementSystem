import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule, NavbarComponent, RouterModule],
})
export class SigninComponent {
  errorMessage: string = '';
  successMessage: string = '';
  rememberMe: boolean = false; // Property to handle the "Remember Me" checkbox

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(signinForm: any): void {
    const credentials = {
      email: signinForm.value.email,
      password: signinForm.value.password,
      rememberMe: this.rememberMe,
    };

    this.authService.signIn(credentials).subscribe(
      (response: any) => {
        this.successMessage = 'Sign in successful!';
        setTimeout(() => {
          this.router.navigate(['/']); // Navigate to home or dashboard
        }, 1000);
      },
      (error: any) => {
        this.errorMessage =
          error.error?.error || 'An error occurred during sign-in.';
      }
    );
  }
}
