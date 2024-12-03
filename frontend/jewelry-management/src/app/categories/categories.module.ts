import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
// import { CategoriesComponent } from './categories.component'; // Adjust the path if necessary

@NgModule({
  declarations: [
    // CategoriesComponent,
  ],
  imports: [
    CommonModule // Import CommonModule to use ngIf, ngFor, etc.
  ],
  exports: [
    // CategoriesComponent // Export if it needs to be used in other modules
  ]
})
export class CategoriesModule {}
