
// import { Component, OnInit } from '@angular/core';
// import { CategoryService } from '../services/category.service';

// interface Category {
//   CategoryID: number;
//   Name: string;
//   Description: string;
// }

// @Component({
//   selector: 'app-categories',
//   templateUrl: './categories.component.html',
//   styleUrls: ['./categories.component.css']
// })
// export class CategoriesComponent implements OnInit {
//   categories: Category[] = [];

//   constructor(private categoryService: CategoryService) {}

//   ngOnInit(): void {
//     this.getCategories();
//   }

//   getCategories(): void {
//     this.categoryService.getCategories().subscribe((data) => {
//       console.log("Categories data:", data); // Add this line
//       this.categories = data;
//     });
//   }
// }

import { Component, OnInit } from '@angular/core';
import { CategoryService } from '../services/category.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; 
import { NavbarComponent } from '../navbar/navbar.component';

interface Category {
  CategoryID: number;
  Name: string;
  Description: string;
}

@Component({
  selector: 'app-categories',
  templateUrl: './categories.component.html',
  styleUrls: ['./categories.component.css'],
  standalone: true, // Add this if you are using standalone components
  imports: [CommonModule, RouterModule, NavbarComponent]
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];

  constructor(private categoryService: CategoryService) {
    console.log('CategoriesComponent initialized. CommonModule should be imported in its module.');
  }

  ngOnInit(): void {
    this.getCategories();
  }

  getCategories(): void {
    this.categoryService.getCategories().subscribe((data) => {
      // console.log("Categories data:", data);
      this.categories = data;
    });
  }
}
