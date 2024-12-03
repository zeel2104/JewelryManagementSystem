import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://localhost:5000/api';

  cartItems: any[] = [];

  constructor(private http: HttpClient) {}

  // Method to get all products with optional query params for search, filter, and sort
  getProducts(search?: string, category?: string, material?: string, minPrice?: number, maxPrice?: number, sortBy?: string): Observable<any> {
    let params = new HttpParams();
    
    if (search) params = params.set('search', search);
    if (category) params = params.set('category', category);
    if (material) params = params.set('material', material);
    if (minPrice) params = params.set('minPrice', minPrice.toString());
    if (maxPrice) params = params.set('maxPrice', maxPrice.toString());
    if (sortBy) params = params.set('sortBy', sortBy);

    return this.http.get(`${this.apiUrl}/products`, { params });
  }

  // Method to add a product to the cart
  addToCart(productId: number, quantity: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/cart/add`, {
      product_id: productId,
      quantity: quantity
    });
  }

  // Method to get all items in the cart
  getCartItems(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/cart/items`);
  }

  // Method to update quantity of a specific item in the cart
  updateCartItem(productId: number, quantity: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/cart/update`, {
      product_id: productId,
      quantity: quantity
    });
  }

  // Method to remove a specific item from the cart
  removeCartItem(productId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/cart/remove/${productId}`);
  }

  // Method to handle checkout of cart items
  checkout(cartItems: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/cart/checkout`, { cartItems });
  }

  // Example usage of addToCart with explicit types for error handling
  exampleAddToCart(productId: number, quantity: number): void {
    this.addToCart(productId, quantity).subscribe(
      (response: any) => {
        console.log('Add to cart response:', response);
      },
      (error: any) => {
        console.error('Error adding to cart:', error);
      }
    );
  }
}
