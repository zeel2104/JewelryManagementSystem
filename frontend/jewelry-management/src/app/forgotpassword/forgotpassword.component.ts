import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgotpassword.component.html',
  standalone: true,
  imports: [CommonModule,FormsModule],
  styleUrls: ['./forgotpassword.component.css'],
})
export class ForgotPasswordComponent {
  message: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService) {}

  onSubmit(forgotPasswordForm: any): void {
    const email = forgotPasswordForm.value.email;

    this.authService.sendResetLink(email).subscribe(
      (response: any) => {
        this.message = 'Password reset link sent to your email.';
        this.errorMessage = '';
      },
      (error: any) => {
        this.errorMessage = error.error?.error || 'An error occurred.';
        this.message = '';
      }
    );
  }
}
