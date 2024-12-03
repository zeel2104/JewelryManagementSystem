import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://localhost:5000/api/products';

  constructor(private http: HttpClient) {}

  getProducts(
    searchQuery: string = '',
    selectedCategory: string = '',
    selectedMaterial: string = '',
    minPrice?: number,
    maxPrice?: number,
    sortBy: string = ''
  ): Observable<any> {
    let params = new HttpParams()
      .set('search', searchQuery)
      .set('category', selectedCategory)
      .set('material', selectedMaterial)
      .set('sort_by', sortBy);
  
    if (minPrice !== undefined) {
      params = params.set('min_price', minPrice.toString());  // Make sure it's a string
    }
  
    if (maxPrice !== undefined) {
      params = params.set('max_price', maxPrice.toString());
    }
    console.log("Minprice: "+minPrice);
  
    return this.http.get<any>(this.apiUrl, { params });
  }
  
}
