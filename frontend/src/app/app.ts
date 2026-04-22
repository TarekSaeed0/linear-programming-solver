import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ObjectiveInput } from './components/problem-input/objective-input/objective-input';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ObjectiveInput],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {}
