import { Directive, ElementRef } from '@angular/core';

@Directive({
  selector: '[appTestDirective]'
})
export class TestDirective {
  constructor(el: ElementRef) {
    console.log('Test Directive Loaded:', el.nativeElement);
  }
}
