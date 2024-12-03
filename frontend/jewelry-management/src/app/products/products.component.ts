import { Component, OnInit } from '@angular/core';
import { ProductService } from '../services/product.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent]
})
export class ProductsComponent implements OnInit {
  products: any = [];
  categories: string[] = ['Necklaces', 'Bracelets', 'Rings', 'Earrings', 'Brooches', 'Watches', 'Pendants', 'Anklets', 'Charms'];
  materials: string[] = ['Gold', 'Silver', 'Pearl', 'Leather', 'Titanium', 'Mixed'];

  searchQuery: string = '';
  selectedCategory: string = '';
  selectedMaterial: string = '';
  minPrice: number | null = null;
  maxPrice: number | null = null;
  sortBy: string = '';

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
  
    this.productService.getProducts(
      this.searchQuery,
      this.selectedCategory,
      this.selectedMaterial,
      this.minPrice ? this.minPrice : undefined,  // Make sure it passes only when there's a value
      this.maxPrice ? this.maxPrice : undefined,  // Same for maxPrice
      this.sortBy
    ).subscribe(
      data => {
        this.products = data;
      },
      error => {
        console.error('Error loading products:', error);
      }
    );
  }
  
  increaseQuantity(product: any): void {
    product.quantity = (product.quantity || 1) + 1;
  }

  decreaseQuantity(product: any): void {
    if (product.quantity && product.quantity > 1) {
      product.quantity -= 1;
    }
  }

  addToCart(product: any): void {
    const cartItem = {
      product_id: product.ProductID,
      quantity: product.quantity || 1
    };
    
    this.productService.addToCart(cartItem.product_id, cartItem.quantity).subscribe(
      response => {
        console.log('Add to cart successful:', response);
        alert(`${cartItem.quantity} ${product.Name}(s) added to cart.`);
      },
      error => {
        console.error('Error adding to cart:', error);
      }
    );
  }

  clearFilters(): void {
    this.searchQuery = '';
    this.selectedCategory = '';
    this.selectedMaterial = '';
    this.minPrice = null;
    this.maxPrice = null;
    this.sortBy = '';
    this.loadProducts();
  }
}
