import { Component, OnInit } from '@angular/core';
import { ProductService } from '../services/product.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent]
})
export class CartComponent implements OnInit {
  cartItems: any[] = [];
  total: number = 0;

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.loadCartItems();
  }

  // Load all items in the cart
  loadCartItems(): void {
    this.productService.getCartItems().subscribe(
      (items: any[]) => {
        console.log("Cart Items:", items);  // Debugging the cart items
        this.cartItems = items;
        this.calculateTotal();  // Recalculate total after loading items
        console.log("Total after loading:", this.total);  // Debugging the total
      },
      (error: any) => {
        console.error('Error fetching cart items:', error);
      }
    );
}

  // Calculate total price
  calculateTotal(): void {
    this.total = this.cartItems.reduce((acc, item) => {
        const itemTotal = item.Quantity * item.Price;
        console.log(`Item Total for ${item.Name}:`, itemTotal);  // Debugging item total
        return acc + itemTotal;
    }, 0);
    console.log("Total calculated:", this.total);  // Debugging final total
}
  // Increase quantity of an item in the cart
  increaseQuantity(item: any): void {
    const newQuantity = item.Quantity + 1;
    this.updateQuantity(item, newQuantity);
  }

  // Decrease quantity of an item in the cart
  decreaseQuantity(item: any): void {
    if (item.Quantity > 1) {
      const newQuantity = item.Quantity - 1;
      this.updateQuantity(item, newQuantity);
    }
  }

  // Update quantity of an item in the cart
  updateQuantity(item: any, quantity: number): void {
    this.productService.updateCartItem(item.ProductID, quantity).subscribe(
      () => {
        item.Quantity = quantity;
        this.calculateTotal();
      },
      (error: any) => {
        console.error('Error updating cart item:', error);
      }
    );
  }

  // Remove an item from the cart
  removeFromCart(item: any): void {
    this.productService.removeCartItem(item.ProductID).subscribe(
      () => {
        this.cartItems = this.cartItems.filter(cartItem => cartItem.ProductID !== item.ProductID);
        this.calculateTotal();
      },
      (error: any) => {
        console.error('Error removing item from cart:', error);
      }
    );
  }

  // Checkout cart items
  checkout(): void {
    this.productService.checkout(this.cartItems).subscribe(
      (response: any) => {
        console.log('Checkout successful:', response);
        alert('Checkout successful!');
        this.cartItems = [];
        this.total = 0;
      },
      (error: any) => {
        console.error('Error during checkout:', error);
      }
    );
  }
}
