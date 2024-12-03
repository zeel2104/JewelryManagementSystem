import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SupportComponent } from './support/support.component';
import { LandingComponent } from './landing/landing.component';
import { CategoriesComponent } from './categories/categories.component';
import { ProductsComponent } from './products/products.component';
import { SignupComponent } from './signup/signup.component';
import { SigninComponent } from './signin/signin.component';
import { CartComponent } from './cart/cart.component';
import { ContactUsComponent } from './contact-us/contact-us.component';
import { ManageComponent } from './manage/manage.component';
import { ForgotPasswordComponent } from './forgotpassword/forgotpassword.component';

export const routes: Routes = [
  //{ path: '', redirectTo: '/categories', pathMatch: 'full' },  // Redirect to categories
  { path: '', component: LandingComponent },  // Default route to landing page
  { path: 'categories', component: CategoriesComponent },
  { path: 'products', component: ProductsComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'signin', component: SigninComponent },
  { path: 'cart', component: CartComponent},
  {path: 'contact-us', component:ContactUsComponent},
  { path: 'support', component: SupportComponent },
  {path: 'forgotpassword', component: ForgotPasswordComponent},
  { path: 'manage', component: ManageComponent}
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }






