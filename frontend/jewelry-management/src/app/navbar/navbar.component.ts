





import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  isLoggedIn: boolean = false;
  userName: string = '';
  userRole: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    // Subscribe to user$ to reactively update the navbar
    this.authService.user$.subscribe((user) => {
      this.isLoggedIn = !!user;
      this.userName = user || '';
      this.getUserRole(user || '');
    });
  }

    // Fetch the user role from the backend using the email
    getUserRole(name: string): void {
      this.authService.getUser(name).subscribe(
        (response) => {
          if (response && response.role) {
            this.userRole = response.role;  // Set user role from API response
          } else {
            this.userRole = '';  // Handle case where role is not found
          }
        },
        (error) => {
          console.error('Error fetching user details:', error);
          this.userRole = '';  // Default to empty if there is an error
        }
      );
    }

  logout(): void {
    this.authService.clearCurrentUser();
    this.router.navigate(['/signin']);
  }
}





























// import { Component, OnInit } from '@angular/core';
// import { Router, RouterModule } from '@angular/router';
// import { AuthService } from '../auth.service';
// import { FormsModule } from '@angular/forms';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-navbar',
//   standalone: true,
//   imports: [FormsModule, CommonModule, RouterModule],
//   templateUrl: './navbar.component.html',
//   styleUrls: ['./navbar.component.css'],
// })
// export class NavbarComponent implements OnInit {
//   isLoggedIn: boolean = false;
//   userName: string = '';

//   constructor(private authService: AuthService, private router: Router) {}

//   ngOnInit(): void {
//     this.updateLoginStatus();
//   }

//   updateLoginStatus(): void {
//     this.isLoggedIn = this.authService.isLoggedIn();
//     if (this.isLoggedIn) {
//       const user = this.authService.getCurrentUser();
//       this.userName = user ? user.name : '';
//     }
//   }

//   logout(): void {
//     this.authService.clearCurrentUser();
//     this.isLoggedIn = false;
//     this.userName = '';
//     this.router.navigate(['/signin']);
//   }
// }
