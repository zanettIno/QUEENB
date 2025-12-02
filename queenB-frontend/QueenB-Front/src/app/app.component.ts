import { Component } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router'; // 1. Importe Router e NavigationEnd
import { CommonModule } from '@angular/common'; // 2. Importe CommonModule
import { NavbarComponent } from './components/navbar/navbar.component';
import { filter } from 'rxjs/operators'; // 3. Importe 'filter'

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, // 4. Adicione CommonModule
    RouterOutlet,
    NavbarComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'QueenB';
  
  isHomePage: boolean = false;

  constructor(private router: Router) {
    
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(event => {
      
      // --- A MUDANÇA ESTÁ AQUI ---
      // Agora ele checa se a URL "começa com" /home
      this.isHomePage = (event as NavigationEnd).url.startsWith('/home');
      
    });
  }
}